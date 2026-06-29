# FinOps Framework — Technology Categories (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/technology-categories/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의

Technology Categories(기술 카테고리)는 조직이 IT 리소스·서비스를 소비하고 지출하는 기술의 유형(types of technology)을 의미함.  
각 카테고리는 고유의 조달 모델(procurement models), 가격 구조(pricing constructs), 비용 가시성 특성(cost visibility  
characteristics), 운영 동학(operational dynamics)을 가지며, 이 차이가 FinOps를 적용하는 방식을 결정함.  
각 카테고리 페이지는 FinOps Scopes 정의 고려사항, FinOps Capabilities가 핵심 활동을 어떻게 지원하는지, FinOps Personas의  
관여 방식, 성공을 측정하는 KPI·지표, 그리고 각 카테고리의 청구·사용 데이터를 FOCUS(FinOps Open Cost and Usage  
Specification)로 통합하는 방법을 설명함.

## 공식 구성 항목 (영문 명칭 그대로)

본 페이지가 정의하는 Technology Categories는 다음 5종임 (페이지 H3 제목 verbatim):

- **FinOps for SaaS** — 관리형 소프트웨어(managed software) 지출의 거버넌스·최적화. 분권화된 구매 모델 전반의 가시성·  
  책임성·데이터 기반 의사결정을 위해 SaaS 사용 데이터에 FinOps Capabilities를 적용함.
- **FinOps for Data Center** — 온프레미스 인프라 투자에 대한 가시성·의사결정 개선. 용량·소비·비즈니스 수요를 정렬하는  
  계획(planning)·할당(allocation)·최적화(optimization) 의사결정 지원을 위해 데이터센터 사용·비용에 Capabilities를 적용함.
- **FinOps for Data Cloud Platforms** — 소비 기반(consumption based) 데이터·분석 지출의 거버넌스·최적화. 쿼리·작업·  
  파이프라인·플랫폼 메타데이터 등 워크로드 텔레메트리에 Capabilities를 적용해 공유 컴퓨트 전반의 책임성을 강화함.
- **FinOps for AI** — 비용 복잡성, 빠른 개발 주기, 지출 예측 불가능성, 그리고 더 높은 수준의 정책·거버넌스 필요성을  
  다루며, 소비·투자·비즈니스 가치를 정렬하는 할당(allocation)·예측(forecasting)·최적화 의사결정으로 혁신을 지원함.
- **FinOps for Public Cloud** — 비용 효율성·확장성·전달 속도 등 비즈니스 성과를 위한 클라우드 기반 소비의 관리·최적화.  
  정보 기반 의사결정·공유 책임성·클라우드 투자와 비즈니스 가치의 지속적 정렬을 위해 클라우드 사용에 Capabilities를 적용함.

> 참고: 기대 키워드였던 "Licensing"은 본 페이지에 독립된 카테고리("FinOps for Licensing")로 존재하지 않음 (본문에 2회  
> 우발적으로만 등장). 날조 방지를 위해 카테고리 목록에 포함하지 않음 (caveats 참조).

## 교재 인용 포인트

1. HBT 멀티클라우드 + SaaS LLM 시나리오는 본 페이지의 **FinOps for Public Cloud**(3 CSP) + **FinOps for SaaS**(SaaS LLM) +  
   **FinOps for AI**(FinOps for AI 확장)에 정확히 매핑됨 — `@inform`·`@optimize` 단계의 기술 범위 근거로 인용 가능.
2. 각 카테고리가 "고유 조달 모델·가격 구조·비용 가시성·운영 동학"을 가진다는 정의는 멀티클라우드/멀티기술 정규화의  
   필요성(FOCUS 정렬)을 정당화하는 1차 출처로 사용 가능.
3. 페이지가 명시한 "각 카테고리의 청구·사용 데이터를 FOCUS로 통합" 문장은 `@inform`의 FOCUS 정규화 작업이  
   FinOps Foundation 공식 권고와 정렬됨을 보이는 근거로 직접 인용 가능.
4. Technology Categories는 Scopes·Personas·Capabilities·KPI를 가로지르는 횡단(cross-cutting) 렌즈임을 명시 — 교재에서  
   "기술 카테고리 × Capabilities" 교차표를 만들 때 출처로 인용 가능.
5. **FinOps for AI**의 정의(비용 복잡성·예측 불가능성·강한 거버넌스 필요)는 `@optimize`의 GPU 활용·모델 다운그레이드,  
   `@operate`의 게이트·정책 설계 WHY를 뒷받침하는 공식 근거로 인용 가능.

## 원문 핵심 인용 (verbatim)

> "Technology categories represent types of technology through which organizations consume and spend on IT resources and  
> services, each with its own procurement models, pricing constructs, cost visibility characteristics, and operational  
> dynamics that shape how FinOps is applied." — 영문 원문 그대로 (추적성용)

> "Each technology category page describes considerations for defining FinOps Scopes, explains how FinOps Capabilities  
> support key activities, how FinOps Personas are involved, which KPIs and metrics help measure success, and how billing  
> and usage data from each category can be unified using the FinOps Open Cost and Usage Specification (FOCUS)." — 영문 원문 그대로

> "FinOps for AI — Addressing the cost complexity, faster development cycle, spend unpredictability, and the need for a  
> greater degree of policy and governance to support innovation through allocation, forecasting, and optimization  
> decisions that align consumption, investment, and business value." — 영문 원문 그대로
