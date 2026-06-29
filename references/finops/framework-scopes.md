# FinOps Framework — Scopes (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/scopes/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의

FinOps Scope(스코프)는 **기술 카테고리 전반에 걸친 정의된 지출 세그먼트(a defined segment of spending  
across technology categories)** 로, 제품·코스트센터·환경 같은 **비즈니스 구성요소(business constructs)** 에  
정렬되어 기술 가치 극대화를 위한 FinOps 적용을 안내함.  
Scope는 **의사결정 컨텍스트(decision context)** 와 공유 기준점을 설정하여, 어떤 Personas를 참여시키고  
어떤 Capabilities를 적용하며 어떤 Domains로 성공을 정의할지 결정하는 **practice profile**을 형성함.  
핵심 원칙: Scope는 **인프라/기술 경계가 아니라 비즈니스 컨텍스트로 정의됨** (Scopes Reflect Decision  
Context, Not Infrastructure Boundaries). 동일 기술 사용이 서로 다른 비즈니스 목표 때문에 복수 Scope에  
동시에 포함될 수 있으며, 상호 배타적이지 않음(not always mutually exclusive).  
하나의 FinOps practice는 통상 **복수의 Scope를 profile의 일부로 정의**하며, 새 Scope는 더 나은 의사결정을  
가능하게 할 때만(distinct business outcome·constraint·decision context) 도입하고 최소·단순하게 유지함.

## 공식 구성 항목 (영문 명칭 그대로)

### 명명된 5개 FinOps Scopes (페이지 내장 JSON-LD `DefinedTermSet` "FinOps Scopes")

1. **FinOps for Public Cloud** (`/framework/scope/public-cloud/`)  
2. **FinOps for SaaS** (`/framework/scope/saas/`)  
3. **FinOps for Data Center** (`/framework/scope/data-center/`)  
4. **FinOps for Data Cloud Platforms** (`/framework/scope/finops-for-data-cloud-platforms/`)  
5. **FinOps for AI** (`/framework/scope/finops-for-ai/`)  

### 본문 설명 섹션 제목 (H3, verbatim)

- Scopes Are Driven by the Business & Technology Strategy  
- Scopes Reflect Decision Context, Not Infrastructure Boundaries  
- Scopes Determine How Personas, Domains, and Capabilities are Engaged  
- Only Create a New Scope When It Enables Better Decisions  
- How FinOps Scopes Evolve  
- How Business Questions Lead to FinOps Scopes  
- The Lifecycle and Interaction of FinOps Scopes  

### Scope가 참조하는 Framework 빌딩블록 (verbatim)

Personas / Domains / Capabilities (예: Data Ingestion, Allocation, Forecasting) — Scope별로 KPI·maturity·  
measures of success가 tailored됨. 비즈니스 질문→Scope 도출 기법으로 **Five whys** 제시.

## 교재 인용 포인트

1. **Scope = 비즈니스 컨텍스트 기반 지출 세그먼트** 임을 강조 — "기술이 어디서 도는가"가 아니라  
   "비즈니스가 무엇에 투자하는가"로 Scope를 정의(특히 AI 투자 사례).  
2. HBT 멀티클라우드 + SaaS LLM 시나리오를 **FinOps for Public Cloud + FinOps for AI** 두 Scope로  
   매핑 — 공식 5개 명명 Scope 중 해당 2종을 직접 인용 가능.  
3. **하이브리드 Kubernetes(public cloud + 데이터센터 온프레)** 예시는 공식 페이지의 본문 예시와 일치 —  
   교재의 멀티클라우드/하이브리드 사례 정당화 근거로 사용.  
4. Scope는 **상호 배타적이지 않음** — 클라우드 Scope와 Agentic AI Scope가 겹치는 forecast variance  
   관리 사례를 운영(Operate) 단계 리뷰 런북의 근거로 인용.  
5. 새 Scope 남발 금지(few·simple·purposeful) 원칙 — WHY 정의 단계에서 "왜 별도 Scope가 필요한가"를  
   Five whys로 검증하는 절차의 1차 출처로 인용.

## 원문 핵심 인용 (verbatim)

> "A FinOps Scope is a defined segment of spending across technology categories, aligned to business  
> constructs–such as product, cost center, or environment–that guide the application of FinOps to maximize  
> technology value." — 공식 정의 (Scopes 페이지 본문)

> "FinOps Scopes are not created because a topic is interesting or because a Practitioner wants to analyze a  
> new area of spend. They are initiated in response to explicit business expectations, most often surfaced  
> through questions from Leadership." — 비즈니스 질문 기반 Scope 도출

> "It is also important to recognize that FinOps Scopes are not always mutually exclusive. Technology usage  
> may be included within multiple Scopes at the same time, particularly when different business outcomes or  
> expectations apply." — Scope 간 상호작용/중첩
