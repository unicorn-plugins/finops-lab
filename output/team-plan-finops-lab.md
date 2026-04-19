# 팀 기획서

## 기본 정보
- 플러그인명: finops-lab
- 목표: FinOps 교재(3단계 순환 — **보이기(Inform) → 줄이기(Optimize) → 체계화(Operate)**)와
  2025-2026 프레임워크 업데이트(FOCUS · Ownership×Capability · Cloud+)를
  **WHY 정의 → FOCUS 정규화·가시화 → 최적화 권고 → 지속 운영 체계화** 4단계로
  가상 기업 (주)하이브리지텔레콤(HBT) 데이터를 손으로 돌려보며 체득
- 대상 도메인: 멀티클라우드 FinOps · **FinOps for AI(LLM 토큰·GPU)** · 비용 거버넌스 · 단위경제(Unit Economics) · 이상 비용 탐지
- 대상 사용자: FinOps 실무자/팀장, 클라우드 아키텍트, DevOps/SRE 엔지니어,
  CCoE(Cost Center of Excellence) 준비 조직, 재무·사업부 Cost Owner

---

## 핵심기능
- **@why-finops (WHY 정의)**: 기업 비즈니스 이슈를 FinOps 3대 가치(투자가치 극대화·비용 최적화·문화 정착)에
  매핑하고, Ownership×Capability 기반 성숙도(Crawl/Walk/Run) 자가진단, COVERS 6원칙 정렬,
  12개월 스킬셋 로드맵(AI Cost · Tooling · Automation · Forecasting) 수립
- **@inform (보이기)**: 3 CSP 샘플 빌링(AWS CUR 2.0 · Azure Cost Export · GCP Billing Export) +
  **AI 사용량 샘플(LLM 토큰·GPU 시간 — OpenAI/Anthropic API · Vertex AI · GPU 인스턴스)**을
  **FOCUS v1.3 통합 스키마(+ AI 확장 컬럼)**로 정규화·병합, 태깅 거버넌스 갭·이상 비용(Anomaly) 자동 탐지,
  서비스·CostCenter·Project·**모델/토큰/GPU** 축 **인터랙티브 웹 대시보드(HTML + Chart.js, 단일 파일)** 생성
- **@optimize (줄이기)**: 유휴/과잉 리소스 탐지(CPU 40% / Memory 60% / 2주 지속 기준),
  Right-sizing 3대안(Downsize-1단/Downsize-2단/Terminate), Amortized 비용 기반
  RI/SP/Spot 혼합 약정 전략 **Conservative/Base/Optimistic 3시나리오** 산출
- **@operate (체계화)**: 단위경제 KPI 설계(가입자당·API 100만 건당·ML 학습 1회당 비용 +
  **LLM 추론 1,000건당 비용 · 토큰 1M당 비용 · GPU 시간당 비용**), 탐지→권고→승인→적용→검증 자동화 파이프라인,
  주간/월간/분기 비용 리뷰 루틴, 게이트 기준(태깅 95% · MAPE 10% · RI 활용률 80% · 이상 탐지 지연 24h ·
  유휴율 3% · **GPU 활용률 ≥ 60%**) 운영화

> 최종 산출은 실습 자산 — **웹 대시보드(HTML)** + 마크다운(권고문·약정 전략·리뷰 런북) + CSV(정규화). 별도 Office 변환은 수행하지 않음.

---

## 사용자 플로우

### STEP 1. @why-finops — WHY 정의 & 성숙도 진단
참고정보:
- [`references/am/finops.md`](references/am/finops.md) §4.1~§4.4 (WHY-HOW-WHAT · COVERS 6원칙 · 3단계 순환)
- [`references/am/finops.md`](references/am/finops.md) §4.14~§4.15 (Crawl/Walk/Run · 2025 Ownership×Capability 다차원 진단)
- [`references/am/finops.md`](references/am/finops.md) §4.16 (Cloud+ · Executive Strategy Alignment · FinOps for AI)
- [`references/finops/state-of-finops-2026-lab-guide.md`](references/finops/state-of-finops-2026-lab-guide.md) §1 (기술 범주별 관리율 YoY)·§2 (Top 스킬셋 수요)·§3 (Capability 성숙도 경로)
- [`resources/basic-info/company-profile.md`](resources/basic-info/company-profile.md) (HBT 회사 프로파일 — 조직·비용 규모·태그 규칙·현 성숙도)
- [`resources/rulebook/covers-principles.yaml`](resources/rulebook/covers-principles.yaml) (COVERS 6원칙 규칙 ID 체계)

- Step 1-1. 비즈니스 이슈 → FinOps 동인 매핑
  - 매출 성장 대비 클라우드 지출 증가율, 멀티클라우드 가시성 결여, 예측 불가 비용 등을
    3대 가치(투자가치·비용최적화·문화정착)로 매핑
  - State of FinOps 2026 "Value of Technology" 미션 변화 반영 (`state-of-finops-2026-lab-guide.md` §1)
  - 산출물: `out/step1/1-drivers.md`
- Step 1-2. 성숙도 자가진단 (Ownership × Capability)
  - HBT 프로파일(§9)의 Crawl 상태를 Ownership별(FinOps팀·개발팀·데이터팀·인프라팀·재무팀) ×
    Capability 20여 개로 세분화 진단, Walk 전환을 위한 3~6개월 집중 역량 선정
  - DORA식 "전사 평균" 함정 회피 — 부서별 최하위 Capability 1개씩 특정 (`finops.md` §4.15)
  - 산출물: `out/step1/2-maturity-diagnosis.md`
- Step 1-3. COVERS 원칙 정렬 & 12개월 스킬셋 로드맵
  - C/O/V/E/R/S 각 원칙당 현재 갭·목표 지표를 규칙 ID(`COVERS-*-##`)로 연결
  - Top 스킬셋 수요(AI Cost 58% · Tooling 43% · Automation 40% · Forecasting 39%) 기반
    조직 우선순위 결정 (`state-of-finops-2026-lab-guide.md` §2)
  - 산출물: `out/step1/3-covers-roadmap.md`
- Step 1-4. WHY 통합본 (경영진 보고용)
  - Step 1-1~1-3 통합 → "왜 지금 FinOps인가" 1-Pager + 12개월 OKR 초안
  - AI/SaaS/Licensing Cloud+ 확장 필요성 포함 (`finops.md` §4.16)
  - 산출물: `out/step1/why-statement.md`

---

### STEP 2. @inform — FOCUS 정규화 & 통합 가시성 (CSP + AI)
참고정보:
- [`references/am/finops.md`](references/am/finops.md) §4.5 (이상 비용 탐지 5단계 · CSP별 자동 수집)
- [`references/am/finops.md`](references/am/finops.md) §4.6 (태깅 거버넌스 · 할당 모델 · Showback/Chargeback)
- [`references/am/finops.md`](references/am/finops.md) §4.7 (Amortized 분할상환 방식)
- [`references/am/finops.md`](references/am/finops.md) §4.11 (FOCUS 표준 · FinOps 도구 생태계)
- [`references/am/finops.md`](references/am/finops.md) §4.16 (FinOps for AI — 98% 관리 · GPU/토큰 특화 메트릭)
- [`references/finops/state-of-finops-2026-lab-guide.md`](references/finops/state-of-finops-2026-lab-guide.md) §4 (AI 비용 3대 난제 · Granular 모니터링 Top 요청) · §5 (FOCUS 채택 85~90% · AI workloads FOCUS 확장 Top 요청)
- [`resources/sample-billing/aws-cur-sample.csv`](resources/sample-billing/aws-cur-sample.csv) (784 → **~830 rows** · **AWS Bedrock `InputTokens/OutputTokens` + GPU 인스턴스 `p4d.24xlarge` 행 추가**)
- [`resources/sample-billing/azure-export-sample.csv`](resources/sample-billing/azure-export-sample.csv) (930 → **~985 rows** · KRW 원본 · **Azure OpenAI `MeterCategory=Cognitive Services` + NC/ND-series GPU VM 행 추가**)
- [`resources/sample-billing/gcp-billing-sample.csv`](resources/sample-billing/gcp-billing-sample.csv) (424 → **~470 rows** · USD 원본 · **Vertex AI `service_description=Vertex AI` + A2/A3 GPU GCE 행 추가**)
- [`resources/sample-billing/saas-llm-sample.csv`](resources/sample-billing/saas-llm-sample.csv) **(신규)** (~200 rows · **OpenAI/Anthropic API Usage** — CSP 빌링에 안 잡히는 SaaS LLM만 별도 수집)
- [`resources/sample-billing/utilization-sample.csv`](resources/sample-billing/utilization-sample.csv) (CPU/Memory + **`gpu_util_pct` 컬럼 추가**)
- [`resources/sample-billing/README.md`](resources/sample-billing/README.md) (스키마 · 학습 이벤트 5종 + **AI 이벤트 4종** 위치 가이드)
- [`resources/schema/focus-v1.yaml`](resources/schema/focus-v1.yaml) (FOCUS v1.3 Mandatory 15종 + **AI 확장 컬럼 — TokenCountInput/Output·ModelName·GpuHours·GpuUtilization**)

- Step 2-1. 원본 빌링(CSP AI 포함) + SaaS LLM 로드 & 스키마 프로파일링
  - 3 CSP CSV(Bedrock·Azure OpenAI·Vertex AI 행 포함) + SaaS LLM CSV(OpenAI/Anthropic)의
    필수 컬럼·통화(USD/KRW)·리소스 ID·모델명 포맷 확인, 누락·중복 검증
  - 산출물: `out/step2/1-source-profile.md`
- Step 2-2. FOCUS 매핑 YAML 생성 (CSP + SaaS LLM → FOCUS)
  - `focus-normalizer`가 AWS CUR 2.0·Azure Cost Export·GCP Billing·**SaaS LLM(OpenAI/Anthropic)** →
    FOCUS v1.3 매핑 YAML **4종** + README 1종을 런타임 생성
    (lookup 테이블·transform 규칙·nullable 예외·AI 확장 컬럼 매핑 포함 —
    CSP의 토큰/GPU 행은 기존 매핑 내에서 `ServiceCategory=AI + ModelName` 룰로 분기)
  - 산출물: `resources/mapping/aws-cur-to-focus.yaml` · `azure-export-to-focus.yaml` ·
    `gcp-billing-to-focus.yaml` · **`saas-llm-to-focus.yaml`** · `resources/mapping/README.md`
- Step 2-3. FOCUS 정규화 병합 (CSP + SaaS LLM)
  - USD → KRW 환산(×1,500), Amortized BilledCost/EffectiveCost 계산,
    AI 확장 컬럼(TokenCountInput/Output·ModelName·GpuHours·GpuUtilization)을 ServiceCategory="AI"로 통합,
    GPU 활용률은 `utilization-sample.csv`의 `gpu_util_pct` 조인, 월 총합이 원본 BilledCost 합과 ±0.01 KRW 일치 검증
  - 산출물: `out/focus-normalized.csv` (FOCUS Mandatory 15종 + AI 확장 5종 · ~2,500 rows)
- Step 2-4. 태그 거버넌스 갭 분석 & 정책 생성 (CSP + AI)
  - `tag-governor`가 HBT 필수 4종 태그(Project/Environment/Owner/CostCenter) 누락률
    (AWS 8% · Azure 5% · GCP 10% · **AI 12%**) 산출, 회사 프로파일·COVERS 원칙 기반 `tag-policy.yaml` 런타임 생성
  - **AI 특화 규칙**: LLM API Key·모델명·요청 metadata 기반 Project/CostCenter 자동 할당 가이드
    (`state-of-finops-2026-lab-guide.md` §4.1 "API Key·tag·metadata 기반 chargeback")
  - 산출물: `out/step2/4-tag-coverage.md` · `resources/templates/tag-policy.yaml`
- Step 2-5. 이상 비용 탐지 & 웹 대시보드 (CSP + AI 통합)
  - `cost-analyst`가 5단계 체계(수집·분석·탐지·대응·예측) 적용 —
    3/15 AWS EC2 3배↑ · 3/20 Azure VM 급증 · 3/25 GCP Compute 급증 +
    **3/18 LLM 토큰 5배↑(모델 교체) · 3/22 GPU 활용률 15% 미달** 자동 식별
  - **인터랙티브 웹 대시보드(HTML + Chart.js CDN, 단일 파일)** — 빌드·서버 불필요, 브라우저로 바로 열림
    - **CSP 섹션** 차트 5종: ① 일별 비용 추이 라인 (CSP별 중첩) · ② 서비스별 Top 10 바 ·
      ③ 태깅 커버리지 도넛 (필수 4종 태그) · ④ CSP 분포 파이 · ⑤ 이상 비용 알림 표(정렬·필터 가능)
    - **AI 섹션** 차트 4종 (신규): ⑥ 모델별 비용 스택 바 (GPT-4o · Claude · Vertex · 내부 GPU) ·
      ⑦ 토큰 사용량 추이 라인 (Input/Output 이중 축) · ⑧ GPU 활용률 히트맵 (인스턴스 × 일자) ·
      ⑨ AI 단위경제 표 (토큰 1M당 · 추론 1,000건당 · GPU 시간당 비용)
    - 데이터 임베드: `focus-normalized.csv`(AI 확장 컬럼 포함)를 HTML `<script>`에 JSON으로 인라인(오프라인 열람 보장)
    - 인터랙션: 기간 슬라이더 · CostCenter/Project/**Model** 필터 · 차트 hover tooltip ·
      이상 행 클릭 → 상세 패널 · **CSP/AI 탭 전환**
    - 접근성: 단일 파일 < 1.2MB 목표 (AI 섹션 추가 반영), 다크모드 토글, 인쇄용 CSS
  - 산출물: `out/dashboard.html` (단일 파일 · Chart.js 4.x CDN · CSP 5종 + AI 4종 = 9 차트)

---

### STEP 3. @optimize — 줄이기 (Right-sizing · 약정 전략)
참고정보:
- [`references/am/finops.md`](references/am/finops.md) §4.8 (유휴 리소스 5종 · Right-sizing 5단계 · 판단 기준 지표)
- [`references/am/finops.md`](references/am/finops.md) §4.9 (HPA/VPA/Karpenter · Flapping 회피)
- [`references/am/finops.md`](references/am/finops.md) §4.10 (RI/SP/Spot 비교 · 의사결정 매트릭스 · Blended 전략)
- [`references/finops/state-of-finops-2026-lab-guide.md`](references/finops/state-of-finops-2026-lab-guide.md) §6 (Shift-Left) · §7 (Workload Optimization 25% Top 현재 우선순위)
- [`resources/sample-billing/utilization-sample.csv`](resources/sample-billing/utilization-sample.csv) (CPU/Memory 사용률 — CUR/Export에 없는 지표)
- [`resources/templates/ri-sp-decision-matrix.md`](resources/templates/ri-sp-decision-matrix.md) (Conservative/Base/Optimistic 3시나리오 의사결정)
- `out/focus-normalized.csv` (Step 2-3 결과물)

- Step 3-1. 유휴 리소스 탐지
  - 미연결 EBS·유휴 EC2·미사용 Disk·방치 LB·오래된 스냅샷 — CSP별 지표·시그니처로 식별
  - 산출물: `out/step3/1-idle-resources.md`
- Step 3-2. 과잉 프로비저닝 & Right-sizing 3대안 (CSP + AI)
  - `rightsize-advisor`가 FOCUS 데이터 + `utilization-sample.csv` 조인,
    CPU 40%·Memory 60% 2주 미달 리소스별 Downsize-1단/Downsize-2단/Terminate 대안 비교
    (성능 SLA 고려·피크타임 반영)
  - **AI Right-sizing 추가**: GPU 활용률 60% 미만 인스턴스(예: 3/22 유휴 GPU) Downsize·Terminate,
    과대 모델 사용 탐지 → **모델 다운그레이드 권고**(GPT-4o → GPT-4o-mini 등 Price/Performance 대안 3종)
  - 산출물: `out/rightsize-plan.md`
- Step 3-3. 스케일링 정책 리뷰 (참고)
  - HPA 임계값·minReplicas·cooldown 비용 영향 체크리스트, VPA+HPA Flapping 방지 가이드,
    Karpenter 빈 패킹 기대 절감률 — 실측 값 아닌 **체크리스트 산출물**
  - 산출물: `out/step3/3-scaling-policy-checklist.md`
- Step 3-4. 약정 할인 3시나리오 (RI/SP/Spot 혼합)
  - `commit-planner`가 상시 워크로드(RDS 3대·App Service 2대·Cloud SQL 2대)·변동·배치 분류,
    Conservative(RI 1y No-Upfront 중심) / Base(SP 1y Partial · 일부 RI 3y) /
    Optimistic(SP 3y All-Upfront + Spot 배치) 3안의 절감액·BEP·리스크 비교
  - 최소 3~6개월 사용 데이터 필요 원칙(`§4.10`) 준수 — 샘플 1개월 데이터의 한계 명시
  - 산출물: `out/commit-strategy.md`

---

### STEP 4. @operate — 체계화 (KPI · 자동화 · 거버넌스)
참고정보:
- [`references/am/finops.md`](references/am/finops.md) §4.11 (FinOps 자동화 5단계 · Shift-Left)
- [`references/am/finops.md`](references/am/finops.md) §4.12 (단위경제 KPI · 활성화·성과 메트릭)
- [`references/am/finops.md`](references/am/finops.md) §4.13 (Cost-Aware Engineering 문화 · 리뷰 주기)
- [`references/finops/state-of-finops-2026-lab-guide.md`](references/finops/state-of-finops-2026-lab-guide.md) §4 (AI FinOps — 토큰/GPU Granular 모니터링) · §8 (ITFM·ITSM·ITAM 인접 분야)
- [`resources/rulebook/covers-principles.yaml`](resources/rulebook/covers-principles.yaml) (모든 액션에 규칙 ID 역추적)
- [`resources/rulebook/gate-criteria.yaml`](resources/rulebook/gate-criteria.yaml) (5대 정량 게이트)
- [`resources/templates/monthly-review-agenda.md`](resources/templates/monthly-review-agenda.md) (60분 표준 아젠다)

- Step 4-1. 단위경제 KPI 대시보드 생성 (CSP + AI)
  - `finops-practitioner`가 HBT 사업 포트폴리오(MNO·MVNO·IoT·B2B) 기반 KPI 3종 + **AI KPI 3종** 확정 —
    **CSP**: 가입자당·API 100만 건당·ML 학습 1회당 비용
    · **AI**: 토큰 1M당 비용(Input/Output) · LLM 추론 1,000건당 비용 · GPU 시간당 비용
  - AI ROI 훅: 비용 대비 생산성·매출 기여도 Unit Economics 산식 (`state-of-finops-2026-lab-guide.md` §4.1·§4.3)
  - 산출물: `resources/templates/kpi-dashboard.md` · `out/step4/1-unit-economics.md`
- Step 4-2. 자동화 파이프라인 설계 (5단계)
  - 탐지(Detect) → 권고(Recommend) → 승인(Approve) → 적용(Apply) → 검증(Verify) 5단계에
    각 에이전트·도구·실패 시 액션 매핑, Shift-Left 훅(PR Gate · Infracost 권장) 포함
  - 산출물: `out/step4/2-automation-pipeline.md`
- Step 4-3. 게이트 기준 운영화 & 리뷰 런북
  - `gate-criteria.yaml` **6종**(태깅≥95% · MAPE≤10% · RI≥80% · 이상탐지≤24h · 유휴≤3% ·
    **GPU 활용률≥60%**)을 주/월/분기 리뷰 어젠다에 삽입, 미달 시 책임 에이전트·에스컬레이션 절차 명시
  - 산출물: `out/step4/3-review-runbook.md`
- Step 4-4. 성숙도 전환 플랜 (Crawl → Walk)
  - Step 1-2 진단 결과를 Phase 0(진단 확정)·Phase 1(Quick Win 90일)·Phase 2(Walk 달성 12개월)로 구성,
    Ownership별 KPI·GO/NO-GO 게이트 연결
  - 산출물: `out/step4/4-maturity-transition.md`

---

### 최종 산출
- 최종 Review: `reviewer`가 WHY-Inform-Optimize-Operate 정합성, FOCUS 필수 15종 커버리지,
  COVERS/게이트 규칙 ID 역참조 가능성, 3시나리오 절감액 일관성, Ownership별 전환 실행 가능성 검증
- **최종 산출 번들** (고정 경로 — reviewer 검증 기준):
  - `out/why-statement.md` (Step 1 통합) · `out/focus-normalized.csv` · `out/dashboard.html` ·
    `out/rightsize-plan.md` · `out/commit-strategy.md` · `out/review-runbook.md` (Step 4 통합)
  - 중간 산출(`out/step{1..4}/*`)은 단계별 디테일 아카이브로 병행 보존
- (선택) README 동기화: 플러그인 README에 실행 가이드 반영

---

## 에이전트 구성

> 추천 근거: 핵심기능 4개(Why/Inform/Optimize/Operate)와 사용자 플로우 STEP 1~4 + 최종 Review에서
> 도출되는 역할 클러스터를 분석하여 **8개 에이전트**로 구성 (개발계획서 §3.3 확정안).
> 동일 전문 영역 내에서 워크플로우가 독립적으로 분리되는 작업은 서브역할로 캡슐화.

- **strategy-director** (HIGH): WHY 정의 · 성숙도 진단 전문가 — 비즈니스 이슈를 FinOps 3대 가치로 매핑,
  Ownership×Capability 다차원 진단, COVERS 원칙 정렬 및 12개월 OKR·스킬셋 로드맵 수립 담당
  > 매칭 근거: STEP 1 전체(1-1~1-4)의 분석/설계/경영진 커뮤니케이션 역량 요구 → architect 계열 HIGH
  - **maturity-assessor**: Ownership별·Capability별 진단 템플릿·점수화 규칙 적용 (`finops.md` §4.14~15)
  - **driver-mapper**: 비즈니스 이슈 → 3대 가치·6원칙 매핑 (State of FinOps 2026 Top 스킬셋 반영)

- **focus-normalizer** (MEDIUM): FOCUS 변환 전문가 — AWS CUR 2.0(Bedrock·GPU 행 포함) ·
  Azure Cost Export(Azure OpenAI·GPU VM 포함) · GCP Billing(Vertex AI·GPU GCE 포함) ·
  **SaaS LLM(OpenAI/Anthropic Usage API)** → FOCUS v1.3 매핑 YAML 4종 생성·병합 수행,
  USD↔KRW 환산 및 Amortized 비용 산출,
  **AI 확장 컬럼(TokenCountInput/Output·ModelName·GpuHours·GpuUtilization)** 통합 담당
  > 매칭 근거: STEP 2-2·2-3의 스키마 매핑·데이터 변환 작업 → executor 계열 MEDIUM
  - **schema-profiler**: 원본 CSV 스키마 프로파일링·누락 컬럼 경고 자동화
  - **unit-converter**: 통화 환산·Amortized 분할상환 계산 (`finops.md` §4.7)
  - **ai-extension-mapper**: CSP CSV 내 AI 행(Bedrock `InputTokens`·Vertex AI SKU 등) 식별 +
    SaaS LLM Usage API 레코드를 FOCUS AI 확장 컬럼으로 매핑, GPU 활용률은 utilization CSV 조인
    (`state-of-finops-2026-lab-guide.md` §5 AI workloads FOCUS 확장 대응)

- **cost-analyst** (MEDIUM): 비용 분석·이상 탐지·웹 대시보드 작성 전문가 —
  FOCUS 정규화 결과(CSP + AI 확장) 기반 서비스·Project·CostCenter·**모델/토큰/GPU** 축 집계,
  이상 비용 5단계 체계(수집·분석·탐지·대응·예측) 실행,
  **`out/dashboard.html` 단일 파일 생성** (HTML + Chart.js 4.x CDN, 데이터 JSON 인라인, 기간 슬라이더·
  CostCenter/Project/Model 필터·CSP/AI 탭 전환·다크모드·인쇄용 CSS 포함, < 1.2MB 오프라인 열람 가능) 담당
  > 매칭 근거: STEP 2-5의 데이터 분석·시각화·정적 웹 산출물 작성 → executor 계열 MEDIUM
  - **anomaly-detector**: 평균+3σ·YoY·전월 대비 룰 기반 이상 비용 식별 (CSP 이벤트 3종 + **AI 이벤트 2종**)
  - **ai-cost-analyzer**: 토큰 사용량 추이·모델별 비용·GPU 활용률·AI 단위경제 산식 집계
  - **chart-renderer**: FOCUS 데이터 → Chart.js 차트 **9종**(CSP 5 + AI 4) 스키마 매핑 및 HTML 템플릿 주입

- **tag-governor** (LOW): 태깅 거버넌스 전문가 — 필수 4종 태그 커버리지 측정, 미태깅 리소스 탐지,
  회사 프로파일 맞춤 `tag-policy.yaml` 생성 및 위반 에스컬레이션 절차 설계 담당
  > 매칭 근거: STEP 2-4의 규칙 기반 단순 집계·정책 문서 작성 → writer 계열 LOW

- **rightsize-advisor** (MEDIUM): Right-sizing 권고 전문가 — CPU 40%·Memory 60% 2주 지속 기준
  유휴/과잉 리소스 식별, Downsize-1단/Downsize-2단/Terminate 3대안 절감액·성능 리스크 비교,
  **AI: GPU 활용률 60% 미만 Downsize·Terminate + 모델 다운그레이드 권고(GPT-4o → GPT-4o-mini 등)** 담당
  > 매칭 근거: STEP 3-1·3-2의 정량 분석·대안 설계 → executor 계열 MEDIUM
  - **utilization-joiner**: billing·utilization CSV 조인키 정합성 검증 (`vm-overprov-*` 통일 규약)
  - **model-selector**: 작업 유형별 Price/Performance 대안 모델 3종 비교(품질 리스크·대체 가능성 평가)

- **commit-planner** (HIGH): 약정 할인 설계 전문가 — 상시/변동/배치 워크로드 분류,
  RI/SP/Spot 혼합 전략을 Conservative/Base/Optimistic 3시나리오로 시뮬레이션,
  BEP·리스크·유연성 트레이드오프 비교 담당
  > 매칭 근거: STEP 3-4는 의사결정·정량 모델링·리스크 설계 → planner 계열 HIGH
  - **scenario-modeler**: 3시나리오 절감액·약정기간·지불방식(No/Partial/All Upfront) 경우의 수 계산
  - **workload-classifier**: 24/7 상시·변동·배치·예측불가 4범주 자동 분류 (`ri-sp-decision-matrix.md` 적용)

- **finops-practitioner** (MEDIUM): 운영 체계화 전문가 — 단위경제 KPI 설계(가입자당·API당·ML 학습당 +
  **토큰 1M당·추론 1,000건당·GPU 시간당**), 자동화 파이프라인 5단계 매핑,
  주/월/분기 리뷰 런북 및 성숙도 전환 Phase 설계 담당
  > 매칭 근거: STEP 4 전체의 운영 프로세스·KPI 설계 → 도메인 특화 MEDIUM
  - **kpi-designer**: HBT 사업 포트폴리오 맞춤 KPI 선정·계산식·트렌드 템플릿 (CSP 3종 + AI 3종)
  - **automation-architect**: 탐지→권고→승인→적용→검증 각 단계 도구·실패 액션 매핑

- **reviewer** (HIGH): 산출물 검증 전문가 — WHY-Inform-Optimize-Operate 4단계 정합성,
  FOCUS 필수 컬럼 15종 커버리지, COVERS/게이트 규칙 ID 역참조 가능성,
  3시나리오 수치 일관성, Ownership별 전환 실행 가능성을 독립 컨텍스트에서 검증 담당
  > 매칭 근거: 최종 Review 단계 — 자체 산출물에 대한 독립적 검증
  > (`omc:execution_protocols`의 reviewer 분리 원칙 준수)

---

## 공유자원

> 매칭 근거 요약: 본 플러그인은 (1) 멀티 CSP 빌링 샘플 기반 학습, (2) FOCUS 표준 정규화,
> (3) COVERS/게이트 룰북 기반 권고 추적성, (4) Office 입력 자료 선택적 변환이 필요하므로
> 아래 자원을 매칭함. 최종 산출은 마크다운(대시보드·권고문)이므로 PPT/이미지 생성 도구는 매칭하지 않음.

### 외부 공유자원 (DMAP 마켓플레이스)

| 자원 유형 | 자원명 | 자원 경로 |
|----------|--------|------------|
| 템플릿 | README-plugin-template | {DMAP_PLUGIN_DIR}/resources/templates/plugin/README-plugin-template.md |
| 샘플 | README | {DMAP_PLUGIN_DIR}/resources/samples/plugin/README.md |
| 도구 | convert-to-markdown | {DMAP_PLUGIN_DIR}/resources/tools/customs/general/convert-to-markdown.py |

### 플러그인 내장 참조 자료 (사전 작성 완료 11종 + 교재·리포트 2종)

**학습의 1차 교재·리포트 (참조 전용)**
- [`references/am/finops.md`](references/am/finops.md) — FinOps 교재 (§4.1~§4.16, 본 플러그인 학습의 기준)
- [`references/finops/state-of-finops-2026-lab-guide.md`](references/finops/state-of-finops-2026-lab-guide.md) — State of FinOps 2026 실습 가이드

**사전 작성 완료 자산 12종** (스킬 실행 시 입력으로 소비 · AI 하이브리드: CSP CSV 확장 + SaaS LLM 1종 신규)

| # | 자원 유형 | 자원명 | 자원 경로 |
|---|----------|--------|------------|
| 0 | 회사정보 | HBT 회사 프로파일 | [`resources/basic-info/company-profile.md`](resources/basic-info/company-profile.md) |
| 1 | 샘플 CSV (업데이트) | AWS CUR 2.0 샘플 (~830 rows · USD 원본) — **Bedrock 토큰·p4d GPU 행 추가** | [`resources/sample-billing/aws-cur-sample.csv`](resources/sample-billing/aws-cur-sample.csv) |
| 2 | 샘플 CSV (업데이트) | Azure Cost Export 샘플 (~985 rows · KRW 원본) — **Azure OpenAI·NC/ND GPU VM 행 추가** | [`resources/sample-billing/azure-export-sample.csv`](resources/sample-billing/azure-export-sample.csv) |
| 3 | 샘플 CSV (업데이트) | GCP Billing Export 샘플 (~470 rows · USD 원본) — **Vertex AI·A2/A3 GPU GCE 행 추가** | [`resources/sample-billing/gcp-billing-sample.csv`](resources/sample-billing/gcp-billing-sample.csv) |
| 3-1 | 샘플 CSV (업데이트) | 사용률 샘플 (CPU/Memory + **`gpu_util_pct` 컬럼 추가**) — `@optimize` 조인 참조 | [`resources/sample-billing/utilization-sample.csv`](resources/sample-billing/utilization-sample.csv) |
| **3-2** | **샘플 CSV (신규)** | **SaaS LLM 사용량 샘플 (~200 rows · USD 원본) — OpenAI/Anthropic Usage API (CSP 빌링에 없는 독립 지출)** | [`resources/sample-billing/saas-llm-sample.csv`](resources/sample-billing/saas-llm-sample.csv) |
| 4 | 가이드 (업데이트) | 3 CSP + SaaS LLM 스키마·학습 이벤트 위치 가이드 | [`resources/sample-billing/README.md`](resources/sample-billing/README.md) |
| 5 | 스키마 (업데이트) | FOCUS v1.3 통합 스키마 + **AI 확장 컬럼 5종** 추가 | [`resources/schema/focus-v1.yaml`](resources/schema/focus-v1.yaml) |
| 11 | 템플릿 | RI/SP/Spot 의사결정 매트릭스 | [`resources/templates/ri-sp-decision-matrix.md`](resources/templates/ri-sp-decision-matrix.md) |
| 12 | 템플릿 | 월간 FinOps 리뷰 60분 아젠다 | [`resources/templates/monthly-review-agenda.md`](resources/templates/monthly-review-agenda.md) |
| 14 | 룰북 | COVERS 6원칙 규칙 ID 체계 | [`resources/rulebook/covers-principles.yaml`](resources/rulebook/covers-principles.yaml) |
| 15 | 룰북 (업데이트) | 게이트 기준 5 → **6종**(GPU 활용률 ≥ 60% 추가) | [`resources/rulebook/gate-criteria.yaml`](resources/rulebook/gate-criteria.yaml) |

> **AI 샘플 하이브리드 설계**:
> - **CSP CSV 내 AI 행 (실재 현장 그대로)** — AWS CUR: `UsageType=InputTokens/OutputTokens`(Bedrock) · `instance_type=p4d.24xlarge`(GPU) / Azure Export: `MeterCategory=Cognitive Services`·`MeterSubCategory=Azure OpenAI` · `MeterName=NC6s v3`(GPU VM) / GCP: `service_description=Vertex AI` · `sku_description=A2/A3 GPU`
> - **#3-2 SaaS LLM 스키마**: `date, provider(openai/anthropic), model, project, cost_center,
>   tokens_input, tokens_output, request_count, cost_usd, api_key_hash, tags(JSON)`
> - **심는 학습 이벤트 4종**: ① 3/18 SaaS LLM 토큰 5배↑(모델 교체) · ② 3/22 AWS/GCP GPU 활용률 15%(utilization 조인) ·
>   ③ 과대 모델 사용(Classification에 GPT-4o) · ④ AI 태깅 누락 12%(CSP AI 행 + SaaS LLM 통합 산출)

### 에이전트 런타임 생성 산출물 (사전 작성 제외)

> 학습 가치상 **사용자가 에이전트 설계·분석 과정을 관찰** 하는 것이 핵심이므로 사전 작성하지 않고
> 스킬 실행 시 생성. 에이전트 프롬프트에는 **기대 스펙·형식·검증 기준** 만 기술.

| 경로 | 생성 주체 | 입력 | 스킬 |
|------|----------|------|------|
| `resources/mapping/aws-cur-to-focus.yaml` | focus-normalizer | #1 + #5 | `@inform` |
| `resources/mapping/azure-export-to-focus.yaml` | focus-normalizer | #2 + #5 | `@inform` |
| `resources/mapping/gcp-billing-to-focus.yaml` | focus-normalizer | #3 + #5 | `@inform` |
| `resources/mapping/saas-llm-to-focus.yaml` | focus-normalizer | #3-2 + #5 | `@inform` |
| `resources/mapping/README.md` | focus-normalizer | 4종 요약 | `@inform` |
| `resources/templates/tag-policy.yaml` | tag-governor | #0 + #14 | `@inform` |
| `resources/templates/kpi-dashboard.md` | finops-practitioner | #0 + 정규화 결과 | `@operate` |
| `out/focus-normalized.csv` | focus-normalizer | #1·#2·#3(AI 행 포함)·#3-2 + 매핑 YAML | `@inform` |
| `out/dashboard.html` | cost-analyst | 정규화 결과 (CSP + AI 통합) | `@inform` |
| `out/rightsize-plan.md` | rightsize-advisor | 정규화 결과 + #3-1(GPU 포함) | `@optimize` |
| `out/commit-strategy.md` | commit-planner | 정규화 결과 + #11 | `@optimize` |

### 적합성 이유

| 자원 | 적합성 |
|------|--------|
| `README-plugin-template` · `README` 샘플 | DMAP 표준 README 구조로 플러그인 배포 품질 일관성 확보 |
| `convert-to-markdown` | `references/` 아래 Office 문서(예: State of FinOps 원본 PDF) 확장 시 마크다운 변환 필요 — 선택적 활용 |
| `references/am/finops.md` | 본 플러그인 학습의 **1차 교재**. §4.4~§4.16 전 섹션이 스킬 4종·에이전트 8종에 1:1 매핑됨 |
| `references/finops/state-of-finops-2026-lab-guide.md` | 2026 최신 트렌드(Value of Technology · AI FinOps 98% · FOCUS 85% · Top 스킬셋)를 실습 우선순위에 직접 반영 |
| `resources/basic-info/company-profile.md` | WHY 정의·KPI 설계·태그 정책·성숙도 진단 등 **전 스킬의 기업 맥락 입력** — 가상 기업 HBT의 멀티클라우드 분포·조직·CostCenter·현 성숙도(Crawl) 포함 |
| `resources/sample-billing/*` | FOCUS 변환·이상 탐지·태깅 분석·Right-sizing 대상 데이터. 학습 이벤트 5종(Anomaly·태깅 누락·유휴·과잉·약정 기회) + **AI 이벤트 4종(토큰 스파이크·GPU 유휴·과대 모델·AI 태깅 누락)** 이 교재 §4.5~§4.10·§4.16과 동시 재현되도록 설계됨 |
| `resources/schema/focus-v1.yaml` | FOCUS v1.3 Mandatory 15종 + Recommended/Conditional. `focus-normalizer`의 목표 스키마 |
| `resources/templates/ri-sp-decision-matrix.md` | `commit-planner`의 3시나리오 의사결정 입력. 상시/변동/예측불가 × Compute/DB/Cache 분류 규칙 포함 |
| `resources/templates/monthly-review-agenda.md` | `finops-practitioner`의 월간 리뷰 런북 템플릿. Inform 15'/Optimize 20'/Operate 15'/Action 10' 표준화 |
| `resources/rulebook/covers-principles.yaml` | 6원칙 규칙 ID 체계로 **모든 권고에 역추적 가능성** 부여. reviewer 검증 기준 |
| `resources/rulebook/gate-criteria.yaml` | 태깅 95% · MAPE 10% · RI 80% · 이상탐지 24h · 유휴 3% · **GPU 활용률 60%** 정량 게이트. @operate·reviewer의 판정 기준 |

### 매칭 결과 없음 (직접 작성 또는 런타임 생성 필요)

- **실 CSP API 연동 어댑터**: 본 MVP는 정적 CSV 기반 학습이므로 제외. 2차 이터레이션에서 AWS Cost Explorer API·Azure Cost Management API·GCP Billing BigQuery 어댑터 필요 시 추가 검토
- **실 LLM 제공사 API 로그 어댑터**: OpenAI/Anthropic Usage API 실데이터 연동은 2차 대상. MVP는 `#3-2 saas-llm-sample.csv` 정적 샘플로 학습 (CSP 네이티브 AI 서비스인 Bedrock·Azure OpenAI·Vertex AI는 각 CSP CSV 내부 행으로 이미 포함)
- **Infracost/Shift-Left IaC Gate**: PR 단계 비용 추정은 2차 이터레이션 대상. STEP 4-2 자동화 파이프라인에 훅만 명시

---

## 비기능 요구사항

- **이식성**: DMAP 기반으로 Claude Code·Cursor·Cowork 어디서나 동작 (`gateway/runtime-mapping.yaml`)
- **보안/컴플라이언스**: 실제 CSP 청구 데이터를 플러그인 외부로 전송하지 않음. 학습용 가상 데이터만 참조.
  실데이터 확장 시 `resource_tags_user_*` 계열 PII 가능 필드 마스킹 권고를 README에 명시
- **재현성**: 동일 샘플 CSV 로드 시 동일 이상·유휴·약정 기회가 탐지되어야 함 (태깅 누락률 ±2%p 허용 — AWS 8.16% · Azure 6.45% · GCP 9.91% · **AI 약 12%** 실측 재현). AI 이벤트 4종(토큰 스파이크·GPU 유휴·과대 모델·태깅 누락)도 결정적으로 재현되어야 함
- **증거 기반**: 모든 정량 권고는 출처(교재 §번호·FOCUS 스펙·State of FinOps 2026 페이지) 명시.
  COVERS 규칙 ID(`COVERS-*-##`)·게이트 항목(`TAGGING_COVERAGE` 등) 역참조 가능
- **스펙 고정**: FOCUS `spec_version: "1.3"` 고정. 스펙 변경 시 `changelog`에 마이그레이션 노트 기록
- **경영진 소통**: Step 1-4 WHY 통합본은 경영진이 이해할 수 있는 용어 —
  "왜(WHY) → 얼마(TCO/KPI) → 어떻게(Inform/Optimize) → 언제(성숙도 Phase) → 위험(Risk)" 순서 고정
- **크기 제한**: Git·플러그인 배포 감안 — CSV 1종당 ≤ 1,000 rows(AI 샘플 ≤ 400 rows), 정규화 결과 ≤ 2,500 rows 권장
- **AI 비용 가시성**: 토큰·모델·GPU 단위 **Granular 모니터링** 제공 (`state-of-finops-2026-lab-guide.md` §4.2). AI 요청에 필수 태그(Project·Owner·CostCenter) 누락 시 경고

---

## 성공 기준

| 구분 | 성공 기준 |
|------|---------|
| 교재 커버리지 | [`references/am/finops.md`](references/am/finops.md) §4.4~§4.16 전 섹션이 스킬·에이전트·자산에 1:1 매핑 — reviewer 체크리스트 100% |
| FOCUS 완전성 | 3 CSP + AI 샘플 CSV 모두 FOCUS v1.3 Mandatory 15종 + **AI 확장 5종** 채워 출력, 월 총합이 원본 `BilledCost` 합과 ±0.01 KRW 일치 |
| 가시성(보이기) | `@inform` 실행 결과 `out/dashboard.html` 단일 파일 자동 생성 — Chart.js 차트 **9종(CSP 5 + AI 4)** + 이상 비용 **5건(CSP 3/15·3/20·3/25 + AI 3/18 토큰·3/22 GPU)** 식별, 브라우저에서 오프라인 열람 가능 |
| AI 비용 가시성 | 모델별 비용 스택·토큰 추이·GPU 활용률 히트맵·AI 단위경제 표가 대시보드 AI 섹션에 렌더링되고, 과대 모델 사용·GPU 저활용 이벤트가 `@optimize` 권고로 연결됨 |
| 태그 거버넌스 | 태그 누락률이 의도한 8%/5%/10%와 ±2%p 내 재현, `tag-policy.yaml` 런타임 생성, 미태깅 리소스 오너 식별 가능 |
| 최적화 권고 | `@optimize` 실행 결과 유휴 리소스 6종 이상·Right-sizing 3대안·RI/SP/Spot 3시나리오가 절감액·BEP·리스크와 함께 제시 |
| 운영 체계화 | 단위경제 KPI **6종(CSP 3 + AI 3)** + 자동화 5단계 + 게이트 **6종(GPU 활용률 포함)** 이 주/월/분기 리뷰 런북에 삽입되어 미달 시 에스컬레이션 절차 명시 |
| 룰북 추적성 | 모든 권고·KPI·게이트가 `COVERS-*-##`·`gate-criteria.yaml` 규칙 ID로 역참조 가능 |
| 성숙도 전환 | Step 1-2 진단 → Step 4-4 전환 플랜까지 Crawl → Walk 12개월 로드맵이 Ownership별 KPI·GO/NO-GO 게이트로 연결 |
| 산출 형식 | HTML(대시보드 — Chart.js 단일 파일) + 마크다운(권고문·리뷰 런북) + CSV(focus-normalized) + YAML(매핑·tag-policy) 일관성 |
| DMAP 표준 준수 | `dmap:develop-plugin` 린트/검증 통과 |
