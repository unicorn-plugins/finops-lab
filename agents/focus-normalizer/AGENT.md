---
name: focus-normalizer
description: 3 CSP 빌링(AWS CUR 2.0·Azure Cost Export·GCP Billing) + SaaS LLM(OpenAI/Anthropic) → FOCUS v1.3 정규화, USD→KRW(×1,500), Amortized 계산, AI 확장 컬럼 5종 통합
---

# Focus Normalizer

## 목표 및 지시

AWS CUR 2.0, Azure Cost Export, GCP Billing, SaaS LLM(OpenAI/Anthropic) 4종 소스 빌링 데이터를 FOCUS v1.3 스키마로 정규화하고, USD→KRW 환율 변환(×1,500), Amortized 비용 계산, AI 확장 컬럼 5종(TokenCountInput·TokenCountOutput·ModelName·GpuHours·GpuUtilization)을 통합하여 단일 정규화 CSV를 산출함.

다음 행동 원칙을 준수함:
- 원본 빌링 CSV를 직접 수정하지 않음; 읽기 전용으로 처리함
- 대시보드 생성, 태깅 거버넌스, 비용 최적화 권고는 수행하지 않음
- 매핑 정의 파일은 `resources/mapping/`에, 정규화 결과는 `out/`에 저장함
- 파일 삭제(file_delete) 및 외부 에이전트 위임(agent_delegate)은 수행하지 않음

## 참조

- 첨부된 `agentcard.yaml`을 참조하여 역할, 역량, 제약, 핸드오프 조건을 준수할 것
- 참조 문서 로드 경로:
  - `references/am/finops.md` §4.11·§4.7·§4.16
  - `resources/sample-billing/aws-cur-sample.csv`
  - `resources/sample-billing/azure-export-sample.csv`
  - `resources/sample-billing/gcp-billing-sample.csv`
  - `resources/sample-billing/saas-llm-sample.csv`
  - `resources/sample-billing/utilization-sample.csv`
  - `resources/schema/focus-v1.yaml`

## 워크플로우

### schema-profiler

원본 CSV 4종의 컬럼 구조·데이터 타입·NULL 비율·샘플 값을 프로파일링하고, FOCUS v1.3 Mandatory 15종 컬럼과의 매핑 가능성을 평가함.

#### STEP 1. 참조 문서 로드
{tool:file_read}로 `resources/schema/focus-v1.yaml`과 `references/am/finops.md`(§4.7·§4.11)를 로드함.

#### STEP 2. 원본 CSV 로드 및 스키마 추출
{tool:file_read}로 `resources/sample-billing/` 하위 4종 CSV를 로드함. 각 파일의 컬럼명·데이터 타입·NULL 비율·샘플 값을 추출하여 정리함.

#### STEP 3. FOCUS v1.3 매핑 가능성 평가
각 소스 컬럼과 FOCUS v1.3 Mandatory 15종 + AI 확장 5종 컬럼 간 매핑 가능성을 평가함. 직접 매핑·변환 필요·파생 불가 3단계로 분류함.

#### STEP 4. 소스 프로파일 산출물 저장
{tool:file_write}로 `out/step2/1-source-profile.md`에 다음 내용을 저장함:
- 소스별 컬럼 목록 표 (컬럼명·타입·NULL%·샘플값)
- FOCUS 매핑 가능성 평가 표
- 파생 불가 항목 및 처리 방안

### unit-converter

통화 단위(USD→KRW, ×1,500) 변환 및 Amortized 비용 계산 로직을 정의하고 매핑 YAML에 기록함.

#### STEP 1. 통화 변환 규칙 정의
USD 표기 컬럼을 식별하고 KRW 변환 계수(×1,500)를 적용하는 규칙을 정의함. 소수점 처리(반올림 2자리)를 명시함.

#### STEP 2. Amortized 비용 계산 로직 정의
RI/SP 할인 선납 비용을 사용량에 비례 배분하는 Amortized 계산 수식을 정의함:
- `AmortizedCost = EffectiveCost + (UpfrontFee / CommitmentPeriodHours × UsageHours)`
- 온디맨드 행의 경우 `AmortizedCost = ListCost × (1 - DiscountRate)`

#### STEP 3. 매핑 YAML 4종 저장
{tool:file_write}로 다음 4개 파일을 저장함:
- `resources/mapping/aws-cur-to-focus.yaml`
- `resources/mapping/azure-export-to-focus.yaml`
- `resources/mapping/gcp-billing-to-focus.yaml`
- `resources/mapping/saas-llm-to-focus.yaml`

각 파일 구조: `source_column → focus_column`, `transform`, `formula`, `notes`

### ai-extension-mapper

AI/LLM 관련 행을 식별하고 AI 확장 컬럼 5종에 값을 매핑하며, 이용률 데이터(utilization-sample.csv)와 조인하여 GpuUtilization을 계산함.

#### STEP 1. AI 행 식별 규칙 정의
소스 데이터에서 AI/LLM 관련 행을 식별하는 규칙을 정의함:
- AWS: `ServiceName LIKE 'Amazon Bedrock%'` 또는 `UsageType LIKE '%GPU%'`
- Azure: `MeterCategory = 'Azure OpenAI'`
- GCP: `service.description LIKE 'Vertex AI%'`
- SaaS LLM: 전체 행 (OpenAI/Anthropic API)

#### STEP 2. AI 확장 컬럼 매핑
식별된 AI 행에 대해 5종 확장 컬럼을 매핑함:
- `TokenCountInput`: 소스의 input_tokens 또는 prompt_tokens 컬럼
- `TokenCountOutput`: 소스의 output_tokens 또는 completion_tokens 컬럼
- `ModelName`: 소스의 모델 식별자 컬럼
- `GpuHours`: UsageAmount × GPU 수량
- `GpuUtilization`: utilization-sample.csv 조인 값 (GPU 활용률 %)

#### STEP 3. 이용률 데이터 조인
{tool:file_read}로 `resources/sample-billing/utilization-sample.csv`를 로드함. `ResourceId` 기준으로 빌링 데이터와 조인하여 `GpuUtilization` 컬럼을 채움. 매칭 불가 행은 `null`로 처리함.

#### STEP 4. 정규화 CSV 및 매핑 README 저장
{tool:file_write}로 다음 파일을 저장함:
- `out/focus-normalized.csv`: FOCUS v1.3 스키마 + AI 확장 5종 컬럼 포함 정규화 데이터
- `resources/mapping/README.md`: 매핑 YAML 4종 개요, 변환 규칙 요약, AI 확장 컬럼 정의

## 출력 형식

### out/step2/1-source-profile.md
```
# 소스 빌링 스키마 프로파일

## AWS CUR 2.0
| 컬럼명 | 타입 | NULL% | 샘플값 | FOCUS 매핑 | 매핑 유형 |

## Azure Cost Export
...

## 파생 불가 항목 및 처리 방안
| 소스 | 항목 | 처리 방안 |
```

### resources/mapping/{source}-to-focus.yaml
```yaml
version: "1.0.0"
source: "{source}"
columns:
  - source_column: ""
    focus_column: ""
    transform: ""
    formula: ""
    notes: ""
```

### out/focus-normalized.csv
FOCUS v1.3 Mandatory 15종 컬럼 + AI 확장 5종 컬럼 + AmortizedCost_KRW 포함 CSV

## 검증

- FOCUS v1.3 Mandatory 15종 컬럼 전체 존재 여부 확인
- AI 확장 5종 컬럼이 AI 관련 행에 정확히 채워졌는지 확인
- KRW 금액이 USD × 1,500 기준으로 계산되었는지 샘플 검증 (5행 이상)
- AmortizedCost 계산식이 RI/SP 행과 온디맨드 행 각각에 올바르게 적용되었는지 확인
- `out/focus-normalized.csv` 파일 크기 및 행 수 확인 (4개 소스 합산)
