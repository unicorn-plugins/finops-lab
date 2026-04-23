---
name: review
description: "최종 독립 검증 — 4단계 정합성, FOCUS 커버리지, COVERS·게이트 규칙 ID 역참조, 3시나리오 수치 일관성, Ownership 전환 실행 가능성"
type: orchestrator
user-invocable: true
---

# Review

[REVIEW 활성화]

## 목표

4단계 파이프라인(WHY→Inform→Optimize→Operate) 전체 산출물에 대해 독립 검증을 수행함. FOCUS Mandatory 15종 + AI 확장 5종 커버리지, COVERS·게이트 규칙 ID 역참조, 3시나리오 수치 일관성, Ownership별 전환 실행 가능성을 객관적으로 감사하여 최종 APPROVED/REJECTED 판정을 산출함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@review` 멘션
- "최종 검증", "정합성 감사" 키워드 포함
- `/finops:review` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트 | FQN | 티어 |
|---|---|---|
| reviewer | `finops:reviewer:reviewer` | HIGH |

### 프롬프트 조립
- `resources/guides/combine-prompt.md`에 따라 AGENT.md + agentcard.yaml + tools.yaml 합치기
- `Agent(subagent_type=FQN, model=tier_mapping 결과, prompt=조립된 프롬프트)` 호출
- tier → 모델 매핑은 `gateway/runtime-mapping.yaml` 참조

### 서브 에이전트 호출
워크플로우 단계에 `Agent: {agent-name}`이 명시된 경우,
메인 에이전트는 해당 단계를 직접 수행하지 않고,
반드시 위 프롬프트 조립 규칙에 따라 해당 에이전트를 호출하여 결과를 받아야 함.

서브에이전트 호출 없이 메인 에이전트가 해당 산출물을 직접 작성하면
스킬 미준수로 간주함.

## 워크플로우

### Phase 1: 전체 산출물 로드 (`ulw` 활용)

다음 파일 존재 여부를 확인함:

**핵심 산출물**:
- `out/why-statement.md`
- `out/focus-normalized.csv`
- `out/dashboard.html`
- `out/rightsize-plan.md`
- `out/commit-strategy.md`
- `out/review-runbook.md`
- `out/step1/` (1-drivers.md · 2-maturity-diagnosis.md · 3-covers-roadmap.md)
- `out/step2/` (FOCUS 정규화 관련 산출물)
- `out/step3/` (Right-sizing · 약정 관련 산출물)
- `out/step4/` (1-unit-economics.md · 2-automation-pipeline.md · 4-maturity-transition.md)

**규칙 파일**:
- `resources/rulebook/covers-principles.yaml`
- `resources/rulebook/gate-criteria.yaml`
- `resources/rulebook/focus-v1.yaml` (또는 동등 파일)

파일 누락 시 사용자에게 누락 목록을 안내하고, 해당 단계의 스킬(`/finops:why-finops`, `/finops:inform`, `/finops:optimize`, `/finops:operate`) 선행 실행을 권장함.

### Phase 2: 독립 검증 → Agent: reviewer (`/oh-my-claudecode:ralph` 활용)

→ Agent: reviewer

- **TASK**: 4단계(WHY→Inform→Optimize→Operate) 정합성 감사 및 체크리스트 전항목 검증 수행. 독립 컨텍스트에서 원본 산출물을 수정 없이 객관 평가하여 APPROVED 또는 REJECTED 판정 산출
- **EXPECTED OUTCOME**:
  - `out/review-report.md` — 최종 검증 보고서
    - 판정: APPROVED 또는 REJECTED (사유 포함)
    - 4단계 정합성 체크리스트 (WHY→Inform→Optimize→Operate 연결 추적)
    - FOCUS Mandatory 15종 + AI 확장 5종 커버리지 매트릭스
    - COVERS 규칙 ID 역참조 목록 (규칙 ID → 산출물 위치)
    - 게이트 기준 6종 역참조 목록 (기준 ID → 런북 위치)
    - 3시나리오 수치 일관성 검증 결과 (시나리오별 절감 수치 교차 확인)
    - Ownership별 전환 실행 가능성 평가 (재무·엔지니어링·경영진)
    - 체크리스트 정량 통과율 (예: 38/40 항목 통과)
- **MUST DO**:
  - 독립 컨텍스트에서 객관 검증 수행 (이전 단계 산출물 작성자와 분리된 관점 유지)
  - 모든 검증 결과를 규칙 ID(COVERS-*-##, GATE-##)로 역추적 가능하게 기술
  - APPROVED 시 통과 근거 명시, REJECTED 시 수정 필요 항목·책임 에이전트·재실행 스킬 명시
  - 체크리스트 정량 통과율(분모/분자) 명시
- **MUST NOT DO**:
  - 원본 산출물 수정 금지
  - 분석 본인이 만든 산출물에 대한 자기 검증 금지
  - 검증 기준 임의 완화 금지 (gate-criteria.yaml·covers-principles.yaml 기준 준수)
  - 수치 미일치 항목을 "허용 오차" 처리하여 통과 처리 금지
- **CONTEXT**:
  - `out/` 하위 전체 산출물 (위 Phase 1 목록)
  - `resources/rulebook/covers-principles.yaml`
  - `resources/rulebook/gate-criteria.yaml`
  - `resources/rulebook/focus-v1.yaml`

### Phase 3: 승인/반려 사용자 안내 (`/oh-my-claudecode:verify` 활용)

`out/review-report.md` 내 판정(APPROVED/REJECTED) 확인 후 다음 안내를 수행함:

**APPROVED 시**:
- [ ] `out/review-report.md` 존재 및 "APPROVED" 문자열 포함 확인
- [ ] 체크리스트 정량 통과율 사용자에게 출력
- 다음 단계로 `/finops:ppt-writer` 실행 권장

**REJECTED 시**:
- [ ] `out/review-report.md` 존재 및 "REJECTED" 문자열 포함 확인
- [ ] 수정 필요 항목 목록과 책임 에이전트 사용자에게 안내
- [ ] 각 항목별 재실행 스킬 명시 (예: 항목 X → `/finops:optimize` 재실행)

## 완료 조건

- [ ] `out/review-report.md` 존재
- [ ] 판정(APPROVED 또는 REJECTED) 명시
- [ ] 체크리스트 정량 통과율(분모/분자) 포함
- [ ] COVERS·게이트 규칙 ID 역참조 목록 포함

## 검증 프로토콜

1. reviewer AGENT.md의 검증 섹션 체크박스 전항목 통과
2. `out/review-report.md` 파일 존재 확인 — 0바이트 초과
3. "APPROVED" 또는 "REJECTED" 문자열 정규표현식으로 스캔
4. COVERS-*-## 패턴 역참조 항목 수 확인 (최소 6건)
5. 체크리스트 통과율 수치(N/M 형식) 존재 확인

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/review-report.md` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료.

## 재개

`out/review-report.md` 존재 여부로 완료 Phase를 판단함. 파일 미존재 시 Phase 1부터 재시작, 존재 시 Phase 3(사용자 안내)부터 재개함.

## 출력 형식

### 사용자 보고 형식 (권장)

```
## Review 최종 검증 결과

### 판정
**[APPROVED | REJECTED]**

### 체크리스트 통과율
- 전체: N/M 항목 통과 (통과율 X%)
- 4단계 정합성: N/4 통과
- FOCUS 커버리지: N/20 통과 (Mandatory 15종 + AI 확장 5종)
- COVERS 역참조: N건 확인
- 게이트 기준: N/6 통과
- 시나리오 수치 일관성: [일치/불일치]
- Ownership 전환 가능성: [가능/보완 필요]

### [APPROVED 시] 다음 단계
→ `/finops:ppt-writer` 로 발표 자료를 작성하세요.

### [REJECTED 시] 수정 필요 항목
| # | 항목 | 책임 에이전트 | 재실행 스킬 |
|---|---|---|---|
| 1 | ... | ... | /finops:... |
```
