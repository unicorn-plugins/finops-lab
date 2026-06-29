# FinOps Framework — Framework Overview (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.  
> 페이지 상 `dateModified`: 2026-02-17, 라이선스: CC BY 4.0.

## 핵심 정의
FinOps Framework(프레임워크)는 FinOps 실천에 필요한 구성요소를 정의한 공식 체계임.  
페이지 `<title>`은 "FinOps Framework Overview"이며, 프레임워크는 7개 구성요소(Principles, Personas, Phases,  
Maturity Model, Domains, Capabilities, Scopes)로 구성됨 (JSON-LD `hasPart` 및 카드 그리드 기준).  
핵심 관계 정의(본문 verbatim): "**Domains** are the outcomes of a FinOps practice & **Capabilities** describe how to  
achieve them." — 즉 Domain(영역)은 FinOps 실천의 성과(outcome), Capability(역량)는 그 성과를 달성하는 방법(how)임.  
Scope(범위) 정의: FinOps Scope는 제품·코스트센터·환경 등 비즈니스 구성에 정렬된, 기술 가치를 극대화하기 위한  
기술 관련 지출의 정의된 세그먼트임.

## 공식 구성 항목 (영문 명칭 그대로)

### 7대 구성요소 (7 Framework components)
Principles · Personas · Phases · Maturity Model · Domains · Capabilities · Scopes  
(각 구성요소의 본문 verbatim 한줄 설명)  
- **Principles**: "Understand the principles of FinOps that create financial accountability through collaboration and  
  drive business value for technology spend." (※ 본 Overview 페이지 본문에는 6개 개별 Principle 명칭이 열거되지 않음 —  
  하위 페이지 `/framework/principles/` 참조 필요)
- **Personas**: "The FinOps discipline covers many different personas, understand more about them, their roles, and  
  requirements."
- **Phases**: "The FinOps journey consists of Inform, Optimize and Operate. Understand more about each phase and how to  
  get started." → 3 Phases: **Inform · Optimize · Operate**
- **Maturity Model**: "A FinOps approach of "Crawl, Walk, Run" enables organizations to start small, and grow in scale,  
  scope, and complexity." → 3단계: **Crawl · Walk · Run**
- **Domains**: "FinOps Domains represent a sphere of activity or knowledge that organizations will perform."
- **Capabilities**: "FinOps Capabilities represents functional areas of activity in support of their corresponding  
  FinOps Domains."
- **Scopes**: "A FinOps Scope is a defined segment of technology-related spending – aligned to business constructs such  
  as products, cost centers, or environments – that guide the application of FinOps to maximize technology value."

### 4 Domains와 소속 Capabilities (본문 verbatim, 총 22 Capabilities)
1. **Understand Usage & Cost** — Data Ingestion · Allocation · Reporting & Analytics · Anomaly Management
2. **Quantify Business Value** — Planning & Estimating · Forecasting · Budgeting · KPIs & Benchmarking · Unit Economics
3. **Optimize Usage & Cost** — Architecting & Workload Placement · Usage Optimization · Rate Optimization ·  
   Licensing & SaaS · Sustainability
4. **Manage the FinOps Practice** — Executive Strategy Alignment · FinOps Practice Operations · Governance, Policy & Risk ·  
   FinOps Education & Enablement · Invoicing & Chargeback · FinOps Assessment · Automation, Tools & Services ·  
   Intersecting Disciplines

### Personas (페르소나)
- **Core Personas** ("are always engaged in a FinOps practice"): FinOps Practitioner · Engineering · Finance ·  
  Leadership · Procurement · Product
- **Allied Personas** ("support a FinOps practice"): ITAM · ITFM · ITSM · Security (그 외 항목은 `/framework/personas/` 참조)

### Technology Categories (Scopes와 연동, 본문 탭 기준)
AI · Public Cloud · SaaS · Data Platform · Private Cloud · Licenses · Data Center (+)

### 2026 Framework 업데이트 (본문 명시)
"2026 Framework Updates: Executive Strategy Alignment, Refining Scopes"

## 교재 인용 포인트
1. FinOps 4단계(WHY → Inform → Optimize → Operate) 중 Inform·Optimize·Operate는 공식 **Phases**와 1:1 정렬됨 —  
   교재의 phase 명칭을 공식 영문(Inform/Optimize/Operate) 그대로 사용.
2. 성숙도 단계는 공식 **Maturity Model**의 Crawl·Walk·Run을 그대로 인용 (operate 스킬의 Crawl→Walk 12개월 전환 근거).
3. Domain↔Capability 관계는 "Domains = outcomes, Capabilities = how"로 인용하여 교재의 영역/역량 구분 근거로 사용.
4. inform 스킬의 이상탐지·태깅·리포팅은 공식 Capability(Anomaly Management, Allocation, Reporting & Analytics,  
   Data Ingestion)로 역참조 가능 — "Understand Usage & Cost" Domain 소속.
5. optimize 스킬의 right-sizing·RI/SP/Spot은 "Optimize Usage & Cost" Domain의 Usage Optimization·Rate Optimization·  
   Architecting & Workload Placement Capability로 역참조.

## 원문 핵심 인용 (verbatim)
> "**Domains** are the outcomes of a FinOps practice & **Capabilities** describe how to achieve them." — 본문 H2

> "The FinOps journey consists of Inform, Optimize and Operate. Understand more about each phase and how to get started." — Phases 카드

> "A FinOps approach of "Crawl, Walk, Run" enables organizations to start small, and grow in scale, scope, and complexity." — Maturity Model 카드

> "A FinOps Scope is a defined segment of technology-related spending – aligned to business constructs such as products, cost centers, or environments – that guide the application of FinOps to maximize technology value." — Scopes 카드
