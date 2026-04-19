# State of FinOps 2026 — 실습 가이드 요약

> 출처: FinOps Foundation, *State of FinOps 2026 Report* (1,192명 응답, 연 $83B+ 클라우드 지출 대표)
> 본 문서는 원본 리포트에서 **finops-lab 실습에 직접 활용할 수 있는 내용**만 추출·재구성한 요약본이다.

---

## 1. 큰 그림: "Cloud Cost"에서 "Technology Value"로

- FinOps Foundation 미션이 *"Value of Cloud"* → *"Value of Technology"* 로 갱신됨.
- FinOps는 단순 클라우드 비용 분석을 넘어 **AI · SaaS · 라이선스 · Private Cloud · 데이터센터 · (신규) 인건비**까지 포괄하는 기술 가치 관리 규율로 확장.
- 실습 설계 시 **클라우드 비용만이 아니라 "기술 지출 전반"을 대상**으로 잡으면 최신 트렌드와 맞춤.

### 기술 범주별 관리율 (YoY)

| 범주 | 2026 | 2025 | YoY |
|---|---|---|---|
| AI | 98% | 63% | +35% |
| SaaS | 90% | 65% | +25% |
| Licensing | 64% | 49% | +15% |
| Private Cloud | 57% | 39% | +18% |
| Data Center | 48% | 36% | +12% |
| Labor (신규) | ~28% | — | — |

---

## 2. 실습 우선순위: Top 스킬셋 수요 (p.9)

FinOps 팀이 향후 12개월 내 보강하려는 역량:

1. **AI Cost management — 58%**
2. **FinOps Tooling — 43%**
3. **Engineering / Automation Development — 40%**
4. **Capacity Planning / Forecasting — 39%**
5. AI Engineering — 24%
6. Infrastructure Architect — 17%

→ 실습 주제를 고를 때 1·2·3·4 영역에 해당하는 Hands-on 랩을 최우선으로 구성.

---

## 3. FinOps Capability 성숙도 경로 (모든 기술 범주에 공통 적용)

> "Dashboards are table stakes of yesterday — reactive. You have to move to proactive, real-time, automation."

리포트가 강조하는 단계별 경로 — **실습 커리큘럼의 기본 순서**로 채택:

1. **Understand Usage & Cost** — 데이터 수집 · Allocation · Reporting & Analytics
2. **Quantify Business Value** — Forecasting · Budgeting · Planning & Estimating · Unit Economics
3. **Optimize Usage & Cost** — Rightsizing · Rate Optimization · Workload Optimization
4. **Manage the FinOps Practice** — 거버넌스 · 정책 · 자동화

### 범주별 우선 역량 (p.18–19)

| 기술 범주 | 1순위 | 2순위 | 3순위 | 4순위 |
|---|---|---|---|---|
| SaaS | Allocation | Forecasting & Budgeting | Reporting & Analytics | Planning & Estimating |
| Licensing | Allocation | Forecasting & Budgeting | Planning & Estimating | Reporting & Analytics |
| Data Center | Allocation | Planning & Estimating | Forecasting & Budgeting | Workload Optimization |
| Data Cloud Platforms | Allocation | Reporting & Analytics | Forecasting & Budgeting | Rate Optimization |

→ 공통 패턴: **Allocation 먼저, Optimization 나중**. "보이지 않으면 자동화할 수 없다."

---

## 4. AI FinOps — 최우선 실습 영역

**"FinOps for AI" 는 Top 미래 우선순위 (33%)** 이며 AI 관리율은 2년 만에 31% → 98% 로 급증.

### 4.1 실습 포인트: AI 비용의 3대 난제 (p.25)

| 난제 | 실습 아이디어 |
|---|---|
| **AI 비용 가시성 부족** (토큰·요청·GPU) | LLM 호출 로그 수집 → 토큰/모델/서비스별 비용 대시보드 |
| **사업부별 Allocation 난이도** | API Key · tag · metadata 기반 chargeback 모델 구현 |
| **AI ROI 정량화** | 비용 대비 생산성/매출 기여도 단위경제학(Unit Economics) 산식 |

### 4.2 실습 포인트: AI 비용 모니터링 (p.22 Top 요청 기능)

리포트가 "아직 없는 도구 기능 1위"로 꼽은 항목 = 실습 프로젝트 아이디어:

1. **AI 지출의 Granular 모니터링** — tokens, LLM requests, GPU utilization
2. **Shift-Left: Pre-Deployment Architecture Costing** — 배포 전 아키텍처 단위 비용 추정
3. **Single Pane of Glass** — 이종 기술 지출 통합 뷰

### 4.3 "AI for FinOps" — FinOps 팀 생산성 향상 (p.27)

49% 가 "매우 중요"로 평가. 초기 Use Case = 실습 주제로 매핑:

- **이상 징후 감지 & 조기 알림** (cost anomaly detection)
- **자동 Rightsizing 추천**
- **Natural Language 비용 데이터 조회** (text-to-SQL on billing data)
- **할인 상품 자동 구매** (RI/SP/CUD auto-procurement)
- **자동 리소스 태깅** (allocation 속도 개선)

### 4.4 AI 투자처 분포 (2026)

| 환경 | 2025 | 2026 |
|---|---|---|
| Public Cloud | ~90% | ~92% |
| SaaS | ~68% | ~80% |
| Data Center | ~30% | ~43% |
| Private Cloud | ~30% | ~44% |

→ SaaS · Private Cloud · 데이터센터의 AI 투자 증가폭이 커짐. 실습도 **Public Cloud 외 환경**을 포함시킬 것.

---

## 5. FOCUS — 표준 빌링 데이터 스펙 (실습 데이터 기반)

**FinOps Open Cost and Usage Specification (FOCUS)**: 이종 제공사 빌링 데이터를 통일된 스키마로 정규화.

### 채택 현황 (2026)
- $100M+ 지출 조직: ~85% FOCUS 포맷 빌링 데이터 확보/계획
- $15M–$100M: ~84%
- $15M 미만: ~90%

### 실습 활용 포인트
- **AWS CUR / Azure Cost Exports / GCP Billing → FOCUS 스키마 변환 파이프라인** 구축이 현실적이고 수요도 큰 랩.
- FOCUS 확장 Top 요청: **AI workloads · Data Center · PaaS/SaaS** → 이 세 영역의 비표준 빌링을 FOCUS로 정규화하는 실습이 가장 가치 있음.

---

## 6. Shift-Left 실습 아이디어

FinOps를 엔지니어링/프로덕트 라이프사이클 **이른 단계**에 삽입하는 트렌드. 리포트가 강조한 **미해결 문제** = 좋은 실습 과제:

1. **Pre-Deployment Architecture Costing** — Terraform/IaC 단계에서 비용 추정 자동화
2. **Cost-aware CI/CD Gate** — PR 단계에서 예상 비용 증분 체크
3. **Unit Economics per Feature** — 기능별 단위 비용 계산 방식
4. **"Cost avoidance" 측정** — "Once you fix it, it's gone" 문제 해결을 위한 baseline 비교 기법

---

## 7. 우선순위 우선주의 Map (현재 vs 향후 12개월)

| 현재 Top | 향후 Top (상승) |
|---|---|
| Workload Optimization & Waste Reduction (25%) | **FinOps for AI (33%, ↑6)** |
| Governance & Policy (21%) | **Applying FinOps to more Scopes (28%)** |
| Forecasting (20%) | **AI for FinOps (24%, ↑6)** |
| Org Alignment (17%) | **Unit Economics (20%, ↑5)** |

→ 실습 난이도 조절:
- **입문**: Workload Optimization, Forecasting
- **중급**: Allocation, Unit Economics, Governance Policy
- **고급**: FinOps for AI, AI for FinOps, Multi-scope 통합

---

## 8. 인접 분야 — 통합 실습 확장 포인트

FinOps가 협업하는 분야 (% 응답):

- **ITFM** (IT Financial Management) — 공유 데이터 65%
- **ITSM** — 정책/자동화 55%
- **ITAM/SAM** — SaaS · 라이선스 컴플라이언스 48%
- **ESG / Sustainability** — 탄소 리포팅 30%
- **Platform Engineering** — Shift-Left 추진

→ 실습 확장 아이디어: ITAM 데이터(라이선스 보유) × FinOps 데이터(실사용량) 결합으로 **오버라이선싱/쉘프웨어 탐지**.

---

## 9. finops-lab 실습 로드맵 제안 (본 리포트 기반)

| 단계 | 랩 주제 | 기반 리포트 포인트 |
|---|---|---|
| **L1. 가시성** | FOCUS 포맷 변환기 (CUR → FOCUS) | §5, p.28–29 |
| **L2. Allocation** | 태그/메타데이터 기반 BU chargeback | §3, §8 |
| **L3. Forecasting** | 시계열 기반 월/분기 예측 모델 | §2 Top4, §7 |
| **L4. Unit Economics** | 요청당·사용자당·기능당 비용 계산 | §7, §6 |
| **L5. AI Cost Visibility** | LLM 토큰·GPU 사용량 대시보드 | §4.1, §4.2 |
| **L6. AI for FinOps** | 이상 탐지 + NL 쿼리 + 자동 Rightsizing | §4.3 |
| **L7. Shift-Left** | IaC 단계 비용 추정 + PR Gate | §6 |
| **L8. Governance** | 예산 초과 자동 차단 · 정책 자동 집행 | §7 |

---

## 10. 핵심 인용 (실습 동기 부여용)

> "We have hit the 'big rocks' of waste and now face a high volume of smaller opportunities that require more effort to capture."

> "The practice you have for governing public cloud spend should naturally include AI. It is simply another bucket of spend that requires the same discipline and governance as any other technology." — *Financial Services*

> "Is your AI providing value? No one can answer that question yet."

> "Dashboards are table stakes of yesterday — reactive. You have to move to proactive, real-time, automation."

> "Once you fix it, it's gone. How do we give developers credit for shift-left activities?"

---

## 부록: 참고 용어

- **FOCUS**: FinOps Open Cost and Usage Specification (이종 빌링 데이터 통일 스키마)
- **Shift-Left**: 개발/기획 단계로 비용 고려 이동
- **Unit Economics**: 거래·사용자·요청 단위 비용 분석
- **Scope Expansion**: Cloud 외 SaaS/Licensing/DC/AI로 FinOps 범주 확장
- **Allocation**: 비용을 팀/서비스/BU 단위로 귀속시키는 작업
- **Chargeback / Showback**: 사용한 만큼 내부 청구 / 보여주기

*원본 PDF: `references/finops/State of FinOps 2026 Report.pdf` · https://data.finops.org*
