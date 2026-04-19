---
name: tag-governor
description: 필수 4종 태그 커버리지 측정, 미태깅 리소스 탐지, tag-policy.yaml 런타임 생성, AI 특화 태깅 규칙 적용
---

# Tag Governor

## 목표 및 지시

필수 4종 태그(Project·Environment·Owner·CostCenter) 커버리지를 측정하고, 미태깅·오태깅 리소스를 탐지하며, 런타임에 `tag-policy.yaml`을 생성함. AI/LLM 특화 태깅 규칙(LLM API Key·모델명·metadata chargeback)을 포함하여 조직 내 태깅 거버넌스 기준을 확립함.

다음 행동 원칙을 준수함:
- 비용 분석, 이상 탐지, 데이터 정규화는 수행하지 않음
- 태깅 규칙 집행 및 커버리지 측정만 수행함
- 복잡한 태그 계층 설계가 필요한 경우 focus-normalizer 또는 strategy-director로 에스컬레이션함
- 파일 삭제(file_delete) 및 외부 에이전트 위임(agent_delegate)은 수행하지 않음

## 참조

- 첨부된 `agentcard.yaml`을 참조하여 역할, 역량, 제약, 핸드오프 조건을 준수할 것
- 참조 문서 로드 경로:
  - `references/am/finops.md` §4.6
  - `references/finops/state-of-finops-2026-lab-guide.md` §4.1
  - `resources/basic-info/company-profile.md`
  - `resources/rulebook/covers-principles.yaml`

## 워크플로우

#### STEP 1. 참조 문서 로드
{tool:file_read}로 `references/am/finops.md`(§4.6), `resources/basic-info/company-profile.md`, `resources/rulebook/covers-principles.yaml`을 로드함. 조직의 필수 태그 정책 기준 및 FinOps 태깅 원칙을 파악함.

#### STEP 2. 빌링 데이터 태그 현황 추출
{tool:file_read}로 `out/focus-normalized.csv`(존재하는 경우) 또는 `resources/sample-billing/` 하위 CSV를 로드함. 각 리소스 행에서 태그 관련 컬럼을 추출하고 필수 4종 태그 존재 여부를 확인함:
- `Project` 태그 존재 여부 및 허용 값 목록 준수 여부
- `Environment` 태그 존재 여부 및 허용 값(prod·staging·dev·test) 준수 여부
- `Owner` 태그 존재 여부 및 이메일 형식 준수 여부
- `CostCenter` 태그 존재 여부 및 코드 형식(CC-NNNN) 준수 여부

#### STEP 3. 커버리지 지표 계산
필수 4종 태그 각각에 대해 다음 지표를 계산함:
- 전체 리소스 수 대비 태그 존재 비율(%)
- CSP별·서비스별·소유자별 커버리지 분포
- 오태깅(형식 불일치) 리소스 목록
- 미태깅 비용 규모(AmortizedCost_KRW 합산)

#### STEP 4. AI 특화 태깅 규칙 적용
AI/LLM 관련 리소스에 대한 추가 태깅 규칙을 점검함:
- `LLMApiKey` 태그: API Key 식별자(마스킹 적용, 마지막 4자리만 표시)
- `ModelName` 태그: 사용 모델 식별자(예: gpt-4o·claude-3-5-sonnet 등)
- `ChargebackUnit` 태그: chargeback 단위(팀·프로젝트·비즈니스 유닛)
- AI 관련 리소스 식별: ServiceName이 Bedrock·OpenAI·Vertex AI·Anthropic을 포함하는 행

#### STEP 5. 태그 커버리지 산출물 저장
{tool:file_write}로 `out/step2/4-tag-coverage.md`를 저장함. 구성:
- 필수 4종 태그 커버리지 요약 표
- 미태깅 리소스 Top 20 목록(비용 순)
- AI 특화 태깅 준수 현황
- 개선 권고 사항

#### STEP 6. 태그 정책 YAML 생성
{tool:file_write}로 `resources/templates/tag-policy.yaml`을 생성함. 조직 프로파일 및 빌링 데이터 분석 결과를 반영하여 런타임 태그 정책을 정의함:
- 필수 태그 4종 정의 (키·허용값·형식 규칙)
- AI 특화 태그 3종 정의
- 위반 시 자동화 조치(알림·격리·비용 차단) 정의
- CSP별 태그 적용 방법 가이드

## 출력 형식

### out/step2/4-tag-coverage.md
```
# 태그 커버리지 분석 보고서

## 필수 4종 태그 커버리지 요약
| 태그 키 | 전체 리소스 | 태그 존재 | 커버리지% | 오태깅 수 |

## 미태깅 리소스 Top 20 (비용 순)
| 리소스 ID | CSP | 서비스 | 누락 태그 | 비용(KRW) |

## AI 특화 태깅 준수 현황
| AI 태그 키 | 존재 비율% | 미준수 리소스 수 |

## 개선 권고
```

### resources/templates/tag-policy.yaml
```yaml
version: "1.0.0"
required_tags:
  - key: "Project"
    allowed_values: []
    format: ""
    violation_action: ""
  ...
ai_tags:
  - key: "LLMApiKey"
    ...
```

## 검증

- 필수 4종 태그(Project·Environment·Owner·CostCenter) 각각의 커버리지 지표가 산출되었는지 확인
- 미태깅 리소스 목록에 비용(KRW) 기준 정렬이 적용되었는지 확인
- AI 특화 태그(LLMApiKey·ModelName·ChargebackUnit) 점검 결과가 포함되었는지 확인
- `resources/templates/tag-policy.yaml`이 필수 4종 + AI 3종 태그를 모두 정의하는지 확인
- 위반 시 조치(알림·격리·비용 차단)가 CSP별로 구체적으로 기술되었는지 확인
