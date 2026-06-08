"""
build_facttable.py  (stdlib only — pandas 불가 환경 대응)

파이프라인 위치: analyze_data.py → chart_data.json → [이 스크립트] → build_dashboard.py
  - out/focus-normalized.csv(레코드 단위 FOCUS 데이터)를 읽어 일자 단위 팩트테이블을 생성
  - 기존 out/chart_data.json에 'fact' / 'fact_schema' 키를 주입(기존 키는 보존)
  - 임베드될 '반올림된' 팩트가 기존 모든 집계를 재현하는지 단언(정합성 게이트)
  - 브라우저 검증용 '필터 오라클'(원본 CSV에서 독립 산출)을 출력

AI/Vertex 규칙: AI = (ModelName != '' OR ServiceName == 'Vertex AI'); Vertex 행은 model='Vertex AI'
  (기존 chart_data.json의 AI 합계 843,695 = 토큰모델 796,175 + Vertex 47,520 와 일치)
"""
import csv, json, sys
from collections import defaultdict

PROV = {'Amazon Web Services':'AWS','Microsoft Azure':'Azure','Google Cloud Platform':'GCP',
        'Anthropic':'Anthropic','OpenAI':'OpenAI'}
SCHEMA = ['date','csp','service','cc','proj','model','cost','inCost','outCost']

def tag(s, k):
    try:
        t = json.loads(s) if s else {}
        return (t.get(k, '') or '')
    except Exception:
        return ''

def fnum(x):
    try: return float(x)
    except Exception: return 0.0

# ---- read raw ----
raw = []
with open('out/focus-normalized.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        raw.append(row)

def norm(row):
    d = row['ChargePeriodStart'][:10]
    csp = PROV.get(row['ServiceProviderName'], row['ServiceProviderName'])
    cc = tag(row.get('Tags',''), 'CostCenter')
    proj = tag(row.get('Tags',''), 'Project')
    svc = row.get('ServiceName','')
    mn = (row.get('ModelName') or '').strip()
    cost = fnum(row.get('AmortizedCost_KRW'))
    ti = fnum(row.get('TokenCountInput')); to = fnum(row.get('TokenCountOutput'))
    if mn:                       # 토큰 기반 모델
        model = mn
        tot = ti + to
        inC = cost*ti/tot if tot > 0 else 0.0
        outC = cost*to/tot if tot > 0 else 0.0
    elif svc == 'Vertex AI':     # GPU형 AI (토큰 없음) → Vertex AI 모델로 라벨
        model = 'Vertex AI'; inC = cost; outC = 0.0
    else:                        # 비-AI 인프라
        model = ''; inC = 0.0; outC = 0.0
    return d, csp, svc, cc, proj, model, cost, inC, outC

# ---- aggregate to daily fact grain (rounded for embed fidelity test) ----
agg = defaultdict(lambda: [0.0, 0.0, 0.0])  # key -> [cost, inCost, outCost]
for row in raw:
    d, csp, svc, cc, proj, model, cost, inC, outC = norm(row)
    k = (d, csp, svc, cc, proj, model)
    a = agg[k]; a[0]+=cost; a[1]+=inC; a[2]+=outC

fact = []
for (d,csp,svc,cc,proj,model), (cost,inC,outC) in agg.items():
    fact.append([d,csp,svc,cc,proj,model, round(cost,2), round(inC,2), round(outC,2)])
fact.sort()

# ============================================================
# RECONCILIATION GATE — re-aggregate from ROUNDED fact, compare to committed chart_data.json
cd = json.load(open('out/chart_data.json', encoding='utf-8'))
DATES = cd['dates']
Fi = {n:i for i,n in enumerate(SCHEMA)}
def col(r,n): return r[Fi[n]]
fails = []
def check(name, ok, detail=''):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ''))
    if not ok: fails.append(name)

print('=== RECONCILE (rounded fact vs committed chart_data.json, tol<1 KRW) ===')

# 1. csp_total
ct = defaultdict(float)
for r in fact: ct[col(r,'csp')] += col(r,'cost')
check('csp_total', all(abs(ct[k]-v) < 1 for k,v in cd['csp_total'].items()))

# 2. daily_by_csp
dbc = {c:[0.0]*len(DATES) for c in cd['csps']}
di = {d:i for i,d in enumerate(DATES)}
for r in fact:
    if col(r,'csp') in dbc: dbc[col(r,'csp')][di[col(r,'date')]] += col(r,'cost')
check('daily_by_csp', all(abs(dbc[c][i]-cd['daily_by_csp'][c][i])<1 for c in cd['csps'] for i in range(len(DATES))))

# 3. svc_top10
sv = defaultdict(float)
for r in fact: sv[col(r,'service')] += col(r,'cost')
top10 = sorted(sv.items(), key=lambda x:-x[1])[:10]
check('svc_top10.labels', [l for l,_ in top10] == cd['svc_top10']['labels'])
check('svc_top10.values', all(abs(v-cd['svc_top10']['values'][i])<1 for i,(_,v) in enumerate(top10)))

# 4. daily_by_cc
for cc, arr in cd['daily_by_cc'].items():
    s = [0.0]*len(DATES)
    for r in fact:
        if col(r,'cc')==cc: s[di[col(r,'date')]] += col(r,'cost')
    check(f'daily_by_cc[{cc}]', all(abs(s[i]-arr[i])<1 for i in range(len(DATES))))

# 5. daily_by_proj
for pj, arr in cd['daily_by_proj'].items():
    s = [0.0]*len(DATES)
    for r in fact:
        if col(r,'proj')==pj: s[di[col(r,'date')]] += col(r,'cost')
    check(f'daily_by_proj[{pj}]', all(abs(s[i]-arr[i])<1 for i in range(len(DATES))))

# 6. ai_trend (AI = model != '')
at = defaultdict(float)
for r in fact:
    if col(r,'model')!='' : at[col(r,'date')] += col(r,'cost')
jt = dict(zip(cd['ai_trend']['dates'], cd['ai_trend']['values']))
check('ai_trend', all(abs(at[d]-jt[d])<1 for d in jt))

# 7. ai_token_chart (per model inCost/outCost)
mt = defaultdict(lambda:[0.0,0.0])
for r in fact:
    if col(r,'model')!='' : mt[col(r,'model')][0]+=col(r,'inCost'); mt[col(r,'model')][1]+=col(r,'outCost')
jt_lab = cd['ai_token_chart']['labels']
check('ai_token.input', all(abs(mt[m][0]-cd['ai_token_chart']['input_costs'][i])<1 for i,m in enumerate(jt_lab)))
check('ai_token.output', all(abs(mt[m][1]-cd['ai_token_chart']['output_costs'][i])<1 for i,m in enumerate(jt_lab)))

# 8/9. totals
check('total_ai_cost', abs(sum(col(r,'cost') for r in fact if col(r,'model')!='') - cd['unit_econ']['total_ai_cost'])<1)
check('total_cost', abs(sum(col(r,'cost') for r in fact) - cd['unit_econ']['total_cost'])<1)

# ============================================================
# FILTERED ORACLES — computed independently from RAW CSV (full precision) for browser cross-check
print('\n=== FILTERED ORACLES (raw CSV, full precision) ===')
N = [norm(r) for r in raw]   # tuples
IN = {n:i for i,n in enumerate(['date','csp','svc','cc','proj','model','cost','inC','outC'])}
def g(t,n): return t[IN[n]]

def csp_sum(pred):
    o = defaultdict(float)
    for t in N:
        if pred(t): o[g(t,'csp')] += g(t,'cost')
    return {k:round(v,2) for k,v in sorted(o.items())}
def svc_top(pred, k=10):
    o = defaultdict(float)
    for t in N:
        if pred(t): o[g(t,'svc')] += g(t,'cost')
    return [[s,round(v,2)] for s,v in sorted(o.items(), key=lambda x:-x[1])[:k]]

print('O1 c2 | CC-300 (full month) per-CSP:', json.dumps(csp_sum(lambda t: g(t,'cc')=='CC-300'), ensure_ascii=False))
print('O2 c3 | Project=ml top10 svc:', json.dumps(svc_top(lambda t: g(t,'proj')=='ml'), ensure_ascii=False))
o3 = round(sum(g(t,'cost') for t in N if g(t,'model')=='gpt-4o' and g(t,'cc')=='CC-200'), 2)
print('O3 c8 | Model=gpt-4o AND CC-200 total AI cost:', o3)
print('O4 c2 | CC-300 AND Project=ml per-CSP:', json.dumps(csp_sum(lambda t: g(t,'cc')=='CC-300' and g(t,'proj')=='ml'), ensure_ascii=False))
print('O5 c2 | date>=2026-03-18 (no other) per-CSP:', json.dumps(csp_sum(lambda t: g(t,'date')>='2026-03-18'), ensure_ascii=False))
o6 = round(sum(g(t,'inC') for t in N if g(t,'model')=='gpt-4o'),2), round(sum(g(t,'outC') for t in N if g(t,'model')=='gpt-4o'),2)
print('O6 c6 | Model=gpt-4o (in,out):', o6)

# ============================================================
if fails:
    print('\nRECONCILE FAILED:', fails); sys.exit(1)

cd['fact'] = fact
cd['fact_schema'] = SCHEMA
with open('out/chart_data.json', 'w', encoding='utf-8') as f:
    json.dump(cd, f, ensure_ascii=False, indent=2)
print(f'\nOK - injected fact ({len(fact)} rows) into out/chart_data.json; all reconciliations PASS')
