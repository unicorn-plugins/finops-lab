# FinOps Framework — Principles (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/principles/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의
FinOps Principles(원칙)는 FinOps 실무 활동을 안내하는 북극성(north star) 역할을 함.  
공식 문구: "FinOps Principles act as a north star, guiding the activities of our FinOps practice."  
6개 원칙은 우선순위(순서)가 없으며 각각이 FinOps 성공에 똑같이 중요함 — 회원은 6개 원칙을  
모두 이해하고 실천하도록 권장됨("These principles are in no particular order, and they are each  
important to FinOps success.").  
CC BY 4.0 라이선스로 공개되며, 사용·각색 시 출처 표기(attribution)가 요구됨.

## 공식 구성 항목 (영문 명칭 그대로)
6 Principles (페이지 표기 순서, verbatim):  
1. Teams need to collaborate  
2. Business value drives technology decisions  
3. Everyone takes ownership for their technology usage  
4. FinOps data should be accessible, timely, and accurate  
5. FinOps should be enabled centrally  
6. Take advantage of the variable cost model of the cloud  

각 원칙의 핵심 설명(페이지 본문 발췌):  
- Teams need to collaborate — "Finance, technology, product, and leaders work together to manage each  
  technology category at the speed and granularity each requires." 효율·혁신을 위해 임원~엔지니어,  
  전 Persona가 가장 가치 있는 전략 목표에 집중하도록 협업함.  
- Business value drives technology decisions — "Unit economic and value-based metrics demonstrate  
  business impact better than just aggregate or categorized technology spend." 비용·품질·속도 간  
  의식적 트레이드오프 결정, FinOps Scopes로 조직 목표별 비즈니스 가치를 타깃함.  
- Everyone takes ownership for their technology usage — "Accountability of usage and cost is pushed to  
  the edge, with engineers taking ownership of costs from architecture design to ongoing operations."  
  비용을 SDLC 시작부터 1급(first class) 지표로 다루며 의사결정을 분산화함.  
- FinOps data should be accessible, timely, and accurate — "Process and share cost data as soon as it  
  becomes available." 실시간 가시성·빠른 피드백 루프가 더 효율적 행동을 유도하고, FOCUS 등으로  
  데이터 정규화·정확성·일관성을 지속 개선함.  
- FinOps should be enabled centrally — "A centralized FinOps function encourages, evangelizes, and  
  enables best practices in a shared accountability model." Rate·commitment·discount 최적화는  
  규모의 경제를 위해 중앙화하는 것이 최선이며, 그 결과 엔지니어는 사용량 최적화에 집중 가능.  
- Take advantage of the variable cost model of the cloud — "Each technology category — public cloud,  
  data center, SaaS, Licenses, Data Cloud Platforms, etc. — entails cost models that have pros and cons  
  for any business." 클라우드의 가변 비용 모델, 데이터센터의 고정 비용 모델 등 각 모델이 더 많은  
  가치를 전달할 기회를 제공함("The variable cost model of the cloud, the fixed cost model of the data  
  center, or other models present opportunities to deliver more value.").  

## 교재 인용 포인트
1. FinOps 3대 가치·WHY 정렬 시, 6개 원칙을 "우선순위 없는 동등한 북극성"으로 인용 —  
   특정 원칙만 강조하지 않도록 주의("in no particular order").  
2. Ownership 전환 서사("Everyone takes ownership")는 비용을 SDLC 시작부터 first-class 지표로 다루는  
   근거로 인용 — @why-finops Ownership×Capability 진단과 연결.  
3. "FinOps should be enabled centrally" 원칙은 Rate/commitment/discount(RI·SP) 최적화 중앙화 논거로  
   @optimize 약정 시나리오·@operate 중앙 거버넌스 설계에 인용.  
4. "FinOps data should be accessible, timely, and accurate"는 FOCUS 정규화·실시간 가시성 대시보드  
   (@inform)의 1차 근거로 인용 — FOCUS가 원칙 본문에 명시적으로 등장함.  
5. "Business value drives technology decisions"는 단위경제(unit economic)·가치 기반 지표(@operate KPI)의  
   직접 근거 — 집계 지출보다 단위경제가 비즈니스 임팩트를 더 잘 보여준다는 문구 인용.  

## 원문 핵심 인용 (verbatim)
> "FinOps Principles act as a north star, guiding the activities of our FinOps practice."  
> "These principles are in no particular order, and they are each important to FinOps success. We  
> encourage members to understand and practice all of these principles."  
> "Accountability of usage and cost is pushed to the edge, with engineers taking ownership of costs  
> from architecture design to ongoing operations."  
