---
name: operate
description: "체계화 — 단위경제 KPI 6종, 자동화 5단계, 게이트 6종, 주/월/분기 리뷰 런북, Crawl→Walk 12개월 전환"
type: orchestrator
user-invocable: true
---

# Operate

[OPERATE 활성화]

## 목표

FinOps 운영 체계를 수립함. 단위경제 KPI 6종(CSP 3종 + AI 3종), 자동화 파이프라인 5단계, 게이트 기준 6종, 주/월/분기 리뷰 런북, Crawl→Walk 12개월 전환 플랜을 산출하여 지속 가능한 클라우드 비용 최적화 운영 기반을 구성함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@operate` 멘션
- "KPI", "리뷰 런북" 키워드 포함
- `/finops:operate` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트 | FQN | 티어 |
|---|---|---|
| finops-practitioner | `finops:finops-practitioner:finops-practitioner` | MEDIUM |

### 프롬프트 조립
- `{DMAP_PLUGIN_DIR}/resources/guides/combine-prompt.md`에 따라 AGENT.md + agentcard.yaml + tools.yaml 합치기
- `Agent(subagent_type=FQN, model=tier_mapping 결과, prompt=조립된 프롬프트)` 호출
- tier → 모델 매핑은 `gateway/runtime-mapping.yaml` 참조

### 서브 에이전트 호출
워크플로우 단계에 `Agent: {agent-name}`이 명시된 경우,
메인 에이전트는 해당 단계를 직접 수행하지 않고,
반드시 위 프롬프트 조립 규칙에 따라 해당 에이전트를 호출하여 결과를 받아야 함.

서브에이전트 호출 없이 메인 에이전트가 해당 산출물을 직접 작성하면
스킬 미준수로 간주함.

### 호출

```
Agent(
  subagent_type="finops:finops-practitioner:finops-practitioner",
  model=MEDIUM 티어 모델,
  prompt=조립된 프롬프트
)
```

## 워크플로우

### Phase 1: 입력 확인 (`ulw` 활용)

다음 파일 존재 여부를 확인함:
- `out/focus-normalized.csv`
- `out/rightsize-plan.md`
- `out/commit-strategy.md`
- `resources/rulebook/gate-criteria.yaml`
- `resources/templates/monthly-review-agenda.md`
- `references/am/finops.md` §4.11~§4.13
- `references/finops/state-of-finops-2026-lab-guide.md` §4·§8

파일 누락 시 사용자에게 알리고 중단함. 선행 스킬(`/finops:optimize`)을 먼저 실행할 것을 안내함.

### Phase 2: KPI·자동화·런북·전환 → Agent: finops-practitioner (`/oh-my-claudecode:ralph` 활용)

→ Agent: finops-practitioner

- **TASK**: Step 4-1~4-4 실행 — 단위경제 KPI 6종(CSP 3종 + AI 3종), 자동화 파이프라인 5단계, 주/월/분기 리뷰 런북, Crawl→Walk 12개월 전환 플랜 산출물 생성함
- **EXPECTED OUTCOME**:
  - `resources/templates/kpi-dashboard.md` — KPI 대시보드 템플릿 (6종 KPI 정의·계산식·목표치)
  - `out/step4/1-unit-economics.md` — 단위경제 KPI 6종 분석 (CSP: 태깅률·RI활용률·이상탐지 응답, AI: GPU활용률·AI 비용/토큰·모델 효율)
  - `out/step4/2-automation-pipeline.md` — 자동화 파이프라인 5단계 설계 (데이터수집→정규화→분석→알림→액션)
  - `out/review-runbook.md` — 주간/월간/분기 리뷰 런북 (게이트 기준 6종·에스컬레이션 절차 포함)
  - `out/step4/4-maturity-transition.md` — Crawl→Walk 12개월 전환 플랜 (분기별 마일스톤·책임 Ownership·성공 지표)
- **MUST DO**:
  - 게이트 기준 6종(태깅≥95%·MAPE≤10%·RI≥80%·이상탐지≤24h·유휴≤3%·GPU≥60%)을 리뷰 런북에 삽입
  - HBT 사업 포트폴리오(MNO·MVNO·IoT·B2B) 맞춤 KPI 지표 반영
  - 각 게이트 미충족 시 책임 에이전트 및 에스컬레이션 절차 명시
  - Ownership별(재무·엔지니어링·경영진) KPI 연결 관계 기술
- **MUST NOT DO**:
  - 게이트 미충족 시 에스컬레이션 절차 누락 금지
  - 게이트 기준 수치 임의 변경 금지 (gate-criteria.yaml 기준 준수)
  - 데이터 시각화 코드·PPT 작성 수행 금지
- **CONTEXT**:
  - `out/focus-normalized.csv`
  - `out/rightsize-plan.md`
  - `out/commit-strategy.md`
  - `resources/rulebook/gate-criteria.yaml`
  - `resources/templates/monthly-review-agenda.md`
  - `references/am/finops.md` §4.11~§4.13
  - `references/finops/state-of-finops-2026-lab-guide.md` §4·§8

### Phase 3: 게이트 기준 검증 (`/oh-my-claudecode:ulw` 활용)

다음 항목을 순서대로 검증함:
- [ ] 게이트 기준 6종(태깅≥95%·MAPE≤10%·RI≥80%·이상탐지≤24h·유휴≤3%·GPU≥60%)이 `out/review-runbook.md`에 모두 삽입되었는지 확인
- [ ] 각 게이트 미달 시 책임 에이전트·에스컬레이션 절차가 명시되었는지 확인
- [ ] 주간·월간·분기별 리뷰 사이클이 런북에 구분되어 기술되었는지 확인
- [ ] Ownership별 KPI 연결이 `out/step4/1-unit-economics.md`에 기술되었는지 확인

검증 미달 항목 발견 시 Phase 2 에이전트를 재호출하여 보완 지시함.

### Phase 4: 리뷰 런북 확정 및 보고 (`/oh-my-claudecode:verify` 활용)

다음 항목을 최종 확인함:
- [ ] 산출물 5종 존재 (`kpi-dashboard.md`, `1-unit-economics.md`, `2-automation-pipeline.md`, `review-runbook.md`, `4-maturity-transition.md`)
- [ ] KPI 6종 완비 확인 (CSP 3종 + AI 3종)
- [ ] 자동화 5단계 완비 확인
- [ ] 게이트 6종 완비 확인
- [ ] Phase 3종(Crawl/Walk/Run) 전환 로드맵 완비 확인

완료 시 다음 단계로 `/finops:review` 실행 권장 안내함.

## 완료 조건

- [ ] 5개 산출물 파일 존재 (`resources/templates/kpi-dashboard.md`, `out/step4/1-unit-economics.md`, `out/step4/2-automation-pipeline.md`, `out/review-runbook.md`, `out/step4/4-maturity-transition.md`)
- [ ] KPI 6종(CSP 3종 + AI 3종) 역참조 가능
- [ ] 게이트 기준 6종 리뷰 런북 내 삽입 확인
- [ ] Ownership별 KPI 연결 확인

## 검증 프로토콜

1. finops-practitioner AGENT.md의 검증 섹션 체크박스 전항목 통과
2. Phase 4 파일 존재 확인 — 5개 파일 모두 0바이트 초과
3. `out/review-runbook.md`에서 게이트 수치(95%, 10%, 80%, 24h, 3%, 60%) 6개 모두 포함 여부 정규표현식으로 스캔
4. Ownership 키워드(재무·엔지니어링·경영진) `out/step4/1-unit-economics.md` 내 존재 확인

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/step4/` 및 `out/`, `resources/templates/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료.

## 재개

마지막 완료 Phase 번호를 확인하고 해당 Phase 다음부터 재개함. `out/step4/` 디렉터리의 파일 존재 여부로 완료 Phase를 판단함.

## 출력 형식

### 사용자 보고 형식 (권장)

```
## Operate 운영 체계 수립 결과 요약

### KPI 대시보드 (6종)
| 구분 | KPI | 목표치 |
|---|---|---|
| CSP | 태깅률 | ≥95% |
| CSP | RI 활용률 | ≥80% |
| CSP | 이상탐지 응답 | ≤24h |
| AI | GPU 활용률 | ≥60% |
| AI | AI 비용/토큰 | ... |
| AI | 모델 효율 | ... |

### 게이트 기준 충족 현황
- 태깅≥95%: [확인/미달]
- MAPE≤10%: [확인/미달]
- RI≥80%: [확인/미달]
- 이상탐지≤24h: [확인/미달]
- 유휴≤3%: [확인/미달]
- GPU≥60%: [확인/미달]

### 다음 단계
→ `/finops:review` 로 최종 독립 검증을 수행하세요.
```
