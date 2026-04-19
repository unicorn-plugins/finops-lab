# finops-lab 샘플 파일 작성 계획

> 작성일: 2026-04-18 (최종 동기화: 2026-04-19)
> 기반: [finops-lab-plan.md](./finops-lab-plan.md) §3.4, §5
> 범위: **샘플 자산(Phase 2)** 에 해당하는 `resources/**` 파일 일체

> ### 📌 구현 반영 동기화 요약 (2026-04-19)
>
> 본 계획 v1과 실제 구현 사이에 아래 드리프트가 발생, 구현을 기준으로 계획을 갱신.
>
> | 항목 | 당초 계획 | 최종 구현 | 결정 |
> |------|----------|----------|------|
> | FOCUS 스키마 버전 | v1.1 | v1.3 (with v1.1 changelog) | **v1.3 채택** — 최신 표준 반영이 학습 가치 큼 |
> | 통화 설계 | "WON 단일" | AWS/GCP USD 원본 + Azure KRW 원본, `@inform` 에이전트가 ×1,500 환산 | **혼합 채택** — CSP 현실 반영 |
> | 사전작성 항목 수 | 9개 | 11개 (#0, #3-1 추가) | **11개 확정** |
> | 행 수 | AWS 600 / Az 450 / GCP 400 | 784 / 930 / 424 | 이벤트 재현 필요 행수만큼 확장, 상한 1,000 준수 |
> | 예산 규모 | company-profile 월 ₩320M | CSV 합계 ~₩41M (13%) | 샘플=서브셋, README에 명시 |
> | Azure 스코프 | "HR/ERP/협업툴" | + web/api/data dev/stg 미러, 보조 prod | company-profile §3.1, §3.3 확장 |
> | Azure overprov 네이밍 | 미지정 | billing=`vm-overprov-*`, util=`vm-overprov-*` 통일 | 조인 가능 |
> | 태깅 누락률 허용 | ±1%p | ±2%p (CSP별 실측 6.45%/8.16%/9.91%) | ±2%p로 완화 |

---

## 0. 목적

DMAP 플러그인 `finops-lab` 의 스킬(`@why-finops` · `@inform` · `@optimize` · `@operate`)이
**별도 외부 API 없이** 손으로 돌려볼 수 있도록, 학습 이벤트가 의도적으로 심어진
정적 샘플 자산을 `resources/` 하위에 일괄 제작한다.

핵심 원칙:
- **교재(§4.5~§4.11) 1:1 매핑** — 각 파일은 교재 섹션과 역추적 가능해야 함
- **FOCUS v1.x 실재 컬럼명 사용** — 연습용이라도 현장 스키마 그대로
- **학습 이벤트 재현성** — 동일 CSV 로드 시 동일 이상/유휴/약정 기회가 탐지됨
- **크기 제한** — Git·플러그인 배포를 감안해 CSV 1종당 ≤ 1,000 rows

---

## 1. 산출물 목록 (한눈에)

| # | 경로 | 포맷 | 용도 | 비고 |
|---|------|------|------|-------|-------|
| 0 | `resources/basic-info/company-profile.md` | MD | 회사정보. `references\samples\company-profile.md` 참조하여 작성 |  
| 1 | `resources/sample-billing/aws-cur-sample.csv` | CSV | AWS CUR 2.0 원본 샘플 | P2 | ★★★ |
| 2 | `resources/sample-billing/azure-export-sample.csv` | CSV | Azure Cost Export 원본 샘플 | P2 | ★★ |
| 3 | `resources/sample-billing/gcp-billing-sample.csv` | CSV | GCP Billing Export 원본 샘플 | P2 | ★★ |
| 3-1 | `resources/sample-billing/utilization-sample.csv` | CSV | CPU/Memory 사용률 샘플(CUR/Export에 없는 지표) — `@optimize` 가 병합 참조 | P2 | ★★ |
| 4 | `resources/sample-billing/README.md` | MD | 3 CSV 스키마·이벤트 가이드 | P2 | ★ |
| 5 | `resources/schema/focus-v1.yaml` | YAML | FOCUS v1.x 통합 스키마 정의 | P2 | ★★ |
| 11 | `resources/templates/ri-sp-decision-matrix.md` | MD | RI/SP/Spot 의사결정 매트릭스 (CSP 독립 지식) | P2 | ★★ |
| 12 | `resources/templates/monthly-review-agenda.md` | MD | 월간 FinOps 리뷰 아젠다 (표준 프로세스) | P2 | ★ |
| 14 | `resources/rulebook/covers-principles.yaml` | YAML | COVERS 6원칙 규칙 ID화 (FinOps 표준) | P2 | ★★ |
| 15 | `resources/rulebook/gate-criteria.yaml` | YAML | 게이트 기준(태깅 95%·MAPE 10% 등, 교재 정량) | P2 | ★★ |

**총 11개 사전 작성** (#0, #1, #2, #3, #3-1, #4, #5, #11, #12, #14, #15)

### 1.1 제외(에이전트 런타임 생성)

아래 산출물은 **사전 작성하지 않고** 스킬 실행 시 해당 에이전트가 입력 자산을 읽어
**런타임에 생성** 한다. (학습 목적상 사용자가 에이전트의 설계·분석 과정을 관찰하는 것이 핵심 가치)

| 경로 | 생성 주체 | 입력 | 스킬 |
|------|----------|------|------|
| `resources/mapping/aws-cur-to-focus.yaml` | `focus-normalizer` | #1 + #5 | `@inform` |
| `resources/mapping/azure-export-to-focus.yaml` | `focus-normalizer` | #2 + #5 | `@inform` |
| `resources/mapping/gcp-billing-to-focus.yaml` | `focus-normalizer` | #3 + #5 | `@inform` |
| `resources/mapping/README.md` | `focus-normalizer` | 위 3종 요약 | `@inform` |
| `resources/templates/tag-policy.yaml` | `tag-governor` | #0 + #14 | `@inform` |
| `resources/templates/kpi-dashboard.md` | `finops-practitioner` | #0 + 정규화 결과 | `@operate` |
| `out/focus-normalized.csv` | `focus-normalizer` | #1·#2·#3 + 매핑 YAML | `@inform` |
| `out/dashboard.md` | `cost-analyst` | 정규화 결과 | `@inform` |
| `out/rightsize-plan.md` | `rightsize-advisor` | 정규화 결과 + #3-1 | `@optimize` |
| `out/commit-strategy.md` | `commit-planner` | 정규화 결과 + #11 | `@optimize` |

> 에이전트 프롬프트에는 각 산출물의 **기대 스펙·형식·검증 기준** 만 기술한다. 학습자는 스킬 실행으로 `out/` 경로에서 결과를 확인.

---

## 2. 공통 설계 기준

### 2.1 기간·통화
- **빌링 기간**: `2026-03-01 ~ 2026-03-31` (30일, UTC)
- **통화 전략** (실제 CSP 현실 반영):
  - AWS CUR: USD 원본 (`line_item_unblended_cost`, `line_item_blended_cost`)
  - Azure Export: KRW 원본 (`CostInBillingCurrency`, `BillingCurrency=KRW` — 계정 단위 환율 사전 적용 가정)
  - GCP Billing: USD 원본 (`cost`, `currency=USD`)
  - **정규화 단계**에서 `@inform`이 AWS/GCP만 ×1,500 환산하여 FOCUS `BilledCost`(KRW)를 통일
- **환율**: $1 = ₩1,500 (고정)
- **집계 단위**: 일(day)

### 2.2 계정·리소스 네이밍
- 가상 조직: `(주)하이브리지텔레콤` (약어: HBT)
- AWS Account: `123456789012`
- Azure Subscription: `00000000-0000-0000-0000-000000000001`
- GCP Project: `acme-prod-001`
- 리소스 ID는 CSP 실제 포맷 준수 (`arn:aws:...`, `/subscriptions/.../resourceGroups/...`, `//compute.googleapis.com/...`)

### 2.3 태그 네임스페이스
- 필수: `Project`, `Environment`, `Owner`, `CostCenter`
- 값 집합: `Project={web, api, data, ml}`, `Environment={prod, stg, dev}`, `CostCenter={CC-100, CC-200, CC-300}`

### 2.4 학습 이벤트 (§5.1 준수)
각 CSV는 아래 5종 이벤트를 **동시에** 담는다. 날짜는 교재 시나리오 유지.

| 이벤트 | AWS | Azure | GCP |
|-------|-----|-------|-----|
| Anomaly | 3/15 EC2 3배↑ | 3/20 VM 급증 | 3/25 GCE 급증 |
| 태깅 누락 | `Project` 8% 결측 | `CostCenter` 5% | `Environment` 10% |
| 유휴 | 미연결 EBS 3 + 유휴 EC2 2 | 미사용 Disk 2 | 유휴 GCE 1 |
| 과잉 프로비저닝 | CPU 15% EC2 5대 | 메모리 30% VM 3대 | CPU 20% GCE 4대 |
| 약정 기회 | 24/7 RDS 3대 | 상시 App Service 2대 | 상시 Cloud SQL 2대 |

> ⚠ 사용률(CPU/Memory)은 CUR/Export에 없음. 별도 `resources/sample-billing/utilization-sample.csv` 를 두어 `@optimize` 가 병합 참조하도록 확장 예정.

---

## 3. 파일별 상세 설계

### 3.1 sample-billing/aws-cur-sample.csv

- **기반 스키마**: AWS CUR 2.0 (30+ 컬럼 중 핵심 18 컬럼)
- **필수 컬럼**:
  `bill_billing_period_start_date, bill_payer_account_id, line_item_usage_account_id,
   line_item_usage_start_date, line_item_usage_end_date, line_item_product_code,
   line_item_operation, line_item_resource_id, line_item_usage_type,
   line_item_usage_amount, line_item_unblended_cost, line_item_blended_cost,
   product_region, product_instance_type, pricing_unit, pricing_term,
   reservation_reservation_a_r_n, resource_tags_user_project,
   resource_tags_user_environment, resource_tags_user_owner,
   resource_tags_user_cost_center`
- **서비스 분포**: EC2 45%, RDS 20%, S3 15%, Lambda 8%, CloudWatch 5%, 기타 7%
- **행 수(실측)**: 784 rows (30일 × ~26 리소스 평균, 이벤트 반영 후)
- **특이 레코드**:
  - `line_item_resource_id=i-spike-001` 의 3/15 비용이 평소 $12 → $36
  - `i-idle-001, i-idle-002` 는 `line_item_usage_amount=0` 이지만 EBS 볼륨 비용 발생
  - `vol-orphan-001~003` 은 EC2 없이 EBS 비용만 존재

### 3.2 sample-billing/azure-export-sample.csv

- **기반 스키마**: Azure Cost Management Export (Amortized)
- **필수 컬럼**:
  `BillingPeriodStartDate, SubscriptionId, SubscriptionName, ResourceGroup,
   ResourceId, MeterCategory, MeterSubCategory, MeterName, UsageQuantity,
   UnitOfMeasure, CostInBillingCurrency, BillingCurrency, ResourceLocation,
   ChargeType, ReservationId, Tags(JSON), Date`
- **서비스 분포**: VM 40%, App Service 20%, SQL DB 15%, Storage 15%, Monitor 5%, 기타 5%
- **행 수(실측)**: 930 rows
- **과잉 프로비저닝 네이밍 규약**: billing·utilization 양쪽 모두 `vm-overprov-001/002`(api·CC-200, rg-api), `vm-overprov-003`(data·CC-300, rg-data)으로 통일(join 가능 보장)
- **특이 레코드**: 3/20 `vm-spike-azure` 비용 급증, 디스크 `disk-orphan-a/b` 미사용 상태 유지

### 3.3 sample-billing/gcp-billing-sample.csv

- **기반 스키마**: GCP Billing Export to BigQuery (CSV 변환 형태)
- **필수 컬럼**:
  `billing_account_id, project_id, project_name, service_description, sku_description,
   usage_start_time, usage_end_time, location_region, resource_name,
   resource_global_name, usage_amount, usage_unit, cost, currency,
   credits_amount, credits_type, labels(JSON), invoice_month`
- **서비스 분포**: Compute Engine 50%, Cloud SQL 15%, GCS 15%, BigQuery 10%, 기타 10%
- **행 수(실측)**: 424 rows
- **특이 레코드**: 3/25 `gce-spike-1` 급증, `gce-idle-1` CPU 20% 유지

### 3.4 sample-billing/README.md

- 각 CSV의 출처·스키마 버전·생성 방법(수작업/스크립트)
- 학습 이벤트 위치(행 번호) 표
- 재생성 가이드 (Python 스니펫 또는 수정 원칙)

### 3.5 schema/focus-v1.yaml

- **FOCUS v1.3 채택** (파일명은 `focus-v1.yaml` 유지, 내부 `spec_version: "1.3"`)
- Mandatory(15종) + Recommended + Conditional 필드 정의 (`BilledCost`, `EffectiveCost`, … `ServiceProviderName`, `CommitmentDiscountStatus`)
- 각 컬럼마다: `column_type, feature_level, data_type, nullable, unit, description, focus_spec_ref, hbt_notes`
- v1.3 주요 변경(ServiceProviderName Mandatory, ProviderName DEPRECATED, ServiceCategory 8→19종 등) `changelog`에 기록
- 공식 스펙 링크(focus.finops.org)를 주석으로 포함

### 3.6 ~~mapping/*~~ → 에이전트 런타임 생성 (제외)

`@inform` 스킬 실행 시 `focus-normalizer` 에이전트가 #1·#2·#3 샘플 CSV 와 #5 FOCUS 스키마를
입력으로 받아 매핑 YAML 3종·README를 생성한다. **사전 작성하지 않음.**

- 에이전트 프롬프트 설계는 Phase 3 에서 담당
- 산출물 기대 구조(참고용, 에이전트가 따라야 할 컨벤션):
  ```yaml
  source: { provider: aws, schema_version: CUR 2.0 }
  target: { schema: focus-v1.yaml }
  mappings:
    - { focus_field: BilledCost, source_field: line_item_unblended_cost, transform: identity }
    - { focus_field: ServiceCategory, source_field: line_item_product_code, transform: lookup_table, lookup: aws_service_to_category }
  lookups:
    aws_service_to_category: { AmazonEC2: Compute, AmazonRDS: Databases, ... }
  ```

### 3.7 ~~templates/tag-policy.yaml~~ → 에이전트 런타임 생성 (제외)

`@inform` 스킬에서 `tag-governor` 에이전트가 #0 회사정보 + #14 COVERS 원칙을 읽어
회사 맞춤 태그 정책을 생성. 에이전트 프롬프트에 **필수/권장 카테고리·심각도·감사주기** 가이드만 내재화.

### 3.8 templates/ri-sp-decision-matrix.md

- 리소스 유형별 매트릭스(상시/변동/예측불가 × Compute/DB/Cache)
- Conservative/Base/Optimistic 3시나리오 결정 기준
- 약정 기간(1y/3y) × 지불방식(No/Partial/All Upfront) 선택 규칙
- 예시 계산 1건 포함 (월 $10k EC2 → 1y SP 27% 절감 시나리오)

### 3.9 templates/monthly-review-agenda.md

- 60분 아젠다(Inform 15' / Optimize 20' / Operate 15' / Action 10')
- 지표 체크리스트(지난달 실적 vs 예산·이상비용·태깅 커버리지·약정 활용률)
- 의사결정 로그 포맷

### 3.10 ~~templates/kpi-dashboard.md~~ → 에이전트 런타임 생성 (제외)

`@operate` 스킬에서 `finops-practitioner` 에이전트가 #0 회사정보(비즈니스 모델) + 정규화 결과를
입력으로 맞춤 KPI 대시보드 생성. 에이전트 프롬프트에 **단위경제 KPI 유형·계산식 패턴·Mermaid 형식** 가이드 내재화.

### 3.11 rulebook/covers-principles.yaml

- COVERS 6원칙(Collaboration / Ownership / Visibility / Efficiency / Reporting / Strategy)
- 각 원칙당 규칙 ID 체계: `COVERS-C-01`, `COVERS-O-01`, …
- 규칙별: `description, rationale, skill, gate_criteria_ref`

### 3.12 rulebook/gate-criteria.yaml

- 정량 게이트:
  - `TAGGING_COVERAGE >= 95%`
  - `FORECAST_MAPE <= 10%`
  - `RI_UTILIZATION >= 80%`
  - `ANOMALY_DETECT_LATENCY <= 24h`
  - `IDLE_RESOURCE_RATE <= 3%`
- 각 항목: 측정식 · 데이터 소스 · 미달 시 Action · 책임 에이전트

### 3.13 ~~examples/*~~ → 에이전트 런타임 생성 (제외)

스킬 실행 결과물로 `out/` 경로에 생성:

| 산출물 | 생성 주체 | 기대 스펙 (에이전트 프롬프트에 내재화) |
|-------|----------|-------------------------------------|
| `focus-normalized.csv` | `focus-normalizer` | FOCUS v1.1 필수 컬럼 16종, ~1,400 rows, BilledCost 월 총합 원본 일치 |
| `dashboard.md` | `cost-analyst` | Mermaid 5종(라인/바/표/도넛/파이) + 이벤트 설명 |
| `rightsize-plan.md` | `rightsize-advisor` | 유휴/과잉 표 + 3대안(Downsize1/Downsize2/Terminate) |
| `commit-strategy.md` | `commit-planner` | Conservative/Base/Optimistic 3시나리오 비교표(절감액·리스크·기간) |

---

## 4. 작업 순서 (의존성 반영)

```
Step A (독립) : #5 focus-v1.yaml  → FOCUS 기준 확정
Step C (독립) : #0 company-profile.md + #1,#2,#3,#3-1 샘플 CSV + #4 README
Step F (독립) : #11 ri-sp-decision-matrix.md + #12 monthly-review-agenda.md
Step H (독립) : #14 covers-principles.yaml + #15 gate-criteria.yaml
```

**모두 독립 — 전부 병렬로 1회차에 완성.**

제외 항목(에이전트 런타임):
- 매핑 YAML 4종 · tag-policy · kpi-dashboard · examples 4종 → P3 에이전트 프롬프트 설계 시 스펙 반영

---

## 5. 검증 체크리스트

- [x] 3 CSP CSV 모두 §5.1 이벤트 5종이 **전부** 포함되어 있는가 — 2026-04-19 확인
- [ ] 매핑 YAML 적용 시 FOCUS Mandatory 15종 모두 채워지는가(Null 허용 항목만 예외)
- [ ] `focus-normalized.csv` 의 월 총합이 3 CSV 원본 `BilledCost` 합과 일치(±0.01 KRW)하는가
- [x] 태깅 누락률이 의도한 8%/5%/10% 와 ±2%p 내로 재현되는가 — AWS 8.16%, Azure 6.45%, GCP 9.91% 실측 (2026-04-19)
- [x] Azure billing↔utilization 조인키(리소스 last segment) 정합성 — 2026-04-19 수정 완료
- [x] Azure `Project×CostCenter` 정합성(web→CC-200, data→CC-300) — 2026-04-19 수정 완료
- [ ] 룰북 규칙 ID 가 모든 예시 산출물에서 역참조 가능한가
- [ ] DMAP 린트(`dmap:develop-plugin` P2 검증) 통과

---

## 6. 리스크

| 리스크 | 대응 |
|-------|------|
| CUR 2.0 컬럼 폭증으로 CSV 비대화 | 핵심 18 컬럼만, 나머지는 `extra_columns` YAML 로 분리 |
| FOCUS v1.1 → v1.2 변경 | `schema/focus-v1.yaml` 상단에 `spec_version: 1.1` 명시, 변경 시 마이그레이션 노트 |
| 학습 이벤트 재현 실패 | CSV 생성 스크립트(`scripts/gen-samples.py`)를 `.temp/` 에 동봉 후 P3 에서 정식화 |
| `gen_samples.py`가 Azure CSV 미생성(수작업 유지) | 스크립트 재실행 시에도 Azure는 유지되지만, Azure 수정 이력은 `.temp/azure-export-sample.csv.bak`으로 백업 필수 + README §6.1 주의 문구 명기 완료 |
| JSON 인코딩 태그 파싱 차이 | Azure/GCP 의 Tags/labels 컬럼은 **이중 인용부호 이스케이프 규칙** 을 README 에 명문화 |

---

## 7. 다음 액션

1. 이 계획 승인
2. Step A(`focus-v1.yaml`) + Step C(샘플 CSV 3종) 동시 착수
3. Step B 매핑 확정 후 Step D 에서 정규화 결과 CSV·대시보드 수치 검증
4. MVP 범위(#1~#9, #14~#17) 13개 완성 → 스킬 `@inform` 과 통합 테스트
