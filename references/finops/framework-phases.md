# FinOps Framework — Phases (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/phases/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의
FinOps는 Framework Capabilities를 **세 단계(Inform → Optimize → Operate)**로 반복(iterative) 수행하며 실천됨.  
실무자는 조직의 기술 사용 현황을 살피며 세 단계를 빠르게 순환(cycle)함 — 현재 IT 환경 상태 파악(**Inform**),  
개선 방안 식별·문서화(**Optimize**), 가장 큰 가치를 만드는 변화를 구성원이 실행하도록 권한 부여(**Operate**).  
목표는 전략을 지속적으로 발전시키고 워크플로우를 정제하며, 결과를 측정하고 점진적 개선을 반복하여  
단계 순환에 필요한 시간을 줄이는 "근육 기억(muscle memory)"을 형성하는 것임.

## 공식 구성 항목 (영문 명칭 그대로)
페이지 본문에 명시된 항목만 기재함 (Principles·Domains·Maturity의 Crawl/Walk/Run 등은 본 페이지 본문에 없음).

- **3 Phases (각 단계의 부제는 페이지 표기 그대로)**  
  - **Inform** — "Visibility & Allocation"  
  - **Optimize** — "Rates & Usage"  
  - **Operate** — "Continuous Improvement & Usage"  
- **Inform 단계에서 언급된 Capabilities** (이 페이지가 Inform 활동으로 거론한 Capabilities이며, 프레임워크 전체 Capability 목록은 아님)  
  - Data Ingestion / Allocation / Reporting & Analytics / Forecasting / Unit Economics  
- **Optimize 단계의 두 최적화 축**  
  - **Usage optimization** — 허용 가능한 결과를 더 적은 리소스로 달성 (엔지니어링팀 협업 중심)  
  - **Rate optimization** — 반드시 써야 하는 리소스에 적정 금액 지불 (구매·리더십 협업 중심)  

## 교재 인용 포인트
1. finops-lab 4단계(WHY → Inform → Optimize → Operate) 중 후반 3단계는 본 페이지의 공식 3 Phases와 1:1 정렬됨  
   (WHY는 별도이며, 공식 프레임워크상 Phases는 Inform·Optimize·Operate 3개임을 교재에서 명확히 구분할 것).  
2. 세 단계는 선형이 아니라 **반복(iterative) 순환**이라는 점을 강조 — "Inform·Optimize로 계속 되돌아감(looping back)".  
3. `@inform` 단계 산출물은 본 페이지의 Inform 정의(비용·사용량·효율 데이터 검토, 정확한 Allocation→Reporting)와 정렬.  
4. `@optimize` 단계의 Right-sizing/RI·SP·Spot 시나리오는 **Usage vs Rate optimization** 2축으로 구조화하여 인용.  
5. `@operate` 단계의 자동화·게이트·리뷰 런북은 본 페이지의 "accountability culture / continuous, incremental action"  
   및 "Capability 성숙(maturing Capabilities)" 서술과 정렬.

## 원문 핵심 인용 (verbatim)
> "FinOps is performed by working iteratively on the Framework Capabilities through three phases: Inform, Optimize and Operate."

> "Optimization options may include both usage optimization (using fewer resources to achieve an acceptable outcome) and rate optimization (paying an appropriate amount for the resources we must use)."

> "Working through this phase, keep in mind the goal to iteratively enact optimization strategies and refine workflows; this involves looping back to the Inform and Optimize phases continuously."
