# FOCUS v1.3 매핑 정의 — (주)하이브리지텔레콤 (HBT)

## 개요

AWS CUR 2.0 · Azure Cost Export · GCP Billing · SaaS LLM(OpenAI/Anthropic) 4종 소스를  
FOCUS v1.3 스키마로 정규화하는 매핑 정의 모음.

| 파일 | 소스 | 통화 처리 | 행 수(2026-03) |
|---|---|---|---|
| `aws-cur-to-focus.yaml` | AWS CUR 2.0 | USD × 1,500 → KRW | 784 |
| `azure-export-to-focus.yaml` | Azure Cost Export | 이미 KRW (변환 없음) | 930 |
| `gcp-billing-to-focus.yaml` | GCP Billing Export | USD × 1,500 → KRW | 424 |
| `saas-llm-to-focus.yaml` | SaaS LLM (OpenAI/Anthropic) | USD × 1,500 → KRW | 197 |

출력 파일: `out/focus-normalized.csv` (총 2,335행)

---

## FOCUS v1.3 Mandatory 15종 컬럼

| # | 컬럼명 | 타입 | 설명 |
|---|---|---|---|
| 1 | BilledCost | Decimal(KRW) | 인보이스 기준 최종 청구 비용 |
| 2 | EffectiveCost | Decimal(KRW) | RI/SP 상각 반영 실질 비용 |
| 3 | BillingAccountId | String | 빌링 계정 식별자 |
| 4 | BillingAccountName | String | 빌링 계정 표시명 |
| 5 | BillingCurrency | String | 청구 통화 (KRW) |
| 6 | BillingPeriodStart | DateTime(UTC) | 청구 기간 시작 |
| 7 | BillingPeriodEnd | DateTime(UTC) | 청구 기간 종료 (exclusive) |
| 8 | ChargePeriodStart | DateTime(UTC) | 청구 항목 기간 시작 |
| 9 | ChargePeriodEnd | DateTime(UTC) | 청구 항목 기간 종료 (exclusive) |
| 10 | ChargeCategory | String | Usage / Purchase / Tax / Credit / Adjustment |
| 11 | ChargeClass | String | null(정상) / Correction(정정) |
| 12 | ChargeDescription | String | 청구 항목 자체 완결형 설명 |
| 13 | ServiceCategory | String | 서비스 최상위 분류 (19종) |
| 14 | ServiceName | String | 서비스 표시명 |
| 15 | ServiceProviderName | String | 서비스 공급자명 (v1.3 신규 필수) |

---

## 통화 변환 규칙

```
BilledCost_KRW = source_cost_usd × 1,500
소수점 처리: round(value, 2) — 2자리 반올림
적용 소스: AWS (line_item_unblended_cost), GCP (cost), SaaS LLM (cost_usd)
비적용 소스: Azure (CostInBillingCurrency 이미 KRW)
```

---

## Amortized 비용 계산 로직

### RI/SP 행 (선납 비용 포함)

```
AmortizedCost_KRW = EffectiveCost_KRW + (UpfrontFee_KRW / CommitmentPeriodHours × UsageHours)
```

### 온디맨드 행

```
AmortizedCost_KRW = ListCost_KRW × (1 - DiscountRate)
= EffectiveCost_KRW  (DiscountRate=0인 경우)
```

### 샘플 데이터 적용 결과

2026-03 샘플은 AWS OnDemand 전용이므로 `AmortizedCost_KRW = EffectiveCost_KRW` 적용.  
GCP CUD 크레딧은 `credits_amount`(음수)가 `cost`에 합산되어 `EffectiveCost`에 자동 반영.

---

## AI 확장 컬럼 5종 정의

| 컬럼명 | 타입 | 설명 | 적용 소스 |
|---|---|---|---|
| TokenCountInput | Integer | 입력 토큰 수 (prompt_tokens / input_tokens) | SaaS LLM |
| TokenCountOutput | Integer | 출력 토큰 수 (completion_tokens / output_tokens) | SaaS LLM |
| ModelName | String | AI 모델 식별자 (예: claude-3-5-sonnet, gpt-4o) | SaaS LLM, GCP Vertex AI |
| GpuHours | Decimal | GPU 사용 시간 (UsageAmount × GPU 수량) | CSP GPU 인스턴스 (샘플 미존재) |
| GpuUtilization | Decimal | GPU 활용률 (%) — utilization-sample.csv 조인 | GPU 리소스 (샘플 GPU 컬럼 없어 null) |

### AI 행 식별 규칙

| 소스 | 식별 조건 |
|---|---|
| AWS | `line_item_product_code IN ('AmazonBedrock', 'AWSBedrockRuntime')` 또는 `line_item_usage_type LIKE '%GPU%'` |
| Azure | `MeterCategory = 'Azure OpenAI'` |
| GCP | `service_description = 'Vertex AI'` |
| SaaS LLM | 전체 행 (provider IN ('anthropic', 'openai')) |

### GpuUtilization 조인 방법

```
JOIN KEY: billing_row.ResourceId = utilization_sample.resource_id
          AND billing_row.ChargePeriodStart[:10] = utilization_sample.date
RESULT:   GpuUtilization = utilization_sample.avg_gpu_percent  (해당 컬럼 없으면 null)
FALLBACK: 매칭 불가 행 → null
```

현재 `utilization-sample.csv`에 GPU 전용 컬럼이 없으므로 전체 GpuUtilization = null.  
GPU 컬럼(`avg_gpu_percent`) 추가 시 자동 반영 가능한 구조로 설계됨.

---

## ServiceCategory 매핑 요약

| 서비스 | ServiceCategory | ServiceSubcategory |
|---|---|---|
| Amazon EC2 / Azure VM / GCP Compute Engine | Compute | Virtual Machines |
| AWS Lambda / GCP Cloud Functions | Compute | Serverless Compute |
| Amazon RDS / Azure SQL / GCP Cloud SQL | Databases | Relational Databases |
| Amazon S3 / Azure Blob / GCP Cloud Storage | Storage | Object Storage |
| Amazon CloudWatch / Azure Monitor | Management and Governance | Observability |
| GCP BigQuery | Analytics | Data Processing |
| GCP Vertex AI | AI and Machine Learning | Machine Learning |
| Azure App Service | Web | Other (Web) |
| Anthropic API / OpenAI API | AI and Machine Learning | Generative AI |

---

## 주요 변환 패턴

| 패턴명 | 설명 | 적용 사례 |
|---|---|---|
| `time_normalize` | T24:00:00Z → 다음날 T00:00:00Z | AWS/GCP ChargePeriodEnd |
| `datetime_append` | 날짜 문자열 + T00:00:00Z | Azure Date, SaaS date |
| `date_add_1` | 날짜 + 1일 | Azure/SaaS ChargePeriodEnd |
| `multiply` | × 1500 (소수점 2자리 반올림) | AWS/GCP/SaaS BilledCost |
| `lookup` | 서비스명 룩업 테이블 | ServiceName, ServiceCategory |
| `json_build` | 개별 태그 컬럼 → JSON 객체 | AWS Tags |
| `json_parse` | JSON 문자열 파싱 | Azure/GCP/SaaS Tags |
| `null_if_empty` | 빈 문자열 → null | CommitmentDiscountId, SubAccountId |
| `split_last` | 경로 마지막 세그먼트 추출 | Azure ResourceName |
