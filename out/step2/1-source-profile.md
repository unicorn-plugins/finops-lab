# 소스 빌링 스키마 프로파일

## AWS CUR 2.0

| 컬럼명 | 타입 | NULL% | 샘플값 | FOCUS 매핑 | 매핑 유형 |
|---|---|---|---|---|---|
| bill_billing_period_start_date | DateTime | 0% | 2026-03-01 | BillingPeriodStart | 직접 매핑 |
| bill_payer_account_id | String | 0% | 123456789012 | BillingAccountId | 직접 매핑 |
| line_item_usage_account_id | String | 0% | 123456789012 | SubAccountId | 직접 매핑 |
| line_item_usage_start_date | DateTime | 0% | 2026-03-01T00:00:00Z | ChargePeriodStart | 직접 매핑 |
| line_item_usage_end_date | DateTime | 0% | 2026-03-01T24:00:00Z | ChargePeriodEnd | 변환 필요 (T24→다음날 T00) |
| line_item_product_code | String | 0% | AmazonEC2 | ServiceName (룩업) | 변환 필요 |
| line_item_operation | String | 0% | RunInstances | ChargeDescription 보조 | 변환 필요 |
| line_item_resource_id | String | 약5% | i-web-001 | ResourceId | 직접 매핑 |
| line_item_usage_type | String | 0% | BoxUsage:m5.2xlarge | ChargeDescription | 직접 매핑 |
| line_item_usage_amount | Decimal | 0% | 24.0000 | ConsumedQuantity | 직접 매핑 |
| line_item_unblended_cost | Decimal | 0% | 9.2160 | BilledCost (×1500) | 변환 필요 (USD→KRW) |
| line_item_blended_cost | Decimal | 0% | 9.2160 | EffectiveCost (×1500) | 변환 필요 (USD→KRW) |
| product_region | String | 약3% | ap-northeast-2 | RegionId | 직접 매핑 |
| product_instance_type | String | 약3% | m5.2xlarge | ResourceType 보조 | 변환 필요 |
| pricing_unit | String | 0% | Hrs | ConsumedUnit | 직접 매핑 |
| pricing_term | String | 0% | OnDemand | ChargeCategory/PricingCategory | 변환 필요 |
| reservation_reservation_a_r_n | String | ~100% | (빈값) | CommitmentDiscountId | 직접 매핑 (null 처리) |
| resource_tags_user_project | String | 약5% | web | Tags.Project | 변환 필요 (JSON 조합) |
| resource_tags_user_environment | String | 약5% | prod | Tags.Environment | 변환 필요 (JSON 조합) |
| resource_tags_user_owner | String | 약5% | webteam@hbt.co.kr | Tags.Owner | 변환 필요 (JSON 조합) |
| resource_tags_user_cost_center | String | 약5% | CC-200 | Tags.CostCenter | 변환 필요 (JSON 조합) |

### FOCUS 매핑 불가 항목 (AWS)

| FOCUS 컬럼 | 처리 방안 |
|---|---|
| BillingAccountName | 고정값 "hbt-prod-aws" 사용 |
| BillingPeriodEnd | 고정값 "2026-04-01T00:00:00Z" (월 기준) |
| ServiceProviderName | 고정값 "Amazon Web Services" |
| ListCost / ListUnitPrice | 샘플 데이터에 공개가 미포함 → null |
| AmortizedCost (RI) | 샘플에 RI 행 없음 → EffectiveCost와 동일 처리 |

---

## Azure Cost Export

| 컬럼명 | 타입 | NULL% | 샘플값 | FOCUS 매핑 | 매핑 유형 |
|---|---|---|---|---|---|
| Date | Date | 0% | 2026-03-01 | ChargePeriodStart (T00:00:00Z 추가) | 변환 필요 |
| BillingPeriodStartDate | Date | 0% | 2026-03-01 | BillingPeriodStart | 직접 매핑 |
| SubscriptionId | String | 0% | 00000000-...-000001 | BillingAccountId | 직접 매핑 |
| SubscriptionName | String | 0% | HBT-Enterprise | BillingAccountName | 직접 매핑 |
| ResourceGroup | String | 약2% | rg-web | SubAccountId / SubAccountName | 직접 매핑 |
| ResourceId | String | 약2% | /subscriptions/.../virtualMachines/... | ResourceId | 직접 매핑 |
| MeterCategory | String | 0% | Virtual Machines | ServiceName (룩업) | 변환 필요 |
| MeterSubCategory | String | 약5% | D Series | ChargeDescription 보조 | 변환 필요 |
| MeterName | String | 0% | D2s v3 | ChargeDescription 보조 | 직접 매핑 |
| UsageQuantity | Decimal | 0% | 24 | ConsumedQuantity | 직접 매핑 |
| UnitOfMeasure | String | 0% | Hours | ConsumedUnit | 직접 매핑 |
| CostInBillingCurrency | Decimal | 0% | 22500 | BilledCost (이미 KRW) | 직접 매핑 |
| BillingCurrency | String | 0% | KRW | BillingCurrency | 직접 매핑 |
| ResourceLocation | String | 약2% | koreacentral | RegionId | 직접 매핑 |
| ChargeType | String | 0% | Usage | ChargeCategory | 변환 필요 |
| ReservationId | String | ~100% | (빈값) | CommitmentDiscountId | 직접 매핑 (null 처리) |
| Tags | JSON | 약5% | {"Project":"web",...} | Tags | 변환 필요 (JSON 파싱) |

### FOCUS 매핑 불가 항목 (Azure)

| FOCUS 컬럼 | 처리 방안 |
|---|---|
| ServiceProviderName | 고정값 "Microsoft Azure" 사용 |
| BillingPeriodEnd | 고정값 "2026-04-01T00:00:00Z" |
| ChargePeriodEnd | Date + 1일 파생 |
| ServiceCategory | MeterCategory 룩업 테이블로 파생 |

---

## GCP Billing Export

| 컬럼명 | 타입 | NULL% | 샘플값 | FOCUS 매핑 | 매핑 유형 |
|---|---|---|---|---|---|
| billing_account_id | String | 0% | 01AB12-CD34EF-567890 | BillingAccountId | 직접 매핑 |
| project_id | String | 0% | acme-prod-001 | SubAccountId | 직접 매핑 |
| project_name | String | 0% | HBT Production | BillingAccountName / SubAccountName | 직접 매핑 |
| service_description | String | 0% | Compute Engine | ServiceName (룩업) | 변환 필요 |
| sku_description | String | 0% | N2 Instance Core running in Korea | ChargeDescription | 직접 매핑 |
| usage_start_time | DateTime | 0% | 2026-03-01T00:00:00Z | ChargePeriodStart | 직접 매핑 |
| usage_end_time | DateTime | 0% | 2026-03-01T24:00:00Z | ChargePeriodEnd | 변환 필요 (T24→다음날 T00) |
| location_region | String | 약3% | asia-northeast3 | RegionId | 직접 매핑 |
| resource_name | String | 약5% | gce-web-001 | ResourceName | 직접 매핑 |
| resource_global_name | String | 약5% | //compute.googleapis.com/... | ResourceId | 직접 매핑 |
| usage_amount | Decimal | 0% | 24.0000 | ConsumedQuantity | 직접 매핑 |
| usage_unit | String | 0% | hours | ConsumedUnit | 직접 매핑 |
| cost | Decimal | 0% | 4.6460 | BilledCost (×1500 USD→KRW) | 변환 필요 |
| currency | String | 0% | USD | BillingCurrency → "KRW" | 변환 필요 |
| credits_amount | Decimal | 약70% | 0.0000 | EffectiveCost = (cost+credits)×1500 | 변환 필요 |
| credits_type | String | 약70% | COMMITTED_USAGE_DISCOUNT | CommitmentDiscountType | 변환 필요 |
| labels | JSON | 약10% | {"Project":"web",...} | Tags | 변환 필요 (JSON 파싱) |
| invoice_month | String | 0% | 2026-03 | BillingPeriodStart 파생 | 변환 필요 |

### FOCUS 매핑 불가 항목 (GCP)

| FOCUS 컬럼 | 처리 방안 |
|---|---|
| ServiceProviderName | 고정값 "Google Cloud Platform" 사용 |
| BillingPeriodEnd | 고정값 "2026-04-01T00:00:00Z" |
| ServiceCategory | service_description 룩업 테이블로 파생 |
| RegionName | location_region 룩업 ("asia-northeast3" → "Seoul") |

---

## SaaS LLM (OpenAI/Anthropic)

| 컬럼명 | 타입 | NULL% | 샘플값 | FOCUS 매핑 | 매핑 유형 |
|---|---|---|---|---|---|
| date | Date | 0% | 2026-03-01 | ChargePeriodStart | 변환 필요 (T00:00:00Z 추가) |
| provider | String | 0% | anthropic | ServiceProviderName | 변환 필요 |
| model | String | 0% | claude-3-5-sonnet | ModelName (AI 확장) | 직접 매핑 |
| project | String | 약5% | api | SubAccountId | 직접 매핑 |
| cost_center | String | 약5% | CC-200 | Tags.CostCenter | 변환 필요 |
| tokens_input | Integer | 0% | 416368 | TokenCountInput (AI 확장) | 직접 매핑 |
| tokens_output | Integer | 0% | 100989 | TokenCountOutput (AI 확장) | 직접 매핑 |
| request_count | Integer | 0% | 3450 | - | 파생 불가 (FOCUS 미지원) |
| cost_usd | Decimal | 0% | 2.7639 | BilledCost (×1500 USD→KRW) | 변환 필요 |
| api_key_hash | String | 0% | sk-18efa72c957d57e8 | BillingAccountId | 직접 매핑 |
| tags | JSON | 약5% | {"Environment":"prod",...} | Tags | 변환 필요 (JSON 파싱) |

### FOCUS 매핑 불가 항목 (SaaS LLM)

| FOCUS 컬럼 | 처리 방안 |
|---|---|
| ResourceId / ResourceName | SaaS 특성상 리소스 미식별 → null |
| RegionId / RegionName | 리전 정보 없음 → null |
| GpuHours / GpuUtilization | 토큰 기반 과금 (GPU 직접 노출 없음) → null |
| request_count | FOCUS 표준 컬럼 없음 → 미포함 |

---

## 파생 불가 항목 및 처리 방안 (전체)

| 소스 | 항목 | 처리 방안 |
|---|---|---|
| 전체 | GpuUtilization | utilization-sample.csv에 GPU 컬럼 없음 → null 처리 |
| AWS | AmortizedCost (RI/SP) | 샘플에 RI 행 없음 (OnDemand만) → AmortizedCost = EffectiveCost |
| AWS | ListCost / ListUnitPrice | 공개가 미포함 → null |
| Azure | BillingPeriodEnd | 소스 미제공 → "2026-04-01T00:00:00Z" 고정 |
| GCP | ServiceCategory | service_description 룩업으로 파생 (Vertex AI → AI and Machine Learning) |
| SaaS LLM | ResourceId | API 기반 과금, 리소스 식별자 없음 → null |
| SaaS LLM | GpuHours | 토큰 기반 과금, GPU 시간 미노출 → null |
