---
name: core
description: "finops 풀 파이프라인 — @why-finops → @inform → @optimize → @operate → @review 순차 실행 (ppt-writer는 post-hoc로 별도 호출)"
type: orchestrator
user-invocable: true
---

# Core

[CORE 활성화]

## 목표

FinOps 랩 전체 파이프라인을 순차 실행함. WHY 정의부터 Inform·Optimize·Operate·Review까지 5단계 스킬을 Skill→Skill 위임으로 자동 연결하여 최종 APPROVED 판정까지 도달함. PPT 발표자료 제작은 post-hoc 별도 호출(`/finops:ppt-writer`)로 처리함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@core` 멘션
- "FinOps 랩 전체", "처음부터 끝까지" 키워드 포함
- `/finops:core` 직접 호출

## 에이전트 호출 규칙

**Agent 위임 없음. Skill→Skill 위임만으로 구성됨.**

### Skill 위임 목록

| 순서 | 스킬 FQN | 역할 |
|---|---|---|
| 1 | `finops:why-finops` | WHY 정의 & 성숙도 진단 |
| 2 | `finops:inform` | FOCUS 정규화 + 대시보드 생성 |
| 3 | `finops:optimize` | Right-sizing + 약정 전략 |
| 4 | `finops:operate` | KPI·자동화·리뷰 런북 |
| 5 | `finops:review` | 최종 독립 검증 |

## 워크플로우

### Phase 1: WHY → Skill: finops:why-finops

→ Skill: finops:why-finops

- **INTENT**: WHY 정의 & 성숙도 진단 수행. 비즈니스 이슈를 FinOps 3대 가치에 매핑하고, Ownership×Capability 성숙도 진단과 12개월 스킬셋 로드맵을 산출함
- **ARGS**: `{"source_plugin": "finops:core"}`
- **RETURN**: `out/why-statement.md` + `out/step1/` (1-drivers.md · 2-maturity-diagnosis.md · 3-covers-roadmap.md) 존재

Phase 완료 후 기대 산출물 파일 존재 여부를 확인함. 실패 시 Phase 1만 재실행 옵션을 사용자에게 제공함.

### Phase 2: Inform → Skill: finops:inform

→ Skill: finops:inform

- **INTENT**: FOCUS 정규화 + 통합 가시성 대시보드 생성. 클라우드 비용 데이터를 FOCUS 표준으로 정규화하고 HTML 대시보드를 산출함
- **ARGS**: `{"source_plugin": "finops:core"}`
- **RETURN**: `out/focus-normalized.csv` + `out/dashboard.html` 존재

Phase 완료 후 기대 산출물 파일 존재 여부를 확인함. 실패 시 Phase 2만 재실행 옵션을 사용자에게 제공함.

### Phase 3: Optimize → Skill: finops:optimize

→ Skill: finops:optimize

- **INTENT**: Right-sizing 분석 + 약정(RI/SP) 전략 수립. 이상 탐지·유휴 자원 식별·약정 시나리오 3종을 산출함
- **ARGS**: `{"source_plugin": "finops:core"}`
- **RETURN**: `out/rightsize-plan.md` + `out/commit-strategy.md` 존재

Phase 완료 후 기대 산출물 파일 존재 여부를 확인함. 실패 시 Phase 3만 재실행 옵션을 사용자에게 제공함.

### Phase 4: Operate → Skill: finops:operate

→ Skill: finops:operate

- **INTENT**: 단위경제 KPI 6종·자동화 파이프라인 5단계·게이트 기준 6종·리뷰 런북·12개월 전환 플랜 수립
- **ARGS**: `{"source_plugin": "finops:core"}`
- **RETURN**: `out/review-runbook.md` + `out/step4/` (1-unit-economics.md · 2-automation-pipeline.md · 4-maturity-transition.md) 존재

Phase 완료 후 기대 산출물 파일 존재 여부를 확인함. 실패 시 Phase 4만 재실행 옵션을 사용자에게 제공함.

### Phase 5: Review → Skill: finops:review

→ Skill: finops:review

- **INTENT**: 4단계 전체 산출물에 대한 최종 독립 검증 수행. FOCUS 커버리지·COVERS·게이트 규칙 ID 역참조·3시나리오 수치 일관성·Ownership 전환 실행 가능성 감사
- **ARGS**: `{"source_plugin": "finops:core"}`
- **RETURN**: `out/review-report.md` 존재 + 판정 APPROVED

Phase 완료 후 `out/review-report.md` 내 "APPROVED" 또는 "REJECTED" 판정 확인함.
- APPROVED 시: 전체 산출물 디렉토리 안내 + `/finops:ppt-writer` 권장 안내
- REJECTED 시: 검토 필요 항목 목록 안내 + 해당 Phase 재실행 옵션 제공

## 완료 조건

- [ ] 5개 Skill 순차 성공 (각 Phase 기대 산출물 존재 확인)
- [ ] `out/review-report.md` 판정 APPROVED
- [ ] 전체 산출물 디렉토리 사용자 안내 완료
- [ ] `/finops:ppt-writer` 권장 안내 완료 (post-hoc)

## 검증 프로토콜

각 Phase 종료 시 기대 산출물 파일 존재 여부를 확인함:

| Phase | 확인 파일 | 실패 시 조치 |
|---|---|---|
| Phase 1 | `out/why-statement.md`, `out/step1/*.md` (3종) | Phase 1만 재실행 |
| Phase 2 | `out/focus-normalized.csv`, `out/dashboard.html` | Phase 2만 재실행 |
| Phase 3 | `out/rightsize-plan.md`, `out/commit-strategy.md` | Phase 3만 재실행 |
| Phase 4 | `out/review-runbook.md`, `out/step4/*.md` (3종) | Phase 4만 재실행 |
| Phase 5 | `out/review-report.md` + 판정 APPROVED | Phase 5만 재실행 |

## 상태 정리

임시 상태 파일 미사용. 각 Phase 산출물은 `out/`, `out/step1/`, `out/step2/`, `out/step3/`, `out/step4/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 실행 중인 Phase의 스킬을 중단하고 전체 파이프라인을 종료함. 이미 완료된 Phase 산출물은 보존됨.

## 재개

각 Phase의 기대 산출물 파일 존재 여부로 완료 Phase를 판단하고, 미완료 Phase부터 재개함:
1. `out/why-statement.md` 미존재 → Phase 1부터 재시작
2. `out/focus-normalized.csv` 미존재 → Phase 2부터 재개
3. `out/rightsize-plan.md` 미존재 → Phase 3부터 재개
4. `out/review-runbook.md` 미존재 → Phase 4부터 재개
5. `out/review-report.md` 미존재 또는 판정 REJECTED → Phase 5부터 재개

## 출력 형식

### 사용자 보고 형식 (권장)

```
## FinOps 풀 파이프라인 실행 결과

### Phase 완료 현황
| Phase | 스킬 | 상태 | 주요 산출물 |
|---|---|---|---|
| Phase 1 | finops:why-finops | [완료/실패] | out/why-statement.md |
| Phase 2 | finops:inform | [완료/실패] | out/focus-normalized.csv, out/dashboard.html |
| Phase 3 | finops:optimize | [완료/실패] | out/rightsize-plan.md, out/commit-strategy.md |
| Phase 4 | finops:operate | [완료/실패] | out/review-runbook.md, out/step4/*.md |
| Phase 5 | finops:review | [완료/실패] | out/review-report.md |

### 최종 판정
**[APPROVED | REJECTED]**

### 전체 산출물 경로
- out/why-statement.md
- out/focus-normalized.csv
- out/dashboard.html
- out/rightsize-plan.md
- out/commit-strategy.md
- out/review-runbook.md
- out/step4/1-unit-economics.md
- out/step4/2-automation-pipeline.md
- out/step4/4-maturity-transition.md
- out/review-report.md

### 다음 단계 (post-hoc)
→ `/finops:ppt-writer` 로 발표 자료를 제작하세요.
```
