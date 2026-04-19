---
name: help
description: finops 플러그인 사용 안내 (명령 목록 · 자동 라우팅)
type: utility
user-invocable: true
---

# Help

## 목표

finops 플러그인의 사용 가능한 명령, 자동 라우팅 키워드, 핵심 워크플로우를 호출 시에만 즉시 출력함.
런타임 상주 파일(CLAUDE.md)에 라우팅 테이블을 등록하는 대신, 이 스킬이 호출 시에만 토큰을 사용하여 사용자 발견성을 제공함.

## 활성화 조건

사용자가 `/finops:help` 호출 시 또는 "finops 도움말", "finops 뭘 할 수 있어" 키워드 감지 시.

## 명령어

| 명령 | 유형 | 설명 |
|------|------|------|
| `/finops:setup` | Setup | 플러그인 초기 설정 |
| `/finops:help` | Utility | 사용 안내 |
| `/finops:why-finops` | Orchestrator | WHY 정의 & 성숙도 진단 (STEP 1) |
| `/finops:inform` | Orchestrator | FOCUS 정규화 & 통합 가시성 (STEP 2) |
| `/finops:optimize` | Orchestrator | Right-sizing & 약정 전략 (STEP 3) |
| `/finops:operate` | Orchestrator | KPI·자동화·리뷰 런북 (STEP 4) |
| `/finops:review` | Orchestrator | 최종 독립 검증 (STEP 5) |
| `/finops:ppt-writer` | Orchestrator | PPT Deck 작성 + .pptx 빌드 (post-hoc) |
| `/finops:core` | Orchestrator | 풀 파이프라인 (why-finops → inform → optimize → operate → review) |

## 워크플로우

**중요: 추가적인 파일 탐색이나 에이전트 위임 없이, 아래 내용을 즉시 사용자에게 출력하세요.**

### 사용 가능한 명령

| 명령 | 유형 | 설명 |
|------|------|------|
| `/finops:setup` | Setup | 플러그인 초기 설정 |
| `/finops:help` | Utility | 사용 안내 |
| `/finops:why-finops` | Orchestrator | WHY 정의 & 성숙도 진단 (STEP 1) |
| `/finops:inform` | Orchestrator | FOCUS 정규화 & 통합 가시성 (STEP 2) |
| `/finops:optimize` | Orchestrator | Right-sizing & 약정 전략 (STEP 3) |
| `/finops:operate` | Orchestrator | KPI·자동화·리뷰 런북 (STEP 4) |
| `/finops:review` | Orchestrator | 최종 독립 검증 (STEP 5) |
| `/finops:ppt-writer` | Orchestrator | PPT Deck 작성 + .pptx 빌드 (post-hoc) |
| `/finops:core` | Orchestrator | 풀 파이프라인 (why-finops → inform → optimize → operate → review) |

### 자동 라우팅 키워드

| 키워드 | 라우팅 대상 |
|--------|-----------|
| `@why-finops`, "FinOps 왜" | why-finops |
| `@inform`, "FOCUS 정규화", "대시보드" | inform |
| `@optimize`, "Right-sizing", "약정" | optimize |
| `@operate`, "KPI", "리뷰 런북" | operate |
| `@review`, "최종 검증" | review |
| `@ppt-writer`, "PPT deck", "발표자료" | ppt-writer |
| `@core`, "FinOps 랩 전체" | core |

### 핵심 산출물

| 산출물 | 설명 |
|--------|------|
| `out/why-statement.md` | WHY 정의 문서 |
| `out/focus-normalized.csv` | FOCUS 정규화 데이터 |
| `out/dashboard.html` | 통합 가시성 대시보드 |
| `out/rightsize-plan.md` | Right-sizing 계획서 |
| `out/commit-strategy.md` | 약정 전략 문서 |
| `out/review-runbook.md` | 리뷰 런북 |
| `out/review-report.md` | 최종 검증 보고서 |
| `out/ppt-scripts/*.pptx` | PPT 발표 자료 |

### 참고

| 구분 | 경로 |
|------|------|
| 1차 교재 | `references/am/finops.md` §4.1~§4.16 |
| 2026 가이드 | `references/finops/state-of-finops-2026-lab-guide.md` |
| 샘플 데이터 | `resources/sample-billing/*.csv` |
| PPT 스타일 가이드 | `agents/ppt-writer/references/ppt-guide.md` |
