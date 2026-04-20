# COVERS 정렬 12개월 스킬셋 로드맵 — HBT

> 작성: 전략기획 태희 / 근거: `resources/rulebook/covers-principles.yaml` (18 규칙), State of FinOps 2026 Top 스킬셋

## 1. COVERS 6원칙 정렬 현황

| 원칙 | 현재 상태 | 목표(1년) | 핵심 규칙 |
|------|-----------|-----------|----------|
| **C** Collaboration | 분기 리뷰, 비공식 협업 | 월 공동 리뷰 정착, #finops-review 채널 상시 운영 | COVERS-C-01, C-02, C-03 |
| **O** Ownership | 태깅 85%, CostCenter 귀속 불완전 | 태깅 95%+, 오너 셀프체크 정례화 | COVERS-O-01, O-02, O-03 |
| **V** Value-driven | 단위경제 KPI 0종, ROI 추적 없음 | KPI 3종 측정, RI/SP ROI 월간 리포트 | COVERS-V-01, V-02, V-03 |
| **E** Elastic Utilization | 유휴 수동 탐지, RI 미집계 | 유휴율 ≤3%, RI 활용률 80%+ | COVERS-E-01~04 |
| **R** Right-time Report | D+N 리포팅, MAPE 미측정 | 24h 내 반영, MAPE ≤10%, 월 3영업일 | COVERS-R-01~04 |
| **S** Steering | FinOps팀 2명 올인원 | 연합 거버넌스, 분기 성숙도 점검 | COVERS-S-01~04 |

## 2. 분기별 스킬셋 로드맵 (Q1~Q4)

State of FinOps 2026 Top 스킬셋(AI Cost Mgmt 58% / FinOps Tooling 43% / Eng·Automation 40% / Capacity Planning 39%)을 분기별로 배분함.

### Q1 — 기반 다지기 (Inform 중심)

| 집중 영역 | 필요 스킬셋 | COVERS 원칙 | 담당 Ownership |
|-----------|------------|-------------|---------------|
| FOCUS v1.1 멀티클라우드 정규화 | FinOps Tooling, Data Engineering | COVERS-S-01 | FinOps팀 + 데이터/AI팀 |
| 필수 4태그 거버넌스 자동화 | Eng/Automation, Policy-as-Code | COVERS-O-01, O-02, S-02 | FinOps팀 + 전 개발팀 |
| Chart.js 통합 대시보드 v1 | Cost Visualization | COVERS-R-02 | 비용 시각화팀 |

**Q1 OKR**  
- O: HBT 3 CSP 비용을 단일 언어로 말할 수 있는 기반을 구축함.  
- KR1: FOCUS v1.1 정규화 커버리지 100% (AWS·Azure·GCP).  
- KR2: 태깅 커버리지 85% → 90%.  
- KR3: 통합 대시보드 CostCenter×Project 뷰 배포.

### Q2 — 가시성·이상 탐지 (Inform + Optimize 시작)

| 집중 영역 | 필요 스킬셋 | COVERS 원칙 | 담당 Ownership |
|-----------|------------|-------------|---------------|
| 이상 비용 탐지 24h 자동 파이프라인 | Anomaly Detection, Eng/Automation | COVERS-R-01 | FinOps팀 |
| 유휴 리소스·Right-sizing 주간 권고 | Capacity Planning | COVERS-E-01, E-02 | FinOps + 인프라운영팀 |
| 월간 공동 리뷰 정착 | Collaboration, Facilitation | COVERS-C-01, O-03 | 전 팀 |

**Q2 OKR**  
- O: 낭비를 사전에 발견하고 월간 리듬으로 공동 의사결정하는 체계를 정착함.  
- KR1: 이상 비용 탐지 지연 ≤24h.  
- KR2: 태깅 커버리지 95% 달성.  
- KR3: 월간 리뷰 참석률 ≥90% (CC-100/200/300 오너 전원).

### Q3 — 최적화 실행 (Optimize 중심)

| 집중 영역 | 필요 스킬셋 | COVERS 원칙 | 담당 Ownership |
|-----------|------------|-------------|---------------|
| RI/SP 3시나리오 의사결정 + 실행 | Capacity Planning, Commitment Strategy | COVERS-E-04, V-03 | 커밋터(약정 전략가) + 재무 |
| 단위경제 KPI 3종 측정 개시 | Value Engineering, BI | COVERS-V-01, V-02 | FinOps팀 + 데이터/AI팀 |
| FinOps for AI — Vertex AI/BigQuery 비용 추적 | AI Cost Management (SoF 2026 58%) | COVERS-V-01 (AI 확장), E-03 | 데이터/AI팀 |

**Q3 OKR**  
- O: 약정·단위경제·AI 비용 3축에서 측정 가능한 ROI를 생성함.  
- KR1: RI/SP 활용률 0 → 70%.  
- KR2: MAU당/API 100만건당/ML 학습당 비용 3종 월간 리포트 발행.  
- KR3: ML 학습 1회당 비용 전월 대비 15% 절감.

### Q4 — 체계화·정착 (Operate 중심)

| 집중 영역 | 필요 스킬셋 | COVERS 원칙 | 담당 Ownership |
|-----------|------------|-------------|---------------|
| 예측(MAPE) 관리 + 연간 예산 편성 참여 | Forecasting, FP&A | COVERS-R-03, S-04 | FinOps팀 + 재무팀 |
| 연합 거버넌스 운영 모델 고도화 | Steering, Operating Model | COVERS-S-02, S-03 | 경영진 + FinOps팀 |
| Walk 전환 최종 점검 + 경영진 보고 | Executive Alignment | COVERS-R-04, S-03 | CTO/CFO + FinOps팀 |

**Q4 OKR**  
- O: Walk 단계 전환을 공식화하고 차년도 운영 모델을 경영진과 합의함.  
- KR1: 예측 MAPE ≤10% 3개월 연속 달성.  
- KR2: RI 활용률 80% 달성.  
- KR3: COVERS 18개 규칙 전부 게이트 기준 통과 (COVERS-S-03 분기 점검).

## 3. 스킬셋 확보 방안

| 스킬셋 | 확보 경로 | 시점 |
|--------|----------|------|
| AI Cost Management | 데이터/AI팀 내 1명 FOCP 취득 + Vertex AI 비용 워크숍 | Q2~Q3 |
| FinOps Tooling | FinOps팀 FOCUS 정규화 구현 + 외부 리퍼런스 | Q1 |
| Engineering/Automation | 클라우드아키텍처팀 협업, Policy-as-Code 파일럿 | Q1~Q2 |
| Capacity Planning | 커밋터(박약정) 주도 RI/SP 의사결정 매트릭스 | Q3 |

## 4. 리스크 및 완화

| 리스크 | 영향 | 완화책 |
|--------|------|--------|
| FinOps팀 2명 병목 | 일정 지연 | 연합 거버넌스(COVERS-S-03)로 일상 책임 분산, Q1 RACI 확정 |
| 태깅 저항 | 95% 미달성 | 오너 셀프체크(COVERS-O-03) + 72h 에스컬레이션 규칙 강제 |
| AI 비용 데이터 불완전 | Q3 KPI 지연 | Q2 중 Vertex AI 빌링 익스포트 사전 검증 |
