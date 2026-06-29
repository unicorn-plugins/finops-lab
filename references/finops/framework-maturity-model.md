# FinOps Framework — Maturity Model (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/maturity-model/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의
FinOps 실천(practice of FinOps)은 본질적으로 반복적(iterative)이며, 모든 프로세스·기능 활동·Capability·Domain의  
성숙도(maturity)는 반복 수행을 통해 향상됨.  
공식 페이지는 성숙도를 **"Crawl, Walk, Run" 접근법**으로 표현함 — 조직이 작게 시작(start small)하여 비즈니스 가치가  
정당화하는 만큼 규모(scale)·범위(scope)·복잡도(complexity)를 키워 나가는 방식임.  
작고 제한된 범위에서 빠르게 행동(quick action at a small scale)하면 FinOps 팀이 결과를 평가하고, 더 크거나·빠르거나·  
세밀하게 추가 행동할 가치에 대한 통찰을 얻을 수 있음.  
이 성숙도 designation은 조직의 Capability·Domain이 **현재 어느 수준에서 운영 중인지 식별**하고, Crawl→Walk 또는  
Walk→Run으로 이동하고 싶은 영역을 식별하는 데 사용됨.  

## 공식 구성 항목 (영문 명칭 그대로)
3단계 성숙도 레벨(maturity designations): **Crawl · Walk · Run**  
각 레벨은 페이지에서 두 블록으로 기술됨 — `Maturity Level Characteristics`(특성)와  
`Sample goals/KPI from the FinOps Community (data.finops.org)`(샘플 목표/KPI).  

### Crawl
- Maturity Level Characteristics  
  - Very little reporting and tooling  
  - Measurements only provide insight into the benefits of maturing the capability  
  - Basic KPIs set for the measurement of success  
  - Basic processes and policies are defined around the capability  
  - Capability is understood but not followed by all the major teams within the organization  
  - Plans to address "low hanging fruit"  
- Sample goals/KPI (data.finops.org)  
  - Able to allocate at least 70% of cost to known owner  
  - Commitments discount target coverage of approximately 60%  
  - Forecast spend to actual spend accuracy variance is below 20%  

### Walk
- Maturity Level Characteristics  
  - Capability is understood and followed within the organization  
  - Difficult edge cases are identified but decision to not address them (informed ignoring) is adopted  
  - Automation and/or processes cover most of the Capability requirements  
  - Most difficult edge cases (ones that threaten the financial well-being of the organization) are identified  
    and effort to resolve has been estimated  
  - Medium to high goals/KPIs set on the measurement of success  
- Sample goals/KPI (data.finops.org)  
  - Able to allocate at least 85% of cost to known owner  
  - Commitments discount target coverage is greater than 75%  
  - Forecast spend to actual spend accuracy variance is less than 10%  

### Run
- Maturity Level Characteristics  
  - Capability is understood and followed by all teams within the organization  
  - Difficult edge cases are being addressed  
  - Very high goals/KPIs set on the measurement of success  
  - Automation is the preferred approach  
- Sample goals/KPI (data.finops.org)  
  - Greater than 90% of spend can be allocated  
  - Commitment discount target coverage is greater than 80 (원문 표기 그대로 — 단위 % 미표기)  
  - Forecast spend to actual spend accuracy variance is less than 5%  

## 교재 인용 포인트
- finops-lab 교재의 "Crawl→Walk 12개월 전환"(operate) 서술은 본 공식 3단계(Crawl·Walk·Run)에 정렬해야 함 —  
  특히 "모든 Capability를 Run으로 끌어올리는 것을 목표로 삼지 말라"는 공식 경고를 명시 인용 권장.  
- 비즈니스 가치 우선 원칙: 공식 페이지는 "Prioritize maturing the Capabilities that provide your organization the  
  highest business value." 라고 단정함 → 교재의 우선순위·게이트 설계 근거로 인용 가능.  
- 정량 임계값(allocation 70/85/90%, commitment coverage 60/75/80%, forecast variance 20/10/5%)은  
  data.finops.org 커뮤니티 **샘플** 값임을 반드시 병기 — 절대 기준이 아닌 가이드라인임을 명확히 할 것.  
- "informed ignoring"(Walk 단계 edge case 처리 정책)은 교재 운영 런북의 예외 처리 정책 근거로 인용 가능.  
- 성숙도는 Capability·Domain별로 개별 측정됨("Every Capability and functional activity can be at a different  
  level of maturity") → 교재의 성숙도 진단을 단일 점수가 아닌 Capability별 진단으로 설계할 근거.  

## 원문 핵심 인용 (verbatim)
> "A "Crawl, Walk, Run" approach to performing FinOps enables organizations to start small, and grow in scale,  
> scope, and complexity as business value warrants maturing a functional activity." — 영문 원문 그대로  

> "These terms are general guidelines, and an organization's goal should never be simply to achieve a "Run"  
> maturity in every Capability." — 영문 원문 그대로  

> "Prioritize maturing the Capabilities that provide your organization the highest business value." — 영문 원문 그대로  
