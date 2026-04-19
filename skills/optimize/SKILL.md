---
name: optimize
description: "줄이기 — 유휴 리소스 탐지, Right-sizing 3대안(CSP+AI), GPU 활용, 모델 다운그레이드, RI/SP/Spot 3시나리오"
type: orchestrator
user-invocable: true
---

# Optimize

[OPTIMIZE 활성화]

## 목표

유휴 리소스를 탐지하고 Right-sizing 3대안(Downsize-1·Downsize-2·Terminate)을 도출함. GPU 활용률·모델 다운그레이드 최적화를 포함하고, RI/SP/Spot Conservative·Base·Optimistic 3시나리오를 모델링하여 통합 최적화 권고를 산출함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@optimize` 멘션
- "Right-sizing", "약정" 키워드 포함
- `/finops:optimize` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트 | FQN | 티어 | 순서 |
|---|---|---|---|
| rightsize-advisor | `finops:rightsize-advisor:rightsize-advisor` | MEDIUM | 1 |
| commit-planner | `finops:commit-planner:commit-planner` | HIGH | 2 |

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
- `out/focus-normalized.csv` (inform 스킬 산출물)
- `resources/sample-billing/utilization-sample.csv`
- `resources/templates/ri-sp-decision-matrix.md`
- `references/am/finops.md` §4.8·§4.9·§4.10

파일 누락 시 사용자에게 알리고 중단함. `out/focus-normalized.csv` 미존재 시 `/finops:inform` 먼저 실행 권장.

### Phase 2: Right-sizing & AI 최적화 → Agent: rightsize-advisor (`/oh-my-claudecode:ralph` 활용)

- **TASK**: Step 3-1~3-3 실행 — 유휴 리소스 탐지 + Right-sizing 3대안 + GPU 활용 최적화 + 모델 다운그레이드 분석
- **EXPECTED OUTCOME**:
  - `out/step3/1-idle-resources.md` — 유휴 리소스 6종 이상 목록 (리소스ID·CSP·서비스·CPU평균·Memory평균·판정 근거)
  - `out/step3/3-scaling-policy-checklist.md` — 스케일링 정책 체크리스트 (CPU·Memory 임계값·자동화 조건)
  - `out/rightsize-plan.md` — Right-sizing 통합 계획서 (Downsize-1·Downsize-2·Terminate 3대안 각 절감액·SLA 리스크·구현 복잡도)
  - 모델 다운그레이드 대안 3종 (품질 리스크·비용 절감률 포함)
- **MUST DO**:
  - CPU 40% 미만·Memory 60% 미만 2주 지속 기준으로 유휴 판정
  - GPU 활용률 60% 미만 리소스 식별
  - 모델 다운그레이드 대안 3종 도출 시 각각 품질 리스크 수준(낮음·중간·높음) 명시
  - Downsize-1·Downsize-2·Terminate 3대안 각각 절감액 수치화
- **MUST NOT DO**:
  - 1주 단일 측정치 기반 유휴 판정 금지 (2주 이상 지속 기준 필수)
  - 절감액 수치 없는 권고 생성 금지
  - 스케일링 자동화 실행 수행 금지
- **CONTEXT**:
  - `out/focus-normalized.csv`
  - `resources/sample-billing/utilization-sample.csv`
  - `references/am/finops.md` §4.8·§4.9·§4.10

### Phase 3: 약정 3시나리오 → Agent: commit-planner (`/oh-my-claudecode:ralph` 활용)

- **TASK**: Step 3-4 실행 — 상시/변동/배치/예측불가 4범주 워크로드 분류, RI/SP/Spot Conservative·Base·Optimistic 3시나리오 모델링
- **EXPECTED OUTCOME**:
  - `out/commit-strategy.md` — 워크로드 분류 표 + 3시나리오 비교 표 (절감액·BEP·리스크·유연성 트레이드오프 포함)
  - Conservative: RI 40%·SP 10%·On-Demand 50%
  - Base: RI 50%·SP 20%·Spot 10%·On-Demand 20%
  - Optimistic: RI 60%·SP 25%·Spot 15%
  - 각 시나리오별 BEP 월수 및 1개월 샘플 데이터 한계 경고 명시
- **MUST DO**:
  - `resources/templates/ri-sp-decision-matrix.md` 의사결정 매트릭스 적용
  - 1개월 샘플 데이터 한계 명시 (3~6개월 데이터 수집 후 재검토 권고 포함)
  - 각 시나리오 BEP 계산식 명시
  - 워크로드 분류 CV 계수 기준 명시
- **MUST NOT DO**:
  - 샘플 기반 과신 표현 금지 ("확실히 N% 절감" 등 단정 표현 금지)
  - 1개월 샘플만으로 최종 약정 결정 권고 금지
  - 데이터 정규화·PPT 제작 수행 금지
- **CONTEXT**:
  - `out/focus-normalized.csv`
  - `resources/templates/ri-sp-decision-matrix.md`
  - `references/am/finops.md` §4.9·§4.10

### Phase 4: 통합 권고 보고 (`/oh-my-claudecode:verify` 활용)

다음 항목을 순서대로 검증함:
- [ ] `out/step3/1-idle-resources.md` 유휴 리소스 6종 이상 목록 확인
- [ ] `out/rightsize-plan.md` Downsize-1·Downsize-2·Terminate 3대안 모두 존재 확인
- [ ] `out/commit-strategy.md` Conservative·Base·Optimistic 3시나리오 수치 일관성 확인
- [ ] 모델 다운그레이드 대안 3종 확인
- [ ] BEP 수치가 각 시나리오에 명시되었는지 확인

검증 통과 후 핵심 결과를 통합 보고하고, 다음 단계로 `/finops:operate` 실행 권장.

## 완료 조건

- [ ] 유휴 리소스 6종 이상 목록 산출
- [ ] Right-sizing Downsize-1·Downsize-2·Terminate 3대안 모두 존재
- [ ] `out/commit-strategy.md` Conservative·Base·Optimistic 3시나리오 수치 일관성 검증 통과
- [ ] 1개월 샘플 한계 경고 문구 포함

## 검증 프로토콜

1. rightsize-advisor·commit-planner 각 AGENT.md 검증 섹션 통과
2. Phase 4 파일 존재 확인: `out/step3/1-idle-resources.md`, `out/rightsize-plan.md`, `out/commit-strategy.md`
3. `out/step3/1-idle-resources.md` 내 유휴 리소스 행 6건 이상 확인
4. `out/commit-strategy.md` 내 3시나리오 절감액·BEP 수치 형식 검증

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/step3/` 및 `out/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료.

## 재개

마지막 완료 Phase 번호를 확인하고 해당 Phase 다음부터 재개함. 다음 파일 존재 여부로 완료 Phase를 판단함:
- Phase 2 완료: `out/rightsize-plan.md`
- Phase 3 완료: `out/commit-strategy.md`

## 출력 형식

### 사용자 보고 형식 (권장)

```
## Optimize 결과 요약

### 유휴 리소스 탐지
- 총 N건 (CSP: N건, AI/GPU: N건)
- 즉시 조치 가능 Terminate 대상: N건

### Right-sizing 절감 예상
| 대안 | 절감액(KRW/월) | SLA 리스크 |
|---|---|---|
| Downsize-1 | | |
| Downsize-2 | | |
| Terminate | | |

### 약정 시나리오 비교
| 시나리오 | 절감액(KRW/년) | BEP(월) | 리스크 |
|---|---|---|---|
| Conservative | | | |
| Base | | | |
| Optimistic | | | |

※ 1개월 샘플 기반 추정치 — 3~6개월 데이터 수집 후 재검토 권고

### 다음 단계
→ `/finops:operate` 으로 FinOps 운영 체계화 및 자동화를 시작하세요.
```
