---
name: why-finops
description: "WHY 정의 & 성숙도 진단 — 비즈니스 이슈를 FinOps 3대 가치에 매핑, Ownership×Capability 진단, COVERS 정렬, 12개월 스킬셋 로드맵 수립"
type: orchestrator
user-invocable: true
---

# WHY-FinOps

[WHY_FINOPS 활성화]

## 목표

조직의 FinOps 도입 필요성(WHY)을 전략적으로 정의함. 비즈니스 이슈를 FinOps 3대 가치에 매핑하고, Ownership×Capability 성숙도를 진단하며, COVERS 원칙에 정렬된 12개월 스킬셋 로드맵과 경영진 WHY 1-Pager를 산출함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@why-finops` 멘션
- "FinOps 왜", "성숙도 진단" 키워드 포함
- `/finops:why-finops` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트 | FQN | 티어 |
|---|---|---|
| strategy-director | `finops:strategy-director:strategy-director` | HIGH |

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

### Phase 1: 입력 확인 (`ulw` 활용)

다음 파일 존재 여부를 확인함:
- `resources/basic-info/company-profile.md`
- `references/am/finops.md` §4.1~§4.4·§4.14~§4.16
- `references/finops/state-of-finops-2026-lab-guide.md` §1~3
- `resources/rulebook/covers-principles.yaml`

파일 누락 시 사용자에게 알리고 중단함.

### Phase 2: WHY·성숙도·COVERS·로드맵 → Agent: strategy-director (`/oh-my-claudecode:ralph` 활용)

- **TASK**: maturity-assessor·driver-mapper 2개 sub_role 워크플로우를 수행하여 Step 1-1~1-4 산출물 생성함
- **EXPECTED OUTCOME**:
  - `out/step1/1-drivers.md` — 비즈니스 이슈 목록 + FinOps 3대 가치 매핑 표
  - `out/step1/2-maturity-diagnosis.md` — Ownership 현황 표 + Capability 수준 매트릭스 + 우선순위 갭 목록
  - `out/step1/3-covers-roadmap.md` — COVERS 원칙 정렬 12개월 분기별 스킬셋 로드맵
  - `out/why-statement.md` — 경영진 대상 WHY 1-Pager (배경·문제·목표·기대효과·실행 로드맵 요약)
  - COVERS 규칙 ID(COVERS-*-##) 역참조 가능, Ownership별 Capability 최하위 1개씩 특정, 12개월 OKR 초안 포함
- **MUST DO**:
  - HBT 회사 프로파일(`resources/basic-info/company-profile.md`) 반영
  - State of FinOps 2026 Top 스킬셋 반영
  - COVERS 규칙 ID를 모든 권고에 명시
  - Ownership별(재무·엔지니어링·경영진) Capability 최하위 항목 1개씩 특정
- **MUST NOT DO**:
  - 규칙 ID 없는 권고 생성 금지
  - "전사 평균" 수치만으로 결론 도출 금지 (Ownership별 세분화 필수)
  - 데이터 정규화·코드 작성·PPT 제작 수행 금지
- **CONTEXT**:
  - `resources/basic-info/company-profile.md`
  - `references/am/finops.md` §4.1~§4.4·§4.14~§4.16
  - `references/finops/state-of-finops-2026-lab-guide.md` §1~3
  - `resources/rulebook/covers-principles.yaml`

### Phase 3: 산출물 정합성 검증 (`/oh-my-claudecode:verify` 활용)

다음 항목을 순서대로 검증함:
- [ ] 4개 산출물 파일 존재 확인 (`out/step1/1-drivers.md`, `2-maturity-diagnosis.md`, `3-covers-roadmap.md`, `out/why-statement.md`)
- [ ] 각 산출물에 COVERS 규칙 ID(COVERS-*-##) 형식 인용 존재 여부 확인
- [ ] `out/why-statement.md`가 1-1~1-3 내용(드라이버·성숙도·로드맵)을 모두 아우르는지 확인
- [ ] Ownership별 Capability 최하위 항목이 1개씩 명시되었는지 확인

### Phase 4: 사용자 보고 (`ulw` 활용)

핵심 결과를 요약하여 보고함:
- Ownership별 Walk 전환 집중 역량 3~6개 목록
- COVERS 규칙 인용 건수 요약
- 12개월 OKR 초안 주요 목표
- 다음 단계로 `/finops:inform` 실행 권장

## 완료 조건

- [ ] 4개 산출물 파일 존재 (`out/step1/1-drivers.md`, `out/step1/2-maturity-diagnosis.md`, `out/step1/3-covers-roadmap.md`, `out/why-statement.md`)
- [ ] COVERS 규칙 ID 최소 6개 이상 인용됨
- [ ] Ownership별(재무·엔지니어링·경영진) Capability 진단 완료
- [ ] 12개월 스킬셋 로드맵 분기별 구성 완료

## 검증 프로토콜

1. strategy-director AGENT.md의 검증 섹션 체크박스 전항목 통과
2. Phase 3 파일 존재 확인 — 4개 파일 모두 0바이트 초과
3. COVERS-*-## 패턴 정규표현식으로 각 파일 스캔, 총 6건 이상 확인

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/step1/` 및 `out/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료.

## 재개

마지막 완료 Phase 번호를 확인하고 해당 Phase 다음부터 재개함. `out/step1/` 디렉터리의 파일 존재 여부로 완료 Phase를 판단함.

## 출력 형식

### 사용자 보고 형식 (권장)

```
## WHY-FinOps 진단 결과 요약

### Ownership별 집중 역량
| Ownership | Walk 전환 집중 역량 |
|---|---|
| 재무 | ... |
| 엔지니어링 | ... |
| 경영진 | ... |

### COVERS 규칙 인용 현황
- 총 인용 건수: N건 (기준: 6건 이상)

### 12개월 OKR 주요 목표
- Q1: ...
- Q2: ...

### 다음 단계
→ `/finops:inform` 으로 FOCUS 정규화 및 통합 가시성 구축을 시작하세요.
```
