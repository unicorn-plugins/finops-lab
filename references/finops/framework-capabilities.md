# FinOps Framework — Capabilities (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/capabilities/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.  
> 수집 정합성: 본문 핵심(공식 정의·Capability 18종·라이선스)은 정적 HTML(JSON-LD + meta)에서 verbatim 수신 성공.  
> 단, 페이지 본문의 카드/필터(Domain 그룹·Persona·Metric)는 JavaScript 렌더링이라 curl로 미수신 — 아래 caveats 참조.

## 핵심 정의
FinOps Capabilities(역량)는 FinOps 실무 자체의 과제를 해결하기 위해 필요한 활동 영역(areas of activity)을 의미함.  
공식 정의(JSON-LD `description`, verbatim): "FinOps Capabilities represent the areas of activity required to meet  
the challenges of the FinOps practice itself."  
각 Capability는 해당 FinOps **Domain**을 지원하는 기능 영역(functional area)이며,  
정의(definitions)·핵심 페르소나(key personas)·성과 지표(performance metrics)·기능 활동(functional activities)을 포함함  
(출처: 페이지 meta description, verbatim).  
Capability는 FinOps Persona 전반에 걸쳐 실행 가능한 과업을 연결하는 빌딩 블록(building blocks)이며,  
기술 가치·의사결정을 비즈니스 목표(business objectives)에 정렬하는 역할을 함 (출처: JSON-LD webpage `description`, verbatim).

## 공식 구성 항목 (영문 명칭 그대로)
### Capabilities 18종 (slug → 공식 display name)
slug은 상위 페이지 JSON-LD `hasPart`(verbatim), display name은 각 Capability 하위 페이지의 `<title>`/`<h1>`(verbatim, 개별 curl 확인)에서 확인함.  
slug과 display name이 크게 다른 항목이 다수이므로 교재 인용 시 반드시 아래 공식 display name 사용 권장.

1. `allocation` → **Allocation**  
2. `anomaly-management` → **Anomaly Management**  
3. `architecting-for-cloud` → **Architecting & Workload Placement**  
4. `benchmarking` → **KPIs & Benchmarking**  
5. `budgeting` → **Budgeting**  
6. `cloud-sustainability` → **Sustainability**  
7. `data-ingestion` → **Data Ingestion**  
8. `finops-assessment` → **FinOps Assessment**  
9. `finops-tools-services` → **Automation, Tools, & Services**  
10. `forecasting` → **Forecasting**  
11. `invoicing-chargeback` → **Invoicing & Chargeback**  
12. `intersecting-disciplines` → **Intersecting Disciplines**  
13. `licensing-saas` → **Licensing & SaaS**  
14. `planning-estimating` → **Planning & Estimating**  
15. `policy-governance` → **Governance, Policy & Risk**  
16. `rate-optimization` → **Rate Optimization**  
17. `reporting-analytics` → **Reporting & Analytics**  
18. `finops-practice-operations` → **FinOps Practice Operations**

### 라이선스·메타
- 라이선스: Creative Commons BY 4.0 (JSON-LD `license`, verbatim)  
- 발행: FinOps Foundation, 언어 en  
- 상위 구조: 본 termset은 `https://www.finops.org/framework/#framework`의 일부(`isPartOf`)이며, Domains 페이지와 관련됨(`relatedLink`)

## 교재 인용 포인트
1. Capability 명칭은 slug이 아닌 **공식 display name**으로 인용함 — 특히 `benchmarking`="KPIs & Benchmarking",  
   `architecting-for-cloud`="Architecting & Workload Placement", `policy-governance`="Governance, Policy & Risk",  
   `finops-tools-services`="Automation, Tools, & Services", `cloud-sustainability`="Sustainability"는 slug과 의미 차이가 큼.  
2. Capability를 "FinOps 실무의 활동 영역(building blocks)"으로 정의하고, 각 Capability가 Domain을 지원한다는 계층 관계로 인용함.  
3. 교재에서 finops-lab 단계(Inform/Optimize/Operate)에 Capability를 매핑할 때, 본 18종을 표준 마스터로 사용함  
   (단, Domain↔Capability 정확한 그룹핑은 본 페이지 curl로 미확정 — Domains 페이지 별도 1차 출처 필요).  
4. 각 Capability 정의는 하위 페이지 meta description이 1차 출처임(예: Allocation/Anomaly Management 정의는 아래 원문 참조).  
5. 브리프 기대 키워드 중 "Workload Optimization"·"Unit Economics"는 본 18종에 **명칭 그대로는 부재** —  
   구 프레임워크 용어로 보이며, 교재 인용 시 현행 명칭(예: Architecting & Workload Placement 등)으로 정렬 필요.

## 원문 핵심 인용 (verbatim)
> "FinOps Capabilities represent the areas of activity required to meet the challenges of the FinOps practice itself.  
> They can be thought of as building blocks that enable and bridge actionable tasks across FinOps Personas,  
> and align technology value and decisions with business objectives." — JSON-LD webpage `description`

> "FinOps Capabilities represents functional areas of activity in support of their corresponding FinOps Domains.  
> Each Capability includes definitions, key personas, performance metrics, and functional activities involved  
> in a real FinOps practice." — meta description

> "A set of outcome- and activity-oriented capability definitions within the FinOps Framework to be applied  
> to business structures and the technology categories that they manage." — JSON-LD DefinedTermSet `description`

> "Allocation defines how costs should be apportioned to those responsible for each component of that cost,  
> whether directly or as a shared element." — Allocation 하위 페이지 meta description

> "Anomaly Management gives a FinOps team the ability to detect, identify, clarify, alert on, and manage  
> unexpected cost events in a timely manner, in order to minimize impact to the business." — Anomaly Management 하위 페이지 meta description

> "Assessment of the FinOps practice allows a FinOps team to measure its own effectiveness, map its activities  
> against the goals of the organization, and identify areas where it will be valuable to mature those activities."  
> — FinOps Assessment 하위 페이지(<https://www.finops.org/framework/capabilities/finops-assessment/>) meta description (curl 검증: 2026-06-09, HTTP 200)

## ⚠️ 수집 한계 (curl 미확인 항목)
- 상위 Capabilities 페이지 본문(`#capabilities-search-hits`, `#domain-filter`)은 Algolia/JS 렌더링으로 정적 HTML에 비어 있음.  
- 따라서 **Domain 4종의 명칭·Capability↔Domain 그룹핑·Persona·Performance Metric**은 본 페이지 curl로 미수신 — 추측 기재하지 않음.  
- 위 18종 display name·정의는 각 하위 Capability 페이지(server-rendered title/meta)를 개별 curl하여 verbatim 확인한 것임.  
- Crawl/Walk/Run 성숙도 모델은 본 페이지 주제 아님(별도 Maturity 페이지 출처 필요).
