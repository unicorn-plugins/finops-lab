# FinOps 리뷰 런북

**작성일**: 2026-04-19  
**작성자**: 최운영/프랙티셔너 (FinOps Operate)  
**참조**: finops.md §4.13, gate-criteria.yaml, resources/templates/monthly-review-agenda.md  
**대상**: (주)하이브리지텔레콤 (HBT) FinOps팀

---

## 1. 리뷰 체계 개요

FinOps 리뷰는 **주간·월간·분기** 3개 주기로 운영함.  
각 주기는 finops.md §4.13의 협업 문화·거버넌스 원칙에 따라 참석자 범위와 의사결정 수준이 구분됨.

| 주기 | 일정 | 시간 | 주요 목적 | 참석자 |
|------|------|------|---------|--------|
| 주간 | 매주 월요일 10:00 | 30분 | 이상 비용·KPI 이상 신속 대응 | FinOps팀 + 엔지니어링 |
| 월간 | 매월 셋째 주 수요일 10:00 | 60분 | 예산 대비 실적·KPI 종합 리뷰 | FinOps팀 + 재무·사업 대표 |
| 분기 | 분기 마지막 월 첫째 주 목요일 14:00 | 90분 | 전략 정렬·성숙도 평가·투자 의사결정 | FinOps팀 + 경영진 |

---

## 2. 주간 리뷰 (매주 월요일)

### 목적

전주 이상 비용 탐지 결과 확인 및 KPI 이상 항목 신속 대응.  
자동화 파이프라인 4단계(알림)에서 생성된 미처리 티켓 일괄 검토.

### 참석자

| 역할 | 담당 | 책임 |
|------|------|------|
| 퍼실리테이터 | 프랙티셔너 (최운영) | 회의 진행, 액션 아이템 확정 |
| 비용 분석 | cost-analyst | 이상 비용 현황 발표 |
| 태깅 점검 | tag-governor (태거) | 주간 태깅 스캔 결과 보고 |
| 리소스 최적화 | rightsize-advisor (라이트사이저) | 유휴 리소스 현황 보고 |
| 엔지니어링 대표 | 서비스개발팀·데이터AI팀 리드 (교대) | 최적화 실행 현황 |

### 30분 아젠다

| 소요시간 | 주제 | 진행자 | 내용 |
|---------|------|--------|------|
| 00~10분 | 이상 비용 현황 | cost-analyst | 전주 이상 이벤트 목록, ANOMALY_DETECT_LATENCY 현황, 미처리 Jira 티켓 |
| 10~20분 | KPI 이상 항목 점검 | 프랙티셔너 | KPI-CSP-1~3·KPI-AI-1~3 주간 변동, 게이트 미달 항목 확인 |
| 20~30분 | 액션 아이템 확정 | 프랙티셔너 | 담당자·마감일 지정, 미해결 티켓 우선순위 재조정 |

### 주간 점검 체크리스트

- [ ] 이상 비용 탐지 건수 및 원인 확인 (전주 동기간 대비 +20% 초과 건)
- [ ] ANOMALY_DETECT_LATENCY: 이상 이벤트별 탐지~알림 시간 ≤ 24h 확인
- [ ] KPI-CSP-1 태깅 커버리지 주간 변동 확인 (목표 ≥ 95%)
- [ ] KPI-AI-1 GPU 활용률 주간 변동 확인 (목표 ≥ 60%)
- [ ] 전주 액션 아이템 완료 현황 업데이트
- [ ] 미처리 Jira 티켓 현황 확인 (`finops-tag-violation`, `finops-idle-resource`, `finops-anomaly-sla`)

### 산출물

- 주간 리뷰 회의록 (Notion → FinOps > 주간리뷰)
- 업데이트된 액션 아이템 목록 (Jira)
- Slack #finops-review 요약 공지

---

## 3. 월간 리뷰 (매월 셋째 주 수요일)

### 목적

예산 대비 실적 종합 점검, KPI 6종 현황 리뷰, 최적화 실행 성과 측정.  
게이트 기준 6종 미달 항목에 대한 개선 계획 수립.

### 참석자

| 역할 | 담당 | 책임 |
|------|------|------|
| 퍼실리테이터 | 프랙티셔너 (최운영) | 회의 진행, 의사결정 촉진 |
| 데이터 준비 | cost-analyst | 대시보드 업데이트, 리포트 준비 (회의 3일 전) |
| 서비스개발 대표 | CC-200 팀 리드 | CC-200 비용 현황, B2B·IoT 단위경제 |
| 데이터/AI 대표 | CC-300 팀 리드 | CC-300 AI 비용 현황, GPU·LLM 최적화 |
| 인프라 대표 | CC-100 팀 리드 | CC-100 비용 현황, RI 관리 현황 |
| 재무팀 담당 | 재무팀 담당자 (필요 시) | 예산 대비 실적, 이월 예산 조정 |

### 60분 아젠다

| 소요시간 | 주제 | 진행자 | 내용 |
|---------|------|--------|------|
| 00~15분 | 비용 현황 리뷰 | cost-analyst | 월 총액·CSP별 분해·CostCenter별(CC-100/200/300) 분석·전월 대비 증감 |
| 15~35분 | 최적화 기회 리뷰 | 프랙티셔너 | 유휴 리소스 현황(IDLE_RESOURCE_RATE)·Right-sizing 실행 현황·RI/SP 활용률(RI_UTILIZATION) |
| 35~50분 | KPI 리뷰 | 프랙티셔너 | KPI 6종 + HBT LoB 단위경제 4종 현황·게이트 6종 판정 |
| 50~60분 | 액션 아이템 확정 | 프랙티셔너 | 담당자·마감일 지정, 다음 월 준비 일정 확인 |

### 월간 KPI·게이트 체크리스트

**KPI 점검 항목**

- [ ] KPI-CSP-1: 태깅 커버리지 ≥ 95% 확인 (목표 미달 시 tag-governor 에스컬레이션)
- [ ] KPI-CSP-2: RI/SP 활용률 ≥ 80% 확인 (측정 시작 후)
- [ ] KPI-CSP-3: 이상 탐지 응답 시간 ≤ 24h 확인
- [ ] KPI-AI-1: GPU 활용률 ≥ 60% 확인
- [ ] KPI-AI-2: AI 비용/토큰 전월 대비 ≥ 5% 감소 확인
- [ ] KPI-AI-3: 모델 효율 ≥ 70% 확인
- [ ] HBT LoB 단위경제 4종(MNO·MVNO·IoT·B2B) 전월 대비 증감 확인

**사전 준비 (회의 3일 전 — cost-analyst 담당)**

- [ ] FOCUS 정규화 데이터 최신화 (focus-normalized.csv 당월 데이터 반영)
- [ ] CSP별 비용 집계 완료 (CC-100/200/300)
- [ ] RI/SP 활용률 계산 (CommitmentDiscountStatus Used/Unused 비율)
- [ ] 유휴 리소스 목록 작성 (CPU < 5%, 7일 이상)
- [ ] AI 리소스 비용 집계 (Anthropic API + Vertex AI, ChargebackUnit별)
- [ ] 회의 자료 사전 공유 (회의 24시간 전 Slack #finops-review)

### 산출물

- 월간 비용 리포트 (PDF, Notion 저장)
- 게이트 6종 현황 판정 표 업데이트 (kpi-dashboard.md)
- 액션 아이템 목록 (Jira 등록)
- Slack #finops-review 요약 공지

---

## 4. 분기 리뷰

### 목적

전략 정렬·성숙도 평가·Crawl→Walk 전환 진행 상황 점검.  
HBT 사업 포트폴리오(MNO·MVNO·IoT·B2B) 단위경제 ROI 경영진 보고.  
다음 분기 투자·약정(RI/SP) 의사결정 승인.

### 참석자

| 역할 | 담당 | 책임 |
|------|------|------|
| 퍼실리테이터 | 프랙티셔너 (최운영) | 회의 진행 |
| 발표 | FinOps팀 전원 | 분기 성과·성숙도 평가 |
| 경영진 스폰서 | CTO / CFO | 전략 의사결정, 투자 승인 |
| 재무팀 | 재무팀장 | 예산 재배분, ROI 확인 |
| LoB 사업부 | MNO·MVNO·IoT·B2B 사업팀장 | 사업별 단위경제 현황 확인 |

### 90분 아젠다

| 소요시간 | 주제 | 진행자 | 내용 |
|---------|------|--------|------|
| 00~20분 | 분기 비용 성과 요약 | 프랙티셔너 | 분기 총비용·절감 실적·예산 대비 달성률 |
| 20~40분 | KPI·게이트 6종 분기 판정 | 프랙티셔너 | 게이트 통과 현황, 미달 원인 분석, 개선 추이 |
| 40~60분 | 성숙도 평가 및 전환 현황 | 프랙티셔너 | Crawl→Walk 전환 마일스톤 달성 여부, Ownership×Capability 진단 |
| 60~75분 | HBT LoB 단위경제 보고 | LoB 대표 | MNO·MVNO·IoT·B2B 단위당 비용 vs 매출 기여 |
| 75~90분 | 다음 분기 계획 및 투자 승인 | CTO/CFO | RI/SP 구매 시나리오 승인, Walk→Run 전환 투자 결정 |

### 분기 점검 항목

- [ ] 게이트 6종 분기 판정 — 5개 게이트 모두 통과 여부 확인 (Walk 전환 조건)
- [ ] walk_stage_criteria 달성 여부 확인 (gate-criteria.yaml §walk_stage_criteria)
  - TAGGING_COVERAGE ≥ 95% (필수)
  - FORECAST_MAPE ≤ 10% (필수)
  - ANOMALY_DETECT_LATENCY ≤ 24h (필수)
  - RI_UTILIZATION ≥ 80% (권장, Walk 달성 후 3개월 내)
  - IDLE_RESOURCE_RATE ≤ 3% (권장)
- [ ] 월간 FinOps 리뷰 3개월 연속 운영 확인
- [ ] 단위경제 KPI 3종 측정 시작 확인
- [ ] 전 프로젝트 예산 경보 자동화 적용 확인
- [ ] Ownership×Capability 성숙도 재진단 (분기별 갱신)

### 산출물

- 분기 FinOps 성과 보고서 (경영진 배포)
- 성숙도 진단 결과 업데이트 (Crawl/Walk/Run 단계별)
- 다음 분기 RI/SP 구매 승인 의사결정 로그
- Crawl→Walk 전환 로드맵 마일스톤 업데이트

---

## 5. 게이트 기준 6종 — 현재값 vs 기준 판정

> 기준: gate-criteria.yaml (2026-04-18 기준, 임의 변경 금지)

| 게이트 ID | 지표명 | 기준 연산자 | 기준값 | 현재값 | 판정 | 책임 에이전트 | Jira 레이블 |
|---------|--------|----------|--------|--------|------|------------|-----------|
| TAGGING_COVERAGE | 태깅 커버리지 | ≥ | 95% | 96.12% | **O 통과** | tag-governor (태거) | `finops-tag-violation` |
| FORECAST_MAPE | 비용 예측 MAPE | ≤ | 10% | 측정 시작 | **— 미측정** | finops-practitioner (프랙티셔너) | `finops-forecast-miss` |
| RI_UTILIZATION | RI/SP 활용률 | ≥ | 80% | 측정 시작 | **— 미측정** | commit-planner (커밋터) | `finops-ri-underutilized` |
| ANOMALY_DETECT_LATENCY | 이상 탐지 지연 | ≤ | 24h | 측정 시작 | **— 미측정** | cost-analyst (FinOps팀) | `finops-anomaly-sla` |
| IDLE_RESOURCE_RATE | 유휴 리소스 비율 | ≤ | 3% | 측정 시작 | **— 미측정** | rightsize-advisor (라이트사이저) | `finops-idle-resource` |
| GPU_UTILIZATION | GPU 활용률 | ≥ | 60% | 측정 시작 | **— 미측정** | finops-practitioner (프랙티셔너) | `finops-gpu-underutilized` | *(TASK 요구 게이트, gate-criteria.yaml 미정의 — Walk 단계 확장 예정)* |

---

## 6. 게이트 미충족 시 책임 에이전트·에스컬레이션 절차

### TAGGING_COVERAGE (태깅 커버리지 < 95%)

**책임 에이전트**: tag-governor (태거 / 김태규)  
**1차 조치** (즉시): tag-governor 에이전트 실행 → 위반 리소스 목록 출력 → 오너 Slack 알림  
**에스컬레이션**: 72시간 내 미수정 시 FinOps팀장 에스컬레이션  
**추가 에스컬레이션**: 1개월 연속 미달 시 인프라운영팀장·서비스개발팀장 공동 대응 지시  
**Jira 레이블**: `finops-tag-violation`

---

### FORECAST_MAPE (비용 예측 MAPE > 10%)

**책임 에이전트**: finops-practitioner (프랙티셔너 / 최운영)  
**1차 조치** (즉시): 예측 모델 파라미터 점검 → 이상 데이터 포인트 제거 → 재예측 실행  
**에스컬레이션**: 연속 2개월 초과 시 모델 고도화 태스크 생성 + 데이터 엔지니어링팀 협업 요청  
**추가 에스컬레이션**: 3개월 연속 미달 시 외부 FinOps 툴링 도입 검토 (분기 리뷰 경영진 보고)  
**Jira 레이블**: `finops-forecast-miss`

---

### RI_UTILIZATION (RI/SP 활용률 < 80%)

**책임 에이전트**: commit-planner (커밋터 / 박약정)  
**1차 조치** (즉시): 미사용 RI 원인 분석 → 인스턴스 교체 또는 RI 수정/판매 검토  
**에스컬레이션**: 활용률 60% 미만 시 RI 추가 구매 즉시 중단 + 재무팀 보고  
**추가 에스컬레이션**: 60% 미만 2개월 지속 시 RI 전략 전면 재검토 + 경영진 승인 요청  
**Jira 레이블**: `finops-ri-underutilized`

---

### ANOMALY_DETECT_LATENCY (이상 탐지 지연 > 24h)

**책임 에이전트**: cost-analyst (FinOps팀 / 이지수팀장)  
**1차 조치** (즉시): 탐지 파이프라인 점검 → 알림 설정 재확인 → 수동 알림 발송  
**에스컬레이션**: 48시간 초과 시 FinOps팀 SLA 위반 처리 + 인시던트 티켓 생성 (`finops-anomaly-sla`)  
**추가 에스컬레이션**: 분기 내 3회 이상 SLA 위반 시 파이프라인 아키텍처 재설계 + CTO 보고  
**Jira 레이블**: `finops-anomaly-sla`

---

### IDLE_RESOURCE_RATE (유휴 리소스 비율 > 3%)

**책임 에이전트**: rightsize-advisor (라이트사이저 / 이최적)  
**1차 조치** (즉시): 유휴 리소스 목록 출력 → 중지/삭제 여부 오너 확인 → 72시간 내 처리  
**에스컬레이션**: 비율 10% 초과 시 긴급 최적화 태스크 생성 + FinOps팀장 즉시 보고  
**추가 에스컬레이션**: 10% 초과 2주 지속 시 해당 팀 비용 리뷰 긴급 소집 + 임원 보고  
**Jira 레이블**: `finops-idle-resource`

---

### GPU_UTILIZATION (GPU 활용률 < 60%)

**책임 에이전트**: finops-practitioner (프랙티셔너 / 최운영) + rightsize-advisor (라이트사이저 / 이최적)  
**1차 조치** (즉시): GPU 스케줄링 정책 점검 → AI 워크로드 배치 최적화 검토 → 데이터/AI팀 협업 요청  
**에스컬레이션**: 2주 연속 < 60% 시 GPU 인스턴스 다운사이징 권고 + commit-planner RI 재검토  
**추가 에스컬레이션**: 1개월 연속 미달 시 AI 인프라 전략 재검토 + CTO 보고  
**Jira 레이블**: `finops-gpu-underutilized`

---

## 7. 의사결정 로그 템플릿

| # | 날짜 | 의사결정 내용 | 근거 | 담당자 | 마감일 | 결과 |
|---|------|-------------|------|--------|--------|------|
| 1 | | | | | | |
| 2 | | | | | | |

---

## 8. 운영 채널 및 도구

| 용도 | 채널/도구 |
|------|---------|
| 일상 알림 | Slack #finops-review |
| 티켓 관리 | Jira (finops-* 레이블) |
| 문서 보관 | Notion (팀 위키 > FinOps) |
| 회의 | Microsoft Teams (화상) |
| 변경 관리 | Terraform + Jira 연계 |
