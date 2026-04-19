# sample-billing 디렉토리 — 스키마·이벤트 가이드

> 생성일: 2026-04-18  
> 용도: finops-lab 플러그인 스킬(`@inform` · `@optimize` · `@operate`) 실습용 정적 샘플 자산  
> 참조: `.temp/sample-files-plan.md §2, §3`

---

## 1. 파일 목록

| 파일 | 포맷 | 행 수 | 빌링 기간 | 통화 |
|------|------|-------|----------|------|
| `aws-cur-sample.csv` | CUR 2.0 | 784 | 2026-03-01 ~ 2026-03-31 | USD |
| `azure-export-sample.csv` | Cost Management Export (Amortized) | 930 | 2026-03-01 ~ 2026-03-31 | KRW |
| `gcp-billing-sample.csv` | Billing Export (BigQuery CSV 변환) | 424 | 2026-03-01 ~ 2026-03-31 | USD |
| `utilization-sample.csv` | 사용률 (CPU/Memory/Network) | 930 | 2026-03-01 ~ 2026-03-31 | - |

> AWS·GCP는 USD 원본, `@inform` 에이전트가 ×1,500 환산하여 focus-normalized.csv(KRW)를 생성합니다.

> **⚠ 샘플 스케일 주의**: 본 CSV는 학습용 서브셋으로, 3 CSP KRW 환산 월 총합은 약 ₩41M 규모입니다(AWS ₩7.8M · Azure ₩29.8M · GCP ₩3.9M). company-profile.md §4의 월 예산 ₩320M은 회사 전체 가상 시나리오이며, 본 CSV는 그 중 약 13% 범위의 대표 워크로드만 추출한 학습용 표본입니다. 예산 대비 실적 계산 실습 시 이 사실을 전제로 하거나, company-profile의 비율(AWS 55%·Azure 25%·GCP 20%)만 그대로 사용하세요.

---

## 2. 공통 설계 기준

### 2.1 가상 기업

| 항목 | 값 |
|------|-----|
| 기업명 | (주)하이브리지텔레콤 (HBT) |
| AWS Account | `123456789012` |
| Azure Subscription | `00000000-0000-0000-0000-000000000001` |
| GCP Project | `acme-prod-001` (Billing Account: `01AB12-CD34EF-567890`) |
| 환율 | $1 = ₩1,500 (고정) |
| 월 예산 | AWS ₩176,000,000 / Azure ₩80,000,000 / GCP ₩64,000,000 |

### 2.2 필수 태그 체계

| 태그 키 | 허용 값 | 비고 |
|---------|---------|------|
| `Project` | `web`, `api`, `data`, `ml` | 귀속 프로젝트 |
| `Environment` | `prod`, `stg`, `dev` | 운영 환경 구분 |
| `Owner` | 담당자 이메일 | 리소스 오너 |
| `CostCenter` | `CC-100`, `CC-200`, `CC-300` | 비용 센터 |

> Azure는 Tags 컬럼에 JSON 형태로 포함 (`{"Project": "web", ...}`)  
> GCP는 labels 컬럼에 JSON 형태로 포함

---

## 3. 학습 이벤트 위치

### 3.1 AWS CUR (aws-cur-sample.csv)

| 이벤트 유형 | 식별 조건 | 해당 리소스 | 비고 |
|------------|---------|-----------|------|
| **이상 비용 (Anomaly)** | `line_item_resource_id=i-spike-001`, `line_item_usage_start_date` 시작일 = 2026-03-15 | `i-spike-001` | 평소 $12/day → 3/15 $36/day (3배) |
| **태깅 누락** | `resource_tags_user_project` = `""` | `i-legacy-001`, `vol-legacy-001`, `hbt-logs` S3 | 전체의 약 8.2% |
| **유휴 (Idle)** | `line_item_usage_amount=0` + 인접한 EBS 행 존재 | `i-idle-001`, `i-idle-002` + `vol-idle-001/002` | stopped 상태 EC2 + 부착 EBS |
| **고아 EBS** | `vol-orphan-*` 행이 존재하되 대응하는 EC2 행 없음 | `vol-orphan-001`, `vol-orphan-002`, `vol-orphan-003` | 500GB gp3 각 $1.33/day |
| **과잉 프로비저닝** | `i-overprov-*` (utilization-sample.csv에서 avg_cpu < 20%) | `i-overprov-001` ~ `i-overprov-005` | m5.4xlarge, CPU 평균 15% |
| **약정 기회 (RI 후보)** | `pricing_term=OnDemand` + `line_item_product_code=AmazonRDS` + 30일 연속 행 존재 | `db-web-001`, `db-api-001`, `db-data-001` | 24/7 상시, RI 미적용 |

### 3.2 Azure Export (azure-export-sample.csv)

| 이벤트 유형 | 식별 조건 | 해당 리소스 | 비고 |
|------------|---------|-----------|------|
| **이상 비용 (Anomaly)** | `ResourceId` 포함 `vm-spike-azure`, `Date` = 2026-03-20 | `vm-spike-azure` | 3/20 비용 급증 |
| **태깅 누락** | `Tags` JSON에 `"CostCenter"` 키 없거나 값 빈값 | `vm-dev-001`, `appservice-dev-001`, `sqldb-dev` 등 dev 환경 리소스 | 전체의 약 6.4% (목표 5% ±2%p 허용) |
| **고아 디스크** | `MeterCategory=Disks`, `ResourceId` 포함 `orphan` | `disk-orphan-a`, `disk-orphan-b` | 미연결 상태 유지 |
| **과잉 프로비저닝** | `vm-overprov-*` (utilization-sample.csv에서 avg_memory < 35%) | `vm-overprov-001/002` (api/CC-200, rg-api), `vm-overprov-003` (data/CC-300, rg-data) | Standard_D8s_v3, 메모리 30% |
| **약정 기회** | `ChargeType=Usage`, `MeterCategory=App Service`, 30일 연속 | App Service 2대 | CUD/RI 미적용 |

### 3.3 GCP Billing (gcp-billing-sample.csv)

| 이벤트 유형 | 식별 조건 | 해당 리소스 | 비고 |
|------------|---------|-----------|------|
| **이상 비용 (Anomaly)** | `resource_name=gce-spike-1`, `usage_start_time` 시작일 = 2026-03-25 | `gce-spike-1` | 3/25 비용 급증 ($8 → $24) |
| **태깅 누락** | `labels` JSON에 `"Environment"` 값 빈값 | `gce-legacy-001`, Cloud SQL 일부 행 | 전체의 약 9.7% |
| **유휴** | `resource_name=gce-idle-1` (utilization-sample.csv에서 avg_cpu ~20%) | `gce-idle-1` | CPU 20% 유지, 과잉 프로비저닝 |
| **과잉 프로비저닝** | `gce-overprov-*` (utilization-sample.csv에서 avg_cpu < 25%) | `gce-overprov-002` ~ `gce-overprov-005` | n2-standard-8, CPU 20% |
| **약정 기회** | `service_description=Cloud SQL`, `credits_type` 없음, 30일 연속 | `cloudsql-web-001`, `cloudsql-data-001` | 24/7, CUD 미적용 |

### 3.4 Utilization (utilization-sample.csv)

| 컬럼 | 설명 |
|------|------|
| `provider` | `AWS` / `Azure` / `GCP` |
| `resource_id` | 각 CSP의 리소스 ID (billing CSV의 resource_id와 조인 가능) |
| `avg_cpu_percent` | 일 평균 CPU 사용률 (%) |
| `avg_memory_percent` | 일 평균 메모리 사용률 (%) |
| `status` | `running` / `stopped` |

> **조인 키**:
> - AWS: `utilization.resource_id ↔ aws-cur.line_item_resource_id` (둘 다 `i-web-001` 형식 단일 식별자)
> - Azure: `utilization.resource_id`(전체 ARM 경로) ↔ `azure-export.ResourceId`(전체 ARM 경로). 리소스명만 매칭하려면 양쪽 모두 `rsplit('/',1)[-1]`로 마지막 세그먼트 추출 후 조인.
> - GCP: `utilization.resource_id ↔ gcp-billing.resource_name` (둘 다 `gce-web-001` 형식)

---

## 4. 스키마 버전

### 4.1 AWS CUR 2.0 컬럼 (이 파일 사용 컬럼)

| 컬럼 | 타입 | FOCUS 매핑 대상 |
|------|------|----------------|
| `bill_billing_period_start_date` | DATE | `BillingPeriodStart` |
| `bill_payer_account_id` | STRING | `BillingAccountId` |
| `line_item_usage_account_id` | STRING | `SubAccountId` |
| `line_item_usage_start_date` | DATETIME | `ChargePeriodStart` |
| `line_item_usage_end_date` | DATETIME | `ChargePeriodEnd` |
| `line_item_product_code` | STRING | `ServiceName` (lookup 필요) |
| `line_item_operation` | STRING | `SkuName` |
| `line_item_resource_id` | STRING | `ResourceId` |
| `line_item_usage_type` | STRING | `SkuId` |
| `line_item_usage_amount` | DECIMAL | `UsageQuantity` |
| `line_item_unblended_cost` | DECIMAL | `BilledCost` (×1500 KRW 환산) |
| `line_item_blended_cost` | DECIMAL | `EffectiveCost` 참고용 |
| `product_region` | STRING | `RegionId` |
| `product_instance_type` | STRING | `ResourceType` |
| `pricing_unit` | STRING | `UsageUnit` |
| `pricing_term` | STRING | `CommitmentDiscountType` 파생 |
| `reservation_reservation_a_r_n` | STRING | `CommitmentDiscountId` |
| `resource_tags_user_*` | STRING | `Tags` 필드로 통합 |

### 4.2 Azure Cost Management Export 컬럼

| 컬럼 | 타입 | FOCUS 매핑 대상 |
|------|------|----------------|
| `Date` | DATE | `ChargePeriodStart` |
| `BillingPeriodStartDate` | DATE | `BillingPeriodStart` |
| `SubscriptionId` | STRING | `BillingAccountId` |
| `SubscriptionName` | STRING | `BillingAccountName` |
| `ResourceGroup` | STRING | `SubAccountId` (부분) |
| `ResourceId` | STRING | `ResourceId` |
| `MeterCategory` | STRING | `ServiceName` |
| `MeterSubCategory` | STRING | `ServiceCategory` 파생 |
| `MeterName` | STRING | `SkuName` |
| `UsageQuantity` | DECIMAL | `UsageQuantity` |
| `UnitOfMeasure` | STRING | `UsageUnit` |
| `CostInBillingCurrency` | DECIMAL | `BilledCost` (이미 KRW) |
| `BillingCurrency` | STRING | 통화 확인용 |
| `ResourceLocation` | STRING | `RegionId` |
| `ChargeType` | STRING | `ChargeCategory` |
| `ReservationId` | STRING | `CommitmentDiscountId` |
| `Tags` | JSON STRING | `Tags` |

### 4.3 GCP Billing Export 컬럼

| 컬럼 | 타입 | FOCUS 매핑 대상 |
|------|------|----------------|
| `billing_account_id` | STRING | `BillingAccountId` |
| `project_id` | STRING | `SubAccountId` |
| `project_name` | STRING | `SubAccountName` |
| `service_description` | STRING | `ServiceName` |
| `sku_description` | STRING | `SkuName` |
| `usage_start_time` | DATETIME | `ChargePeriodStart` |
| `usage_end_time` | DATETIME | `ChargePeriodEnd` |
| `location_region` | STRING | `RegionId` |
| `resource_name` | STRING | `ResourceName` |
| `resource_global_name` | STRING | `ResourceId` |
| `usage_amount` | DECIMAL | `UsageQuantity` |
| `usage_unit` | STRING | `UsageUnit` |
| `cost` | DECIMAL | `BilledCost` (×1500 KRW 환산) |
| `currency` | STRING | 통화 확인용 |
| `credits_amount` | DECIMAL | EffectiveCost 계산 시 차감 |
| `credits_type` | STRING | `CommitmentDiscountType` 파생 |
| `labels` | JSON STRING | `Tags` |
| `invoice_month` | STRING | `BillingPeriodStart` 월 |

---

## 5. Tags/labels JSON 인코딩 주의사항

### Azure Tags 파싱

Azure의 `Tags` 컬럼은 CSV 표준 이중 인용부호 이스케이프(`""` → `"`)가 적용된 JSON 문자열입니다. `csv` / `pandas` 표준 파서가 자동으로 언에스케이프 하므로, 애플리케이션 레벨에서는 일반 JSON 문자열로 처리됩니다:

```
{"Project": "web", "Environment": "prod", "Owner": "webteam@hbt.co.kr", "CostCenter": "CC-200"}
```

Python pandas로 읽을 때:

```python
import json, pandas as pd
df = pd.read_csv('azure-export-sample.csv', dtype=str).fillna('')
df['tags_parsed'] = df['Tags'].apply(lambda s: json.loads(s) if s else {})
```

> 만약 `""` 이스케이프가 보인다면(비표준 reader 사용 시) `s.replace('""','"').strip('"')` 으로 복원한 뒤 `json.loads` 하세요.

### GCP labels 파싱

GCP의 `labels` 컬럼은 표준 JSON 형식:

```
{"Project": "web", "Environment": "prod", "Owner": "sre@hbt.co.kr", "CostCenter": "CC-200"}
```

```python
df['labels_parsed'] = df['labels'].apply(
    lambda x: json.loads(x) if pd.notna(x) and x != '' else {}
)
```

---

## 6. 재생성 가이드

### 6.1 스크립트 실행

```bash
# finops-lab 루트 디렉토리에서 실행
python .temp/gen_samples.py
```

> **⚠ 주의**: `gen_samples.py`는 **AWS / GCP / Utilization CSV만** 재생성합니다.
> `azure-export-sample.csv`는 직접 편집으로 유지되는 산출물이며 스크립트 실행으로 덮어써지지 않습니다.
> Azure CSV를 수정해야 한다면 파일을 직접 편집하고 `.temp/azure-export-sample.csv.bak`(직전 백업)과 diff로 검증하세요.

### 6.2 수정 원칙

| 항목 | 수정 방법 |
|------|---------|
| 이상 비용 날짜 변경 | `gen_samples.py`에서 `d.day == 15` (AWS), `d.day == 20` (Azure), `d.day == 25` (GCP) 수정 |
| 태깅 누락 비율 조정 | 태깅 없는 리소스 추가/제거 또는 누락 일수 조정 |
| 비용 규모 조정 | 각 리소스의 `cost` 값 수정 (USD → KRW 환산 고려) |
| 신규 리소스 추가 | 해당 CSP의 `rows_*` 리스트에 행 추가 |

### 6.3 검증 체크리스트

```python
import json, pandas as pd

df_aws  = pd.read_csv('aws-cur-sample.csv',       dtype=str).fillna('')
df_az   = pd.read_csv('azure-export-sample.csv',  dtype=str).fillna('')
df_gcp  = pd.read_csv('gcp-billing-sample.csv',   dtype=str).fillna('')
df_util = pd.read_csv('utilization-sample.csv',   dtype=str).fillna('')

# 1. 이상 비용(Anomaly) 재현
aws_spike = df_aws[df_aws['line_item_resource_id']=='i-spike-001']
print('AWS 3/15 cost =', aws_spike[aws_spike['line_item_usage_start_date'].str.startswith('2026-03-15')]['line_item_unblended_cost'].values)  # 36.0
az_spike  = df_az[df_az['ResourceId'].str.contains('vm-spike-azure')]
print('Azure 3/20 cost(KRW) =', az_spike[az_spike['Date']=='2026-03-20']['CostInBillingCurrency'].values)  # 135000
gcp_spike = df_gcp[df_gcp['resource_name']=='gce-spike-1']
print('GCP 3/25 cost =', gcp_spike[gcp_spike['usage_start_time'].str.startswith('2026-03-25')]['cost'].values)  # 24.0

# 2. 태깅 누락률 (목표: AWS 8%, Azure 5±2%, GCP 10%)
print(f"AWS Project 누락률:    {(df_aws['resource_tags_user_project']=='').mean()*100:.2f}%")

def missing_key(s, key):
    try: return not json.loads(s).get(key,'') if s else True
    except: return True
print(f"Azure CostCenter 누락: {df_az['Tags'].apply(lambda s: missing_key(s,'CostCenter')).mean()*100:.2f}%")
print(f"GCP Environment 누락:  {df_gcp['labels'].apply(lambda s: missing_key(s,'Environment')).mean()*100:.2f}%")

# 3. 유휴 / 고아 / 과잉 검증
print('AWS idle EC2 usage=0 rows:', ((df_aws['line_item_resource_id'].isin(['i-idle-001','i-idle-002'])) & (df_aws['line_item_usage_amount'].astype(float)==0)).sum(), '(기대 60)')
print('AWS orphan EBS rows:',        df_aws['line_item_resource_id'].str.startswith('vol-orphan-').sum(), '(기대 90)')

util_aws = df_util[df_util['provider']=='AWS']
print('AWS overprov 평균 CPU:',
      f"{util_aws[util_aws['resource_id'].str.startswith('i-overprov')]['avg_cpu_percent'].astype(float).mean():.2f}%",
      '(목표 15%)')

# 4. Azure billing↔utilization 조인 검증
df_az['resource_last']  = df_az['ResourceId'].str.rsplit('/',1).str[-1]
df_util_az = df_util[df_util['provider']=='Azure'].copy()
df_util_az['resource_last'] = df_util_az['resource_id'].str.rsplit('/',1).str[-1]
missing = set(df_util_az['resource_last']) - set(df_az['resource_last'])
print('util에만 있고 billing에 없는 Azure 리소스:', missing, '(기대: set())')
```
