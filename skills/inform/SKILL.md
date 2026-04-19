---
name: inform
description: "FOCUS 정규화 & 통합 가시성 — 3 CSP + SaaS LLM → FOCUS v1.3 + AI 확장 5종, 태깅 거버넌스, 이상 탐지, Chart.js 9차트 대시보드"
type: orchestrator
user-invocable: true
---

# Inform

[INFORM 활성화]

## 목표

3 CSP(AWS·Azure·GCP) + SaaS LLM 빌링 데이터를 FOCUS v1.3 + AI 확장 5종으로 정규화함. 태깅 거버넌스 정책을 수립하고, 비용 이상 탐지 5건을 식별하며, Chart.js 9차트 단일 HTML 대시보드를 산출함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@inform` 멘션
- "FOCUS 정규화", "대시보드" 키워드 포함
- `/finops:inform` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트 | FQN | 티어 | 순서 |
|---|---|---|---|
| focus-normalizer | `finops:focus-normalizer:focus-normalizer` | MEDIUM | 1 |
| tag-governor | `finops:tag-governor:tag-governor` | LOW | 2 |
| cost-analyst | `finops:cost-analyst:cost-analyst` | MEDIUM | 3 |

### 프롬프트 조립 지시

각 에이전트 호출 전 다음 순서로 프롬프트를 조립함 (combine-prompt.md 규약):
1. 해당 에이전트의 `agents/{agent-name}/AGENT.md` 전문 로드
2. `agents/{agent-name}/agentcard.yaml` 역량·제약·핸드오프 섹션 로드
3. 해당 Phase의 TASK·EXPECTED OUTCOME·MUST DO·MUST NOT DO·CONTEXT를 조합하여 단일 프롬프트 완성

### 호출

```
Agent(
  subagent_type="finops:{agent}:{agent}",
  model={티어} 모델,
  prompt=조립된 프롬프트
)
```

## 워크플로우

### Phase 1: 입력 확인 (`ulw` 활용)

다음 파일 존재 여부를 확인함:
- `resources/sample-billing/aws-cur-sample.csv`
- `resources/sample-billing/azure-export-sample.csv`
- `resources/sample-billing/gcp-billing-sample.csv`
- `resources/sample-billing/utilization-sample.csv`
- `resources/sample-billing/saas-llm-sample.csv`
- `resources/schema/focus-v1.yaml`
- `references/am/finops.md` §4.5~§4.11·§4.16

파일 누락 시 사용자에게 알리고 중단함.

### Phase 2: 원본 프로파일링 + FOCUS 매핑 + 병합 → Agent: focus-normalizer (`/oh-my-claudecode:ralph` 활용)

- **TASK**: schema-profiler → unit-converter → ai-extension-mapper 순서로 Step 2-1~2-3 실행함
- **EXPECTED OUTCOME**:
  - `out/step2/1-source-profile.md` — 소스별 컬럼 목록 표 + FOCUS 매핑 가능성 평가 표 + 파생 불가 항목 처리 방안
  - `resources/mapping/aws-cur-to-focus.yaml` — AWS CUR 컬럼 매핑 정의
  - `resources/mapping/azure-export-to-focus.yaml` — Azure Export 컬럼 매핑 정의
  - `resources/mapping/gcp-billing-to-focus.yaml` — GCP Billing 컬럼 매핑 정의
  - `resources/mapping/saas-llm-to-focus.yaml` — SaaS LLM 컬럼 매핑 정의
  - `resources/mapping/README.md` — 매핑 YAML 4종 개요 및 변환 규칙 요약
  - `out/focus-normalized.csv` — FOCUS Mandatory 15종 + AI 확장 5종 컬럼 포함, 월 총합 원본 ±0.01 KRW 일치
- **MUST DO**:
  - USD→KRW 환율 ×1,500 적용
  - Amortized 비용 계산식 적용 (RI/SP 선납 비용 비례 배분)
  - AI 확장 컬럼(TokenCountInput·TokenCountOutput·ModelName·GpuHours·GpuUtilization) 5종 통합
  - `resources/sample-billing/utilization-sample.csv`를 ResourceId 기준 조인하여 GpuUtilization 계산
  - FOCUS v1.3 spec_version 준수
- **MUST NOT DO**:
  - FOCUS v1.3 spec_version 변경 금지
  - 원본 빌링 CSV 직접 수정 금지
  - 대시보드 생성·태깅 거버넌스·비용 최적화 권고 수행 금지
- **CONTEXT**:
  - `resources/sample-billing/*.csv` (5종)
  - `resources/schema/focus-v1.yaml`
  - `references/am/finops.md` §4.5~§4.11·§4.16

### Phase 3: 태깅 갭 분석 → Agent: tag-governor (`/oh-my-claudecode:ulw` 활용)

- **TASK**: Step 2-4 실행 — 필수 4종 태그(CostCenter·Project·Environment·Owner) 커버리지 측정, tag-policy.yaml 런타임 생성
- **EXPECTED OUTCOME**:
  - `out/step2/4-tag-coverage.md` — CSP별 누락률 표 (AWS≈8%·Azure≈5%·GCP≈10%·AI≈12%, ±2%p 허용)
  - `resources/templates/tag-policy.yaml` — HBT 프로파일·COVERS 원칙 기반 태그 정책 정의
- **MUST DO**:
  - HBT 회사 프로파일(`resources/basic-info/company-profile.md`) 기반 정책 생성
  - COVERS 원칙 연계 태그 정책 근거 명시
  - AI 특화 규칙(API Key 기반 chargeback·model metadata 태깅) 포함
  - 누락률 실측 데이터 기반 산출
- **MUST NOT DO**:
  - 임의 누락률 수치 조작 금지 (실측 기반만 허용)
  - 데이터 정규화·대시보드 생성 수행 금지
- **CONTEXT**:
  - `out/focus-normalized.csv` (Phase 2 산출물)
  - `resources/basic-info/company-profile.md`

### Phase 4: 이상 탐지 + 대시보드 → Agent: cost-analyst (`/oh-my-claudecode:ralph` 활용)

- **TASK**: Step 2-5 실행 — 이상 비용 5단계 탐지(CSP 3건 + AI 2건) + Chart.js 9차트 대시보드 단일 HTML 생성
- **EXPECTED OUTCOME**:
  - `out/dashboard.html` — 파일 크기 1.2MB 미만, 오프라인 열람 가능, 기간 슬라이더·CostCenter/Project/Model 필터·CSP/AI 탭·다크모드 포함
  - 이상 비용 5건 목록 (CSP 3 + AI 2, 각 항목에 탐지 근거 명시)
  - Chart.js 9차트 구성: CSP 차트 5개 + AI 차트 4개
- **MUST DO**:
  - Chart.js 4.x CDN 스크립트 인라인 삽입
  - 정규화 CSV 데이터를 `<script>` 태그 내 JSON으로 인라인 임베드
  - 9차트 완비 (CSP 5: 월별 추이·서비스별·리전별·탑 10 리소스·이상비용 / AI 4: 모델별·토큰별·GPU 활용률·비용 예측)
  - 기간 슬라이더·필터·탭·다크모드 UI 구현
- **MUST NOT DO**:
  - 외부 서버 의존 금지 (CDN 제외한 동적 데이터 로드 금지)
  - 1.2MB 초과 파일 생성 금지
- **CONTEXT**:
  - `out/focus-normalized.csv`
  - `resources/sample-billing/utilization-sample.csv`

### Phase 5: 검증 및 보고 (`/oh-my-claudecode:verify` 활용)

다음 항목을 순서대로 검증함:
- [ ] `out/focus-normalized.csv` 월 총합이 원본 합산과 ±0.01 KRW 이내 일치
- [ ] `out/dashboard.html` 파일 크기 1.2MB 미만 확인
- [ ] 9차트 HTML 내 Chart.js 인스턴스 9개 존재 확인
- [ ] CSP·AI 탭 존재 확인
- [ ] 이상 비용 5건(CSP 3 + AI 2) 목록 확인
- [ ] `out/step2/4-tag-coverage.md` 존재 및 CSP별 누락률 표 포함 확인

검증 통과 후 핵심 결과 요약 보고 및 다음 단계 `/finops:optimize` 권장.

## 완료 조건

- [ ] `out/focus-normalized.csv` 월 총합 원본 ±0.01 KRW 일치
- [ ] `out/dashboard.html` 내 9차트 존재
- [ ] 이상 비용 5건 목록 산출 (CSP 3 + AI 2)
- [ ] `out/step2/4-tag-coverage.md` CSP별 누락률 표 포함
- [ ] `resources/templates/tag-policy.yaml` 생성 완료

## 검증 프로토콜

1. focus-normalizer·tag-governor·cost-analyst 각 AGENT.md 검증 섹션 통과
2. Phase 5 파일 존재 및 크기 확인
3. `out/dashboard.html` 내 `new Chart(` 패턴 9건 이상 확인
4. 이상 탐지 5건 항목 각각에 탐지 근거 문자열 존재 확인

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/step2/`, `out/`, `resources/mapping/`, `resources/templates/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료.

## 재개

마지막 완료 Phase 번호를 확인하고 해당 Phase 다음부터 재개함. 다음 파일 존재 여부로 완료 Phase를 판단함:
- Phase 2 완료: `out/focus-normalized.csv`
- Phase 3 완료: `resources/templates/tag-policy.yaml`
- Phase 4 완료: `out/dashboard.html`

## 출력 형식

### 사용자 보고 형식 (권장)

```
## Inform 결과 요약

### FOCUS 정규화
- 총 행 수: N행
- 월 총합 검증: 원본 ±0.01 KRW 이내 일치

### 태깅 갭 현황
| CSP | 누락률 |
|---|---|
| AWS | ~8% |
| Azure | ~5% |
| GCP | ~10% |
| AI | ~12% |

### 이상 비용 탐지
| # | CSP/AI | 항목 | 탐지 근거 |
|---|---|---|---|

### 대시보드
- 파일: out/dashboard.html (NMB)
- 차트: 9개 (CSP 5 + AI 4)

### 다음 단계
→ `/finops:optimize` 으로 Right-sizing 및 약정 최적화를 시작하세요.
```
