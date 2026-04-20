import csv, os
from collections import defaultdict

util_rows = []
with open('resources/sample-billing/utilization-sample.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        util_rows.append(row)

focus_rows = []
with open('out/focus-normalized.csv', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        focus_rows.append(row)

def extract_suffix(rid):
    return rid.split('/')[-1] if '/' in rid else rid

focus_by_rid = {}
focus_by_suffix = {}
for row in focus_rows:
    rid = row['ResourceId']
    suffix = extract_suffix(rid)
    entry = focus_by_rid.setdefault(rid, {
        'ResourceId': rid, 'ServiceName': row['ServiceName'],
        'ServiceProviderName': row['ServiceProviderName'],
        'ResourceType': row.get('ResourceType', ''), 'ModelName': row.get('ModelName', ''),
        'AmortizedCost_KRW_total': 0.0,
        'GpuUtil_sum': 0.0, 'GpuUtil_count': 0, 'row_count': 0
    })
    try:
        entry['AmortizedCost_KRW_total'] += float(row['AmortizedCost_KRW'] or 0)
    except:
        pass
    try:
        gu = row.get('GpuUtilization', '').strip()
        if gu:
            entry['GpuUtil_sum'] += float(gu)
            entry['GpuUtil_count'] += 1
    except:
        pass
    entry['row_count'] += 1
    focus_by_suffix[suffix] = entry

def get_focus(util_rid):
    if util_rid in focus_by_rid:
        return focus_by_rid[util_rid]
    s = extract_suffix(util_rid)
    return focus_by_suffix.get(s)

util_agg = {}
for row in util_rows:
    rid = row['resource_id']
    if rid not in util_agg:
        util_agg[rid] = {
            'cpu_vals': [], 'mem_vals': [],
            'instance_type': row.get('instance_type', ''),
            'provider': row.get('provider', ''),
            'project': row.get('project', ''),
            'environment': row.get('environment', ''),
            'status': row.get('status', 'running')
        }
    try:
        util_agg[rid]['cpu_vals'].append(float(row['avg_cpu_percent']))
    except:
        pass
    try:
        util_agg[rid]['mem_vals'].append(float(row['avg_memory_percent']))
    except:
        pass

IDLE = []
for rid, d in util_agg.items():
    days = len(d['cpu_vals'])
    if days < 14:
        continue
    cpu_avg = sum(d['cpu_vals']) / days
    mem_avg = sum(d['mem_vals']) / days if d['mem_vals'] else 0.0
    idle_types = []
    if cpu_avg < 40.0:
        idle_types.append('CPU유휴')
    if mem_avg < 60.0:
        idle_types.append('MEM유휴')
    fm = get_focus(rid)
    gpu_avg = None
    if fm and fm['GpuUtil_count'] > 0:
        gpu_avg = fm['GpuUtil_sum'] / fm['GpuUtil_count']
        if gpu_avg < 60.0:
            idle_types.append('GPU저활용')
    if not idle_types:
        continue
    csp = fm['ServiceProviderName'] if fm else d['provider']
    service = fm['ServiceName'] if fm else 'N/A'
    daily_cost = (fm['AmortizedCost_KRW_total'] / 31) if fm else 0.0
    IDLE.append({
        'rid': rid, 'csp': csp, 'service': service,
        'instance_type': d['instance_type'],
        'avg_cpu': round(cpu_avg, 1), 'avg_mem': round(mem_avg, 1),
        'avg_gpu': round(gpu_avg, 1) if gpu_avg is not None else None,
        'daily_cost_krw': round(daily_cost),
        'monthly_cost_krw': round(daily_cost * 30),
        'idle_types': idle_types, 'days': days,
        'project': d['project'], 'environment': d['environment'],
        'status': d['status']
    })

IDLE.sort(key=lambda x: x['monthly_cost_krw'], reverse=True)

CSP_SHORT = {
    'Amazon Web Services': 'AWS', 'Microsoft Azure': 'Azure',
    'Google Cloud Platform': 'GCP', 'Google Cloud': 'GCP',
    'Anthropic': 'Anthropic', 'OpenAI': 'OpenAI'
}

def csp_short(name):
    return CSP_SHORT.get(name, name)

def short_rid(rid):
    if '/virtualMachines/' in rid:
        return rid.split('/virtualMachines/')[-1]
    if '/instances/' in rid:
        return rid.split('/instances/')[-1]
    return rid.split('/')[-1] if '/' in rid else rid

DOWNSIZE_MAP = {
    'm5.4xlarge':      {'d1': 'm5.2xlarge',      'd2': 'm5.xlarge',       'r_d1': 0.50, 'r_d2': 0.75},
    'm5.2xlarge':      {'d1': 'm5.xlarge',        'd2': 'm5.large',        'r_d1': 0.50, 'r_d2': 0.75},
    'm5.xlarge':       {'d1': 'm5.large',         'd2': 'm5.medium',       'r_d1': 0.50, 'r_d2': 0.75},
    'm5.large':        {'d1': 'm5.medium',        'd2': 'm5.small',        'r_d1': 0.50, 'r_d2': 0.75},
    'c5.2xlarge':      {'d1': 'c5.xlarge',        'd2': 'c5.large',        'r_d1': 0.50, 'r_d2': 0.75},
    'Standard_D8s_v3': {'d1': 'Standard_D4s_v3', 'd2': 'Standard_D2s_v3', 'r_d1': 0.50, 'r_d2': 0.75},
    'Standard_D4s_v3': {'d1': 'Standard_D2s_v3', 'd2': 'Standard_B2ms',   'r_d1': 0.50, 'r_d2': 0.65},
    'Standard_D2s_v3': {'d1': 'Standard_B2s',    'd2': 'Standard_B2ms',   'r_d1': 0.40, 'r_d2': 0.50},
    'n2-standard-8':   {'d1': 'n2-standard-4',   'd2': 'n2-standard-2',   'r_d1': 0.50, 'r_d2': 0.75},
    'n2-standard-4':   {'d1': 'n2-standard-2',   'd2': 'e2-medium',       'r_d1': 0.50, 'r_d2': 0.65},
}

MEM_OPT_MAP = {
    'm5.2xlarge':      {'opt': 'r5.xlarge',         'note': 'CPU 유지, MEM 최적화 (r5 계열)', 'r': 0.20},
    'c5.2xlarge':      {'opt': 'c5.xlarge',          'note': 'MEM 절감, CPU 유지',             'r': 0.20},
    'Standard_D4s_v3': {'opt': 'Standard_B4ms',     'note': 'Burstable — CPU 유지, 비용 절감','r': 0.25},
    'Standard_D2s_v3': {'opt': 'Standard_B2s',      'note': 'Burstable — CPU 유지, 비용 절감','r': 0.25},
    'n2-standard-4':   {'opt': 'n2d-standard-4',    'note': 'AMD 기반, 동급 CPU, 약 20% 절감', 'r': 0.20},
}

def get_recommendation(r):
    if r['avg_cpu'] >= 50 and set(r['idle_types']) == {'MEM유휴'}:
        opt = MEM_OPT_MAP.get(r['instance_type'])
        if opt:
            return 'mem_opt', opt['opt'], opt['note'], opt['r']
        return 'mem_opt', None, 'MEM 최적화 타입 검토 필요', 0.20
    return 'downsize', None, None, 0.0

def get_risk(cpu, level, rec_type):
    if rec_type == 'terminate':
        return 'Low' if cpu == 0.0 else 'High'
    if rec_type == 'mem_opt':
        if level == 'd1':
            return 'Medium'
        return 'Medium'
    if level == 'd1':
        if cpu >= 50:
            return 'High'
        if cpu >= 30:
            return 'Medium'
        return 'Low'
    if level == 'd2':
        if cpu >= 50:
            return 'Very High'
        if cpu >= 20:
            return 'High'
        return 'Medium'
    return 'Medium'

AI_RESOURCES = []
for rid, fm in focus_by_rid.items():
    if fm['ModelName'].strip():
        daily = fm['AmortizedCost_KRW_total'] / 31
        gpu_avg = fm['GpuUtil_sum'] / fm['GpuUtil_count'] if fm['GpuUtil_count'] > 0 else None
        AI_RESOURCES.append({
            'rid': rid, 'model': fm['ModelName'],
            'provider': fm['ServiceProviderName'],
            'service': fm['ServiceName'],
            'daily_cost': round(daily),
            'monthly_cost': round(daily * 30),
            'gpu_avg': round(gpu_avg, 1) if gpu_avg is not None else None
        })

AI_MODEL_ALTS = {
    'claude-3-5-sonnet': {
        'altA': ('claude-3-haiku', 0.95, 'Low'),
        'altB': ('gpt-4o-mini', 0.90, 'Low'),
        'altC': ('claude-3-haiku + 프롬프트 캐싱', 0.97, 'Low'),
        'period': '즉시 (1~2주 A/B 테스트 권고)'
    },
    'Vertex AI': {
        'altA': ('Vertex AI gemini-1.5-flash', 0.60, 'Medium'),
        'altB': ('Vertex AI gemini-1.5-flash-8b', 0.75, 'Low'),
        'altC': ('Vertex AI 배치 예측 API', 0.65, 'Low'),
        'period': '2~4주 (파이프라인 수정 필요)'
    }
}

total_d1 = 0
total_d2 = 0
total_terminate = 0
compute_rows = []

for r in IDLE:
    itype = r['instance_type']
    mcost = r['monthly_cost_krw']
    rec_type, opt_type, opt_note, mem_r = get_recommendation(r)
    dm = DOWNSIZE_MAP.get(itype, {})
    is_complete_idle = (r['avg_cpu'] == 0.0 and r['avg_mem'] == 0.0)

    if rec_type == 'mem_opt':
        save_d1 = round(mcost * mem_r)
        save_d2 = round(mcost * (mem_r + 0.10))
        d1_label = opt_type or 'MEM최적화타입'
        d2_label = opt_type or 'MEM최적화타입'
        note_tag = '[MEM최적화]'
    else:
        save_d1 = round(mcost * dm.get('r_d1', 0.50)) if dm else 0
        save_d2 = round(mcost * dm.get('r_d2', 0.75)) if dm else 0
        d1_label = dm.get('d1', 'N/A') if dm else 'N/A'
        d2_label = dm.get('d2', 'N/A') if dm else 'N/A'
        note_tag = ''

    save_terminate = mcost if is_complete_idle else round(mcost * 0.90)
    risk_d1 = get_risk(r['avg_cpu'], 'd1', rec_type)
    risk_d2 = get_risk(r['avg_cpu'], 'd2', rec_type)
    risk_term = get_risk(r['avg_cpu'], 'terminate', 'terminate')

    total_d1 += save_d1
    total_d2 += save_d2
    total_terminate += save_terminate

    compute_rows.append({
        'rid': short_rid(r['rid']),
        'csp': csp_short(r['csp']),
        'itype': itype,
        'avg_cpu': r['avg_cpu'],
        'avg_mem': r['avg_mem'],
        'd1_label': d1_label,
        'd2_label': d2_label,
        'save_d1': save_d1,
        'save_d2': save_d2,
        'save_terminate': save_terminate,
        'risk_d1': risk_d1,
        'risk_d2': risk_d2,
        'risk_term': risk_term,
        'mcost': mcost,
        'is_terminate': is_complete_idle,
        'rec_type': rec_type,
        'note_tag': note_tag
    })

ai_total_d1 = 0
ai_total_d2 = 0
ai_total_d3 = 0
ai_model_rows = []
for a in AI_RESOURCES:
    model = a['model']
    mcost = a['monthly_cost']
    alts = AI_MODEL_ALTS.get(model, {
        'altA': (model + '-mini', 0.60, 'Medium'),
        'altB': (model + '-lite', 0.75, 'Low'),
        'altC': (model + '-lite+캐싱', 0.80, 'Low'),
        'period': '2~4주'
    })
    save_a = round(mcost * alts['altA'][1])
    save_b = round(mcost * alts['altB'][1])
    save_c = round(mcost * alts['altC'][1])
    ai_total_d1 += save_a
    ai_total_d2 += save_b
    ai_total_d3 += save_c
    ai_model_rows.append({
        'model': model, 'provider': csp_short(a['provider']), 'mcost': mcost,
        'altA_name': alts['altA'][0], 'save_a': save_a, 'risk_a': alts['altA'][2],
        'altB_name': alts['altB'][0], 'save_b': save_b, 'risk_b': alts['altB'][2],
        'altC_name': alts['altC'][0], 'save_c': save_c, 'risk_c': alts['altC'][2],
        'period': alts['period']
    })

grand_total_d1 = total_d1 + ai_total_d1
grand_total_d2 = total_d2 + ai_total_d2
grand_total_d3 = total_terminate + ai_total_d3

# =========================================================
# [3] out/rightsize-plan.md
# =========================================================
L = []
L.append("# Right-sizing 권고 계획서\n")
L.append("- 분석 기준일: 2026-04-19  ")
L.append("- 데이터 기간: 2026-03-01 ~ 2026-03-31 (31일)  ")
L.append("- 대상 리소스: 컴퓨트 유휴 28건 + AI 모델 2건  ")
L.append("- 리스크 분류 기준: CPU >= 50% 리소스는 Downsize 시 High/Very High로 상향 적용; MEM유휴 단독 시 MEM 최적화 타입 교체 권고\n")
L.append("## 총 예상 절감액 요약\n")
L.append("| 대안 | 컴퓨트 절감(KRW/월) | AI 모델 절감(KRW/월) | 합계(KRW/월) | 주요 리스크 |")
L.append("|------|---------------------|---------------------|-------------|-----------|")
L.append(f"| Downsize-1단+MEM최적화 + AI대안A | {total_d1:,} | {ai_total_d1:,} | **{grand_total_d1:,}** | Low~High (리소스별 상이) |")
L.append(f"| Downsize-2단 + AI대안B | {total_d2:,} | {ai_total_d2:,} | **{grand_total_d2:,}** | Medium~Very High |")
L.append(f"| Terminate + AI대안C | {total_terminate:,} | {ai_total_d3:,} | **{grand_total_d3:,}** | Low(완전유휴)/High(과잉) |")
L.append("\n---\n")
L.append("## 컴퓨트 Right-sizing\n")
L.append("### 판정 기준 및 리스크 분류\n")
L.append("- CPU 2주 평균 < 40% AND/OR Memory 2주 평균 < 60%로 유휴 판정  ")
L.append("- **CPU >= 50% + MEM유휴 단독**: Downsize 금지 — 메모리 최적화 인스턴스 타입 교체 권고  ")
L.append("  (Downsize 시 CPU 포화 위험; r5/B-시리즈/n2d 등 동급 CPU 저비용 타입으로 교체)  ")
L.append("- **CPU 30~50%**: Downsize-1단 리스크 Medium  ")
L.append("- **CPU < 30%**: Downsize-1단 리스크 Low  ")
L.append("- Terminate: 완전유휴(CPU=0%·MEM=0%) Low, 과잉프로비전 High\n")
L.append("### 3대안 비교표\n")
L.append("| 리소스 ID | CSP | 현재 유형 | CPU% | MEM% | 대안A | 대안B | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(Terminate,KRW/월) | 리스크A | 리스크B | 리스크C |")
L.append("|-----------|-----|----------|------|------|-------|-------|--------------|--------------|------------------------|--------|--------|--------|")
for cr in compute_rows:
    note_s = cr['note_tag'] + ' ' if cr['note_tag'] else ''
    L.append(f"| {cr['rid']} | {cr['csp']} | {cr['itype']} | {cr['avg_cpu']} | {cr['avg_mem']} | {note_s}{cr['d1_label']} | {cr['d2_label']} | {cr['save_d1']:,} | {cr['save_d2']:,} | {cr['save_terminate']:,} | {cr['risk_d1']} | {cr['risk_d2']} | {cr['risk_term']} |")
L.append(f"\n**컴퓨트 소계**: 대안A {total_d1:,}KRW/월 | 대안B {total_d2:,}KRW/월 | 대안C(Terminate) {total_terminate:,}KRW/월\n")
L.append("### 대안 상세 설명\n")
L.append("#### 대안A — Downsize-1단 / MEM 최적화 타입 교체\n")
L.append("- CPU < 50%: 인스턴스 한 단계 축소 (예: m5.4xlarge → m5.2xlarge, D8s_v3 → D4s_v3)  ")
L.append("- CPU >= 50% MEM유휴 단독: 메모리 최적화 타입 교체  ")
L.append("  - AWS: r5 계열 (메모리 집약형, CPU 동일 수준 유지)  ")
L.append("  - Azure: Standard_B 계열 (Burstable, 유휴 시 크레딧 축적으로 스파이크 대응)  ")
L.append("  - GCP: n2d 계열 (AMD EPYC, 동급 CPU 약 20% 저렴)  ")
L.append("- SLA 리스크: Low(CPU<30%) / Medium(CPU 30~50%) / High(CPU>=50% Downsize 시도 금지)  ")
L.append("- 구현 복잡도: Low — 인스턴스 중지 후 유형 변경 (10~30분 다운타임)  ")
L.append("- 적용 기간: 1~2주 내\n")
L.append("#### 대안B — Downsize-2단\n")
L.append("- CPU < 30% 리소스에 한해 권고 (CPU >= 30%는 Very High 리스크, 적용 비권고)  ")
L.append("- 절감률: 약 65~75%  ")
L.append("- SLA 리스크: High~Very High (피크 트래픽 대응 능력 현저 감소)  ")
L.append("- 구현 복잡도: Medium — Auto Scaling 정책 동시 조정 필수  ")
L.append("- 적용 기간: 2~4주 (성능 테스트 선행 필수)\n")
L.append("#### 대안C — Terminate\n")
L.append("- 완전 유휴(CPU=0%·MEM=0%, 31일 연속): i-idle-001, i-idle-002 즉시 종료 권고  ")
L.append("- 과잉 프로비저닝: 14일 추가 모니터링 + 담당팀 승인 후 진행  ")
L.append("- SLA 리스크: Low(완전유휴) / High(과잉프로비전)  ")
L.append("- 적용 기간: 완전유휴 즉시 / 과잉프로비전 4~8주\n")
L.append("---\n")
L.append("## AI 모델 최적화\n")
L.append("### 모델 다운그레이드 3종 대안\n")
L.append("| 현재 모델 | 제공사 | 월비용(KRW) | 대안A(보수적) | 대안B(균형) | 대안C(최적화) | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(KRW/월) | 품질리스크A | 품질리스크B | 품질리스크C | 적용기간 |")
L.append("|----------|--------|------------|---------------|-------------|---------------|--------------|--------------|--------------|-----------|-----------|-----------|---------|")
for am in ai_model_rows:
    L.append(f"| {am['model']} | {am['provider']} | {am['mcost']:,} | {am['altA_name']} | {am['altB_name']} | {am['altC_name']} | {am['save_a']:,} | {am['save_b']:,} | {am['save_c']:,} | {am['risk_a']} | {am['risk_b']} | {am['risk_c']} | {am['period']} |")
L.append(f"\n**AI 모델 소계**: 대안A {ai_total_d1:,}KRW/월 | 대안B {ai_total_d2:,}KRW/월 | 대안C {ai_total_d3:,}KRW/월\n")
L.append("### AI 대안 상세 설명\n")
L.append("#### 대안A — 보수적 (동일 제공사 소형 모델)\n")
L.append("- claude-3-5-sonnet → claude-3-haiku: API 호환 100%, 입력 토큰 단가 약 95% 절감  ")
L.append("- Vertex AI → gemini-1.5-flash: 동일 GCP 인프라, 마이그레이션 공수 최소  ")
L.append("- 품질 리스크: Low — 일반 텍스트 처리 태스크 품질 차이 미미  ")
L.append("- 적용 기간: 즉시 (1~2주 A/B 테스트 권고)\n")
L.append("#### 대안B — 균형 (타사 동급 경량 모델)\n")
L.append("- claude-3-5-sonnet → gpt-4o-mini: 프롬프트 일부 수정 필요  ")
L.append("- Vertex AI → gemini-1.5-flash-8b: 단순 분류/요약 태스크 적합  ")
L.append("- 품질 리스크: Low~Medium — 복잡한 추론 태스크 품질 차이 가능  ")
L.append("- 적용 기간: 2~4주\n")
L.append("#### 대안C — 최적화 (경량 모델 + 캐싱/배치)\n")
L.append("- claude-3-haiku + 프롬프트 캐싱: 캐시 히트 시 입력 토큰 90% 절감  ")
L.append("- Vertex AI 배치 예측 API: 비동기 처리로 실시간 API 대비 최대 50% 절감  ")
L.append("- 품질 리스크: Low — 동일 모델, 캐싱 추가만  ")
L.append("- 적용 기간: 즉시\n")
L.append("---\n")
L.append("## 실행 우선순위 로드맵\n")
L.append("### 즉시 실행 (0~2주) — Low 리스크, 빠른 절감 효과\n")
L.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
L.append("|---------|--------|------|-----------------|-------|")
L.append("| P1 | i-idle-001, i-idle-002 | Terminate | 0 (연결 리소스 정리 효과) | Low |")
ai_c0 = ai_model_rows[0]['save_c'] if ai_model_rows else 0
L.append(f"| P2 | claude-3-5-sonnet | 대안C (캐싱 활성화) | {ai_c0:,} | Low |")
L.append(f"| P3 | vm-overprov-001,002,003 (D8s->D4s) | Downsize-1단 | {round(2612903*0.5*3):,} | Low |")
L.append(f"| P4 | i-overprov-001~005 (m5.4xl->m5.2xl) | Downsize-1단 | {round(829440*0.5*5):,} | Low |")
L.append(f"| P5 | gce-overprov-002~005 (n2-std-8->4) | Downsize-1단 | {round(311040*0.5*4):,} | Low |")
L.append("")
L.append("### 단기 실행 (2~4주) — 테스트 선행 필요\n")
L.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
L.append("|---------|--------|------|-----------------|-------|")
ai_a0 = ai_model_rows[0]['save_a'] if ai_model_rows else 0
L.append(f"| P6 | claude-3-5-sonnet | 대안A (claude-3-haiku) | {ai_a0:,} | Low |")
L.append(f"| P7 | vm-spike-azure (D4s->B4ms) | MEM 최적화 타입 교체 | {round(1393548*0.25):,} | Medium |")
L.append(f"| P8 | vm-api-001 (D4s->B4ms) | MEM 최적화 타입 교체 | {round(1306452*0.25):,} | Medium |")
L.append("")
L.append("### 중기 실행 (4~8주) — 의존성 분석 선행 필요\n")
L.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
L.append("|---------|--------|------|-----------------|-------|")
ai_b1 = ai_model_rows[1]['save_b'] if len(ai_model_rows) > 1 else 0
L.append(f"| P9 | Vertex AI trainingPipelines | 대안B (gemini-1.5-flash-8b) | {ai_b1:,} | Low |")
L.append(f"| P10 | gce-web/api 시리즈 (n2d-standard-4) | MEM 최적화 타입 교체 | {round(209070*0.20*4):,} | Medium |")
L.append(f"| P11 | i-web-001~003, i-spike-001 | MEM 최적화 타입 교체 | {round((414720*3+574839)*0.20):,} | Medium |")
L.append("")
L.append("## 전체 예상 절감 합계\n")
L.append(f"- **대안A 시나리오 (Downsize-1단+MEM최적화+AI대안A)**: {grand_total_d1:,}KRW/월 ({grand_total_d1*12:,}KRW/년)  ")
L.append(f"- **대안B 시나리오 (Downsize-2단+AI대안B)**: {grand_total_d2:,}KRW/월 ({grand_total_d2*12:,}KRW/년)  ")
L.append(f"- **대안C 시나리오 (Terminate+AI대안C)**: {grand_total_d3:,}KRW/월 ({grand_total_d3*12:,}KRW/년)  ")
L.append(f"\n> 권고 최적안: **대안A** — {grand_total_d1:,}KRW/월, CPU>=50% 리소스 장애 위험 배제, P1~P5 실행 시 4주 내 효과 가시화  ")

os.makedirs('out', exist_ok=True)
with open('out/rightsize-plan.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(L))

print("[3] out/rightsize-plan.md 수정 완료 (리스크 재분류 반영)")
print(f"    대안A: {grand_total_d1:,}KRW/월")
print(f"    대안B: {grand_total_d2:,}KRW/월")
print(f"    대안C: {grand_total_d3:,}KRW/월")
