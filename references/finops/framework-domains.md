# FinOps Framework — Domains (1차 출처 요약)

> 출처: FinOps Foundation — <https://www.finops.org/framework/domains/> (curl 수집: 2026-06-09)  
> 본 문서는 공식 페이지에서 finops-lab 교재 인용에 필요한 핵심만 추출·정리한 요약본임.

## 핵심 정의
Domains(도메인)는 FinOps 실천의 **결과(outcomes)** 임 — "Domains are the outcomes of a FinOps practice."  
FinOps Framework의 Domains는 조직이 FinOps 실천을 통해 달성해야 할 **근본적 비즈니스 성과**를 기술함.  
즉, FinOps 실천으로 조직은 클라우드 사용·비용을 **이해(understand)** 하고, 그 **비즈니스 가치를 정량화(quantify)** 하며,  
**사용량과 지불 단가를 모두 최적화(optimize)** 하고, **효과적인 실천 체계를 관리(manage)** 함.  
각 Domain은 해당 성과를 달성하기 위해 수행하는 **Capabilities(역량) 집합**을 기술함.  
조직은 자신의 필요와 현재 **FinOps Maturity Level**에 따라 가치를 주는 Capability를 선별적으로 개발함 —  
모든 조직이 모든 Capability에 투자하지는 않으나, 클라우드를 사용하는 모든 조직은 **4개 Domain 전부에서 활동을 수행**함.

## 공식 구성 항목 (영문 명칭 그대로)
FinOps Domains = **4개 Domain / 총 22개 Capabilities**. 첫 3개 Domain은 클라우드 사용 성공에 필요한 실천,  
4번째 Domain은 FinOps 실천 자체를 성공시키는 활동을 기술함. (Domain은 순차적 단계가 아니라 **병렬 추진**됨.)

### 1) Understand Usage & Cost (4 Capabilities)
- Data Ingestion  
- Allocation  
- Reporting & Analytics  
- Anomaly Management  

### 2) Quantify Business Value (5 Capabilities)
- Planning & Estimating  
- Forecasting  
- Budgeting  
- KPIs & Benchmarking  
- Unit Economics  

### 3) Optimize Usage & Cost (5 Capabilities)
- Architecting & Workload Placement  
- Rate Optimization  
- Usage Optimization  
- Sustainability  
- Licensing & SaaS  

### 4) Manage the FinOps Practice (8 Capabilities)
- FinOps Practice Operations  
- Governance, Policy & Risk  
- FinOps Assessment  
- Automation, Tools, & Services  
- FinOps Education & Enablement  
- Invoicing & Chargeback  
- Intersecting Disciplines  
- Executive Strategy Alignment  

## 교재 인용 포인트
1. finops-lab 4단계(WHY → Inform → Optimize → Operate)는 공식 4 Domain과 정렬됨 —  
   Inform↔Understand Usage & Cost, (가치 정량화)↔Quantify Business Value, Optimize↔Optimize Usage & Cost,  
   Operate↔Manage the FinOps Practice. 교재 단계명을 공식 Domain 영문명과 병기하여 추적성 확보.  
2. @inform 단계의 산출물(데이터 수집·태깅·이상탐지·대시보드)은 **Data Ingestion / Allocation /  
   Reporting & Analytics / Anomaly Management** Capability에 1:1 매핑하여 근거를 표기.  
3. @optimize 단계의 Right-sizing·RI/SP/Spot·GPU 활용은 **Usage Optimization / Rate Optimization /  
   Architecting & Workload Placement** Capability로 정렬. 모델 다운그레이드·SaaS LLM은 **Licensing & SaaS** 참조.  
4. @operate 단계의 단위경제 KPI는 Quantify의 **Unit Economics / KPIs & Benchmarking**, 게이트·자동화·런북은  
   Manage의 **Governance, Policy & Risk / Automation, Tools, & Services / FinOps Practice Operations**로 매핑.  
5. "Domain은 순차 단계가 아니라 병렬 추진"이라는 공식 문장을 인용하여, 교재의 4단계를 **순차 워크플로우가 아닌  
   상호의존적 운영 모델**로 설명할 때 근거로 사용.

## 원문 핵심 인용 (verbatim)
> "Domains are the outcomes of a FinOps practice." — 영문 원문 그대로 (추적성용)

> "Each Domain describes a set of Capabilities an organization can perform to achieve these outcomes." — 영문 원문 그대로

> "Domains are not steps in a serial process. Activities in multiple Domains will be pursued in parallel while an organization builds Capabilities for their FinOps practice." — 영문 원문 그대로
