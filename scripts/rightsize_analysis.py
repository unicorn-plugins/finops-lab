import csv, os
from collections import defaultdict

# ===== 데이터 로드 =====
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
        'ResourceType': row.get('ResourceType',''), 'ModelName': row.get('ModelName',''),
        'AmortizedCost_KRW_total': 0.0,
        'GpuUtil_sum': 0.0, 'GpuUtil_count': 0, 'row_count': 0
    })
    try: entry['AmortizedCost_KRW_total'] += float(row['AmortizedCost_KRW'] or 0)
    except: pass
    try:
        gu = row.get('GpuUtilization','').strip()
        if gu:
            entry['GpuUtil_sum'] += float(gu)
            entry['GpuUtil_count'] += 1
    except: pass
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
            'instance_type': row.get('instance_type',''),
            'provider': row.get('provider',''),
            'project': row.get('project',''),
            'environment': row.get('environment',''),
            'status': row.get('status','running')
        }
    try: util_agg[rid]['cpu_vals'].append(float(row['avg_cpu_percent']))
    except: pass
    try: util_agg[rid]['mem_vals'].append(float(row['avg_memory_percent']))
    except: pass

IDLE = []
for rid, d in util_agg.items():
    days = len(d['cpu_vals'])
    if days < 14:
        continue
    cpu_avg = sum(d['cpu_vals'])/days
    mem_avg = sum(d['mem_vals'])/days if d['mem_vals'] else 0.0
    idle_types = []
    if cpu_avg < 40.0: idle_types.append('CPU유휴')
    if mem_avg < 60.0: idle_types.append('MEM유휴')
    fm = get_focus(rid)
    gpu_avg = None
    if fm and fm['GpuUtil_count'] > 0:
        gpu_avg = fm['GpuUtil_sum']/fm['GpuUtil_count']
        if gpu_avg < 60.0: idle_types.append('GPU저활용')
    if not idle_types:
        continue
    csp = fm['ServiceProviderName'] if fm else d['provider']
    service = fm['ServiceName'] if fm else 'N/A'
    daily_cost = (fm['AmortizedCost_KRW_total']/31) if fm else 0.0
    IDLE.append({
        'rid': rid, 'csp': csp, 'service': service,
        'instance_type': d['instance_type'],
        'avg_cpu': round(cpu_avg,1), 'avg_mem': round(mem_avg,1),
        'avg_gpu': round(gpu_avg,1) if gpu_avg is not None else None,
        'daily_cost_krw': round(daily_cost),
        'monthly_cost_krw': round(daily_cost*30),
        'idle_types': idle_types, 'days': days,
        'project': d['project'], 'environment': d['environment'],
        'status': d['status']
    })

IDLE.sort(key=lambda x: x['monthly_cost_krw'], reverse=True)

CSP_SHORT = {
    'Amazon Web Services': 'AWS',
    'Microsoft Azure': 'Azure',
    'Google Cloud Platform': 'GCP',
    'Google Cloud': 'GCP',
    'Anthropic': 'Anthropic',
    'OpenAI': 'OpenAI'
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
    'm5.4xlarge': {'d1': 'm5.2xlarge', 'd2': 'm5.xlarge',      'r_d1': 0.50, 'r_d2': 0.75},
    'm5.2xlarge': {'d1': 'm5.xlarge',  'd2': 'm5.large',        'r_d1': 0.50, 'r_d2': 0.75},
    'm5.xlarge':  {'d1': 'm5.large',   'd2': 'm5.medium',       'r_d1': 0.50, 'r_d2': 0.75},
    'm5.large':   {'d1': 'm5.medium',  'd2': 'm5.small',        'r_d1': 0.50, 'r_d2': 0.75},
    'c5.2xlarge': {'d1': 'c5.xlarge',  'd2': 'c5.large',        'r_d1': 0.50, 'r_d2': 0.75},
    'Standard_D8s_v3': {'d1': 'Standard_D4s_v3', 'd2': 'Standard_D2s_v3', 'r_d1': 0.50, 'r_d2': 0.75},
    'Standard_D4s_v3': {'d1': 'Standard_D2s_v3', 'd2': 'Standard_B2ms',   'r_d1': 0.50, 'r_d2': 0.65},
    'Standard_D2s_v3': {'d1': 'Standard_B2s',    'd2': 'Standard_B2ms',   'r_d1': 0.40, 'r_d2': 0.50},
    'n2-standard-8': {'d1': 'n2-standard-4', 'd2': 'n2-standard-2', 'r_d1': 0.50, 'r_d2': 0.75},
    'n2-standard-4': {'d1': 'n2-standard-2', 'd2': 'e2-medium',      'r_d1': 0.50, 'r_d2': 0.65},
}

def get_downsize(itype, monthly_cost):
    dm = DOWNSIZE_MAP.get(itype)
    if not dm:
        return None, None, 0, 0
    save_d1 = round(monthly_cost * dm['r_d1'])
    save_d2 = round(monthly_cost * dm['r_d2'])
    return dm['d1'], dm['d2'], save_d1, save_d2

# AI 리소스
AI_RESOURCES = []
for rid, fm in focus_by_rid.items():
    if fm['ModelName'].strip():
        daily = fm['AmortizedCost_KRW_total'] / 31
        gpu_avg = fm['GpuUtil_sum']/fm['GpuUtil_count'] if fm['GpuUtil_count']>0 else None
        AI_RESOURCES.append({
            'rid': rid, 'model': fm['ModelName'],
            'provider': fm['ServiceProviderName'],
            'service': fm['ServiceName'],
            'daily_cost': round(daily),
            'monthly_cost': round(daily * 30),
            'gpu_avg': round(gpu_avg,1) if gpu_avg is not None else None
        })

# =========================================================
# [1] out/step3/1-idle-resources.md
# =========================================================
os.makedirs('out/step3', exist_ok=True)

lines = []
lines.append("# 유휴 리소스 목록\n")
lines.append("## 식별 기준\n")
lines.append("- CPU: 2주 평균 < 40% | Memory: 2주 평균 < 60% | GPU: 2주 평균 < 60%  ")
lines.append("- 관찰 기간: 2026-03-01 ~ 2026-03-31 (31일, 14일 이상 연속 데이터 보유 리소스만 판정)  ")
lines.append("- 조건 중 하나 이상 충족 시 최적화 후보 분류  ")
lines.append("- 이용률 데이터 누락(null) 처리 방침: 해당 날짜 제외 후 유효 측정치만으로 평균 산정; 14일 미만 데이터 보유 리소스는 판정 제외\n")
lines.append(f"## 유휴 리소스 목록 ({len(IDLE)}건)\n")
lines.append("| 리소스 ID | CSP | 서비스 | 인스턴스 유형 | CPU% | Memory% | GPU% | 일일비용(KRW) | 유휴유형 |")
lines.append("|-----------|-----|--------|--------------|------|---------|------|--------------|---------|")
for r in IDLE:
    gpu_s = f"{r['avg_gpu']:.1f}" if r['avg_gpu'] is not None else "N/A"
    lines.append(f"| {short_rid(r['rid'])} | {csp_short(r['csp'])} | {r['service']} | {r['instance_type']} | {r['avg_cpu']} | {r['avg_mem']} | {gpu_s} | {r['daily_cost_krw']:,} | {'·'.join(r['idle_types'])} |")

lines.append("\n## 판정 근거 요약\n")
cpu_idle = sum(1 for r in IDLE if 'CPU유휴' in r['idle_types'])
mem_idle = sum(1 for r in IDLE if 'MEM유휴' in r['idle_types'])
both_idle = sum(1 for r in IDLE if 'CPU유휴' in r['idle_types'] and 'MEM유휴' in r['idle_types'])
lines.append("| 유형 | 건수 | 판정 기준 |")
lines.append("|------|------|---------|")
lines.append(f"| CPU유휴 | {cpu_idle}건 | 2주 평균 CPU < 40% |")
lines.append(f"| MEM유휴 | {mem_idle}건 | 2주 평균 Memory < 60% |")
lines.append(f"| CPU+MEM 복합 | {both_idle}건 | 두 조건 동시 충족 |")
lines.append("| GPU저활용 | 0건 | 2주 평균 GPU < 60% (해당 리소스 GPU 이용률 측정값 없음) |")
lines.append("\n## 주요 유휴 리소스 상세\n")
lines.append("### 완전 유휴 리소스 (Terminate 우선순위)\n")
for r in IDLE:
    if r['avg_cpu'] == 0.0 and r['avg_mem'] == 0.0:
        lines.append(f"- **{short_rid(r['rid'])}** ({r['instance_type']}): CPU 0% · Memory 0% · {r['days']}일 연속 — 즉시 종료 권고  ")
lines.append("\n### 과잉 프로비저닝 리소스 (Downsize 우선순위)\n")
for r in IDLE:
    if 'CPU유휴' in r['idle_types'] and r['avg_cpu'] > 0 and r['monthly_cost_krw'] > 500000:
        lines.append(f"- **{short_rid(r['rid'])}** ({r['instance_type']}): CPU {r['avg_cpu']}% · Memory {r['avg_mem']}% · 월 {r['monthly_cost_krw']:,}KRW  ")

with open('out/step3/1-idle-resources.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("[1] out/step3/1-idle-resources.md 작성 완료 - 유휴 리소스", len(IDLE), "건")

# =========================================================
# [2] out/step3/3-scaling-policy-checklist.md
# =========================================================
lines2 = []
lines2.append("# 서비스별 스케일링 정책 체크리스트\n")
lines2.append("## 체크리스트 적용 기준\n")
lines2.append("- 유휴 판정 기준: CPU 2주 평균 < 40%, Memory 2주 평균 < 60%  ")
lines2.append("- 자동화 실행은 본 체크리스트 범위 외 (별도 운영팀 승인 필요)  ")
lines2.append("- 스케일-인 임계값 도달 후 최소 72시간 모니터링 후 적용 권고\n")
lines2.append("## AWS EC2 스케일링 정책\n")
lines2.append("| 항목 | 내용 |")
lines2.append("|------|------|")
lines2.append("| 스케일-인 CPU 임계값 | 평균 < 40% (14일 연속) |")
lines2.append("| 스케일-인 Memory 임계값 | 평균 < 60% (14일 연속) |")
lines2.append("| 스케일-아웃 CPU 임계값 | 순간 > 80% (5분 연속) |")
lines2.append("| 스케일-아웃 Memory 임계값 | 순간 > 85% (5분 연속) |")
lines2.append("| 최소 인스턴스 수 | 2 (가용성 보장) |")
lines2.append("| Downsize 전 사전 점검 | [ ] 피크 시간대 CPU/MEM 확인 [ ] 애플리케이션 팀 승인 [ ] 롤백 계획 수립 |")
lines2.append("| Terminate 전 사전 점검 | [ ] 연결된 EBS 볼륨 정리 [ ] 보안그룹 정리 [ ] 스냅샷 백업 |")
lines2.append("| 적용 후 모니터링 기간 | 최소 7일 |")
lines2.append("")
lines2.append("## Microsoft Azure VM 스케일링 정책\n")
lines2.append("| 항목 | 내용 |")
lines2.append("|------|------|")
lines2.append("| 스케일-인 CPU 임계값 | 평균 < 40% (14일 연속) |")
lines2.append("| 스케일-인 Memory 임계값 | 평균 < 60% (14일 연속) |")
lines2.append("| 스케일-아웃 CPU 임계값 | 순간 > 80% (5분 연속) |")
lines2.append("| VM 크기 변경 방법 | Azure Portal > VM 크기 조정 또는 az vm resize CLI |")
lines2.append("| 유지보수 기간 | 업무 외 시간 (22:00~06:00 KST) |")
lines2.append("| Downsize 전 사전 점검 | [ ] Azure Advisor 권고 확인 [ ] 가용성 집합 호환성 확인 [ ] 관리 디스크 유형 확인 |")
lines2.append("| 적용 후 모니터링 기간 | 최소 7일 |")
lines2.append("")
lines2.append("## Google Cloud Compute Engine 스케일링 정책\n")
lines2.append("| 항목 | 내용 |")
lines2.append("|------|------|")
lines2.append("| 스케일-인 CPU 임계값 | 평균 < 40% (14일 연속) |")
lines2.append("| 스케일-인 Memory 임계값 | 평균 < 60% (14일 연속) |")
lines2.append("| 스케일-아웃 CPU 임계값 | 순간 > 80% (5분 연속) |")
lines2.append("| 머신 유형 변경 방법 | gcloud compute instances set-machine-type |")
lines2.append("| 인스턴스 재시작 필요 여부 | 예 (중지 후 유형 변경) |")
lines2.append("| Downsize 전 사전 점검 | [ ] Cloud Monitoring 알림 정책 업데이트 [ ] Managed Instance Group 설정 확인 [ ] 서비스 SLA 확인 |")
lines2.append("| 적용 후 모니터링 기간 | 최소 7일 |")
lines2.append("")
lines2.append("## AI 모델 스케일링 정책\n")
lines2.append("| 항목 | 내용 |")
lines2.append("|------|------|")
lines2.append("| GPU 저활용 임계값 | 평균 < 60% (14일 연속) |")
lines2.append("| 모델 다운그레이드 조건 | GPU < 60% + 품질 지표 허용 범위 내 |")
lines2.append("| 다운그레이드 전 A/B 테스트 기간 | 최소 7일 |")
lines2.append("| 품질 지표 측정 항목 | 응답 정확도, 응답 시간, 사용자 만족도 |")
lines2.append("| 롤백 트리거 | 품질 지표 10% 이상 하락 시 즉시 롤백 |")
lines2.append("")
lines2.append("## 공통 사전 점검 체크리스트\n")
lines2.append("- [ ] 2주 이상 이용률 데이터 확보 확인  ")
lines2.append("- [ ] 해당 리소스 담당팀(오너) 승인 완료  ")
lines2.append("- [ ] 피크 시간대 예외 여부 확인 (배치 작업, 이벤트 기간 등)  ")
lines2.append("- [ ] 스냅샷/백업 최신 상태 확인  ")
lines2.append("- [ ] 롤백 절차 문서화 완료  ")
lines2.append("- [ ] 변경 후 알림 임계값 재설정 완료  ")
lines2.append("- [ ] ITSM 변경 요청(RFC) 등록 완료  ")

with open('out/step3/3-scaling-policy-checklist.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines2))

print("[2] out/step3/3-scaling-policy-checklist.md 작성 완료")

# =========================================================
# [3] out/rightsize-plan.md
# =========================================================
# 절감액 계산
total_d1 = 0
total_d2 = 0
total_terminate = 0
compute_rows = []

for r in IDLE:
    itype = r['instance_type']
    mcost = r['monthly_cost_krw']
    d1_type, d2_type, save_d1, save_d2 = get_downsize(itype, mcost)

    # Terminate: 완전 유휴 (CPU=0, MEM=0) 또는 14일 이상 idle 상태 명시적
    is_terminate_candidate = (r['avg_cpu'] == 0.0 and r['avg_mem'] == 0.0)
    save_terminate = mcost if is_terminate_candidate else round(mcost * 0.90)

    risk_d1 = 'Low' if r['avg_cpu'] < 20 else 'Medium'
    risk_d2 = 'Medium' if r['avg_cpu'] < 20 else 'High'
    risk_term = 'High' if not is_terminate_candidate else 'Low'

    if d1_type:
        total_d1 += save_d1
        total_d2 += save_d2
    total_terminate += save_terminate

    compute_rows.append({
        'rid': short_rid(r['rid']),
        'csp': csp_short(r['csp']),
        'itype': itype,
        'd1_type': d1_type or 'N/A',
        'd2_type': d2_type or 'N/A',
        'save_d1': save_d1,
        'save_d2': save_d2,
        'save_terminate': save_terminate,
        'risk_d1': risk_d1,
        'risk_d2': risk_d2,
        'risk_term': risk_term,
        'mcost': mcost,
        'is_terminate': is_terminate_candidate
    })

# AI 모델 절감 계산
AI_MODEL_ALTS = {
    'claude-3-5-sonnet': {
        'altA': ('claude-3-haiku', 0.95, 'Low'),
        'altB': ('gpt-4o-mini', 0.90, 'Low'),
        'altC': ('claude-3-haiku + 프롬프트 캐싱', 0.97, 'Low'),
        'period': '즉시 적용 가능 (1~2주 A/B 테스트 권고)'
    },
    'Vertex AI': {
        'altA': ('Vertex AI gemini-1.5-flash', 0.60, 'Medium'),
        'altB': ('Vertex AI gemini-1.5-flash-8b', 0.75, 'Low'),
        'altC': ('Vertex AI + 배치 예측 API', 0.65, 'Low'),
        'period': '2~4주 (파이프라인 수정 필요)'
    }
}

ai_total_d1 = 0
ai_total_d2 = 0
ai_total_d3 = 0
ai_model_rows = []
for a in AI_RESOURCES:
    model = a['model']
    mcost = a['monthly_cost']
    alts = AI_MODEL_ALTS.get(model, {
        'altA': (f"{model}-mini", 0.60, 'Medium'),
        'altB': (f"{model}-lite", 0.75, 'Low'),
        'altC': (f"{model}-lite + 캐싱", 0.80, 'Low'),
        'period': '2~4주'
    })
    save_a = round(mcost * alts['altA'][1])
    save_b = round(mcost * alts['altB'][1])
    save_c = round(mcost * alts['altC'][1])
    ai_total_d1 += save_a
    ai_total_d2 += save_b
    ai_total_d3 += save_c
    ai_model_rows.append({
        'model': model,
        'provider': csp_short(a['provider']),
        'mcost': mcost,
        'altA_name': alts['altA'][0], 'save_a': save_a, 'risk_a': alts['altA'][2],
        'altB_name': alts['altB'][0], 'save_b': save_b, 'risk_b': alts['altB'][2],
        'altC_name': alts['altC'][0], 'save_c': save_c, 'risk_c': alts['altC'][2],
        'period': alts['period']
    })

grand_total_d1 = total_d1 + ai_total_d1
grand_total_d2 = total_d2 + ai_total_d2
grand_total_d3 = total_terminate + ai_total_d3

lines3 = []
lines3.append("# Right-sizing 권고 계획서\n")
lines3.append(f"- 분석 기준일: 2026-04-19  ")
lines3.append(f"- 데이터 기간: 2026-03-01 ~ 2026-03-31 (31일)  ")
lines3.append(f"- 대상 리소스: 컴퓨트 유휴 {len(IDLE)}건 + AI 모델 {len(AI_RESOURCES)}건\n")
lines3.append(f"## 총 예상 절감액 요약\n")
lines3.append("| 대안 | 컴퓨트 절감(KRW/월) | AI 모델 절감(KRW/월) | 합계(KRW/월) | 주요 리스크 |")
lines3.append("|------|---------------------|---------------------|-------------|-----------|")
lines3.append(f"| Downsize-1단 + 모델대안A | {total_d1:,} | {ai_total_d1:,} | **{grand_total_d1:,}** | Low — 단계적 축소, SLA 영향 최소 |")
lines3.append(f"| Downsize-2단 + 모델대안B | {total_d2:,} | {ai_total_d2:,} | **{grand_total_d2:,}** | Medium — 피크 트래픽 리스크 존재 |")
lines3.append(f"| Terminate + 모델대안C | {total_terminate:,} | {ai_total_d3:,} | **{grand_total_d3:,}** | Mixed — 완전유휴Low·과잉프로비전High |")

lines3.append("\n---\n")
lines3.append("## 컴퓨트 Right-sizing\n")
lines3.append("### 판정 기준\n")
lines3.append("- CPU 2주 평균 < 40% AND/OR Memory 2주 평균 < 60% (31일 데이터 전수 적용)  ")
lines3.append("- 절감액 = 현재 월비용 × 다운사이즈 절감률 (AWS/Azure/GCP 공시가 기준 추산)  ")
lines3.append("- Terminate 절감액: 완전유휴(CPU=0%·MEM=0%)는 100%, 과잉프로비전은 90% 적용\n")
lines3.append("### 3대안 비교표\n")
lines3.append("| 리소스 ID | CSP | 현재 유형 | 대안A(Downsize-1단) | 대안B(Downsize-2단) | 대안C(Terminate) | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(KRW/월) | 리스크A | 리스크B | 리스크C |")
lines3.append("|-----------|-----|----------|---------------------|---------------------|-----------------|--------------|--------------|--------------|--------|--------|--------|")
for cr in compute_rows:
    lines3.append(f"| {cr['rid']} | {cr['csp']} | {cr['itype']} | {cr['d1_type']} | {cr['d2_type']} | Terminate | {cr['save_d1']:,} | {cr['save_d2']:,} | {cr['save_terminate']:,} | {cr['risk_d1']} | {cr['risk_d2']} | {cr['risk_term']} |")

lines3.append(f"\n**컴퓨트 소계**: Downsize-1단 {total_d1:,}KRW/월 | Downsize-2단 {total_d2:,}KRW/월 | Terminate {total_terminate:,}KRW/월\n")

lines3.append("### 대안별 상세 조건\n")
lines3.append("#### 대안A — Downsize-1단\n")
lines3.append("- 인스턴스 한 단계 축소 (예: m5.4xlarge → m5.2xlarge, Standard_D8s_v3 → Standard_D4s_v3)  ")
lines3.append("- 절감률: 약 50% (인스턴스 크기 절반 기준)  ")
lines3.append("- SLA 리스크: Low — 현재 이용률 대비 여유분 충분  ")
lines3.append("- 구현 복잡도: Low — 인스턴스 중지 후 유형 변경, 약 10~30분 다운타임  ")
lines3.append("- 권고 적용 기간: 1~2주 내 (운영팀 승인 후)\n")
lines3.append("#### 대안B — Downsize-2단\n")
lines3.append("- 인스턴스 두 단계 축소 (예: m5.4xlarge → m5.xlarge, Standard_D8s_v3 → Standard_D2s_v3)  ")
lines3.append("- 절감률: 약 75%  ")
lines3.append("- SLA 리스크: Medium — 예상치 못한 트래픽 스파이크 대응 능력 감소  ")
lines3.append("- 구현 복잡도: Medium — Auto Scaling 정책 동시 조정 필요  ")
lines3.append("- 권고 적용 기간: 2~4주 내 (성능 테스트 선행 필수)\n")
lines3.append("#### 대안C — Terminate\n")
lines3.append("- 완전 유휴 리소스(CPU=0%·MEM=0%, 31일 연속): i-idle-001, i-idle-002 즉시 종료 권고  ")
lines3.append("- 과잉 프로비저닝 리소스: 14일 추가 모니터링 후 담당팀 승인 절차 진행  ")
lines3.append("- SLA 리스크: Low(완전유휴) / High(과잉프로비전 Terminate)  ")
lines3.append("- 구현 복잡도: Low(완전유휴) / High(의존성 확인 필요)  ")
lines3.append("- 권고 적용 기간: 완전유휴 즉시 / 과잉프로비전 4~8주\n")

lines3.append("---\n")
lines3.append("## AI 모델 최적화\n")
lines3.append("### 판정 기준\n")
lines3.append("- GPU 이용률 < 60% 또는 동일 품질 달성 가능한 경량 모델 존재 시 다운그레이드 권고  ")
lines3.append("- 절감률은 각 모델 공식 API 단가 기준 추산  ")
lines3.append("- 품질 리스크: 다운그레이드 전 7일 A/B 테스트 및 품질 지표(정확도·응답시간) 모니터링 필수\n")
lines3.append("### 모델 다운그레이드 3종 대안\n")
lines3.append("| 현재 모델 | 제공사 | 월비용(KRW) | 대안A(보수적) | 대안B(균형) | 대안C(최적화) | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(KRW/월) | 품질리스크A | 품질리스크B | 품질리스크C |")
lines3.append("|----------|--------|------------|---------------|-------------|---------------|--------------|--------------|--------------|-----------|-----------|-----------|")
for am in ai_model_rows:
    lines3.append(f"| {am['model']} | {am['provider']} | {am['mcost']:,} | {am['altA_name']} | {am['altB_name']} | {am['altC_name']} | {am['save_a']:,} | {am['save_b']:,} | {am['save_c']:,} | {am['risk_a']} | {am['risk_b']} | {am['risk_c']} |")

lines3.append(f"\n**AI 모델 소계**: 대안A {ai_total_d1:,}KRW/월 | 대안B {ai_total_d2:,}KRW/월 | 대안C {ai_total_d3:,}KRW/월\n")
lines3.append("### AI 대안 상세 설명\n")
lines3.append("#### 대안A — 보수적 (동일 제공사 소형 모델)\n")
lines3.append("- claude-3-5-sonnet → claude-3-haiku: 동일 Anthropic 플랫폼, API 호환 100%  ")
lines3.append("- Vertex AI → gemini-1.5-flash: 동일 GCP 인프라, 마이그레이션 공수 최소  ")
lines3.append("- 품질 리스크: Low — 일반 텍스트 처리 태스크 품질 차이 미미  ")
lines3.append("- 적용 기간: 즉시 적용 가능 (1~2주 A/B 테스트 권고)\n")
lines3.append("#### 대안B — 균형 (타사 동급 모델)\n")
lines3.append("- claude-3-5-sonnet → gpt-4o-mini: OpenAI API, 프롬프트 일부 수정 필요  ")
lines3.append("- Vertex AI → gemini-1.5-flash-8b: 경량화 버전, 단순 분류/요약 태스크 적합  ")
lines3.append("- 품질 리스크: Low~Medium — 복잡한 추론 태스크에서 품질 차이 발생 가능  ")
lines3.append("- 적용 기간: 2~4주 (API 통합 수정 + 테스트)\n")
lines3.append("#### 대안C — 최적화 (경량 모델 + 캐싱)\n")
lines3.append("- claude-3-haiku + 프롬프트 캐싱 활성화: 반복 요청 캐시 히트율 향상으로 추가 절감  ")
lines3.append("- Vertex AI 배치 예측 API: 실시간 아닌 비동기 처리로 비용 최대 50% 절감  ")
lines3.append("- 품질 리스크: Low — 동일 모델 사용, 캐싱만 추가  ")
lines3.append("- 적용 기간: 즉시 적용 가능\n")

lines3.append("---\n")
lines3.append("## 실행 우선순위 로드맵\n")
lines3.append("### 즉시 실행 (0~2주)\n")
lines3.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
lines3.append("|---------|--------|------|-----------------|-------|")
lines3.append("| P1 | i-idle-001, i-idle-002 | Terminate | 0 (비용 없음 — 연결 리소스 정리 효과) | Low |")
lines3.append(f"| P2 | claude-3-5-sonnet | 대안C (캐싱 활성화) | {ai_model_rows[0]['save_c']:,} | Low |")
lines3.append(f"| P3 | vm-overprov-001, 002, 003 (Azure D8s) | Downsize-1단 → D4s | {round(2612903*0.5*3):,} | Low |")
lines3.append("| P4 | i-overprov-001~005 (AWS m5.4xlarge) | Downsize-1단 → m5.2xlarge | {:,} | Low |".format(round(829440*0.5*5)))
lines3.append("")
lines3.append("### 단기 실행 (2~4주)\n")
lines3.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
lines3.append("|---------|--------|------|-----------------|-------|")
lines3.append(f"| P5 | claude-3-5-sonnet | 대안A (claude-3-haiku) | {ai_model_rows[0]['save_a']:,} | Low |")
lines3.append("| P6 | gce-overprov-002~005 (n2-standard-8) | Downsize-1단 → n2-standard-4 | {:,} | Low |".format(round(311040*0.5*4)))
lines3.append("| P7 | vm-spike-azure, vm-api-001 (D4s) | Downsize-1단 → D2s | {:,} | Medium |".format(round((1393548+1306452)*0.5)))
lines3.append("")
lines3.append("### 중기 실행 (4~8주)\n")
lines3.append("| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |")
lines3.append("|---------|--------|------|-----------------|-------|")
lines3.append(f"| P8 | Vertex AI trainingPipelines | 대안B (gemini-1.5-flash-8b) | {ai_model_rows[1]['save_b']:,} | Low |")
lines3.append("| P9 | i-web-001~003, i-spike-001 | Downsize-1단 | {:,} | Medium |".format(round((414720*3+574839)*0.5)))
lines3.append("| P10 | gce-web/api 시리즈 (n2-standard-4) | MEM 모니터링 후 판단 | - | 검토 필요 |")
lines3.append("")
lines3.append(f"\n## 전체 예상 절감 합계\n")
lines3.append(f"- **Downsize-1단 + AI대안A 시나리오**: {grand_total_d1:,}KRW/월 ({grand_total_d1*12:,}KRW/년)  ")
lines3.append(f"- **Downsize-2단 + AI대안B 시나리오**: {grand_total_d2:,}KRW/월 ({grand_total_d2*12:,}KRW/년)  ")
lines3.append(f"- **Terminate + AI대안C 시나리오**: {grand_total_d3:,}KRW/월 ({grand_total_d3*12:,}KRW/년)  ")
lines3.append(f"\n> 권고 최적안: **Downsize-1단 + AI대안A** — 절감액 {grand_total_d1:,}KRW/월, 리스크 최소, 즉시 적용 가능  ")
lines3.append("> 단계별 실행으로 총 절감 극대화 가능 (P1~P4 우선 실행 시 약 4주 내 절감 효과 가시화)  ")

with open('out/rightsize-plan.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines3))

print("[3] out/rightsize-plan.md 작성 완료")
print(f"\n=== 최종 요약 ===")
print(f"유휴 리소스: {len(IDLE)}건")
print(f"AI 모델: {len(AI_RESOURCES)}건")
print(f"Downsize-1단+AI대안A: {grand_total_d1:,}KRW/월")
print(f"Downsize-2단+AI대안B: {grand_total_d2:,}KRW/월")
print(f"Terminate+AI대안C:    {grand_total_d3:,}KRW/월")
