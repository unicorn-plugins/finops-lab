---
name: help
description: finops 플러그인 사용 안내 (명령 목록 · 자동 라우팅)
type: utility
user-invocable: true
---

# Help

[HELP 활성화]

## 목표

finops 플러그인의 사용 가능한 명령, 자동 라우팅 키워드, 핵심 워크플로우를 호출 시에만 즉시 출력함.
런타임 상주 파일(AGENTS.md)에 라우팅 테이블을 등록하는 대신, 이 스킬이 호출 시에만 토큰을 사용하여 사용자 발견성을 제공함.

## 활성화 조건

사용자가 `/finops:help` 호출 시 또는 "finops 도움말", "finops 뭘 할 수 있어" 키워드 감지 시.

## 사용 안내

**중요: 추가적인 파일 탐색이나 에이전트 위임 없이, 아래 내용을 즉시 사용자에게 출력하세요.**

### 명령어

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

`@{skill-name}`으로 Skill 직접 호출 가능

### 자동 라우팅 (키워드 감지)

| 키워드 | 라우팅 대상 |
|--------|-----------|
| `@why-finops`, "FinOps 왜" | `/finops:why-finops` |
| `@inform`, "FOCUS 정규화", "대시보드" | `/finops:inform` |
| `@optimize`, "Right-sizing", "약정" | `/finops:optimize` |
| `@operate`, "KPI", "리뷰 런북" | `/finops:operate` |
| `@review`, "최종 검증" | `/finops:review` |
| `@ppt-writer`, "PPT deck", "발표자료" | `/finops:ppt-writer` |
| `@core`, "FinOps 랩 전체" | `/finops:core` |

### Quick Guide

1. **최초 1회**: `/finops:setup` — 모델 버전 확인, generate_image/pptxgenjs 설치, 라우팅 등록
2. **전체 수행**: `/finops:core` — WHY → Inform → Optimize → Operate → Review 순차 실행
3. **단독 실행**: `/finops:{skill-name}` — 해당 스킬만 개별 실행
4. **PPT 제작**: review APPROVED 후 `/finops:ppt-writer`로 발표자료 빌드 (post-hoc)

## 산출물 디렉토리 구조

```
finops-lab/
├── out/
│   ├── why-statement.md                # WHY 정의 문서
│   ├── step1/                          # WHY-FinOps 산출물 (1-drivers / 2-maturity / 3-covers)
│   ├── focus-normalized.csv            # FOCUS 정규화 데이터
│   ├── dashboard.html                  # Chart.js 9차트 대시보드
│   ├── step2/                          # Inform 산출물 (source-profile / tag-coverage)
│   ├── rightsize-plan.md               # Right-sizing 계획서
│   ├── commit-strategy.md              # 약정 전략 문서
│   ├── step3/                          # Optimize 산출물 (idle-resources / scaling-policy)
│   ├── review-runbook.md               # 주/월/분기 리뷰 런북
│   ├── step4/                          # Operate 산출물 (unit-economics / automation / transition)
│   ├── review-report.md                # 최종 독립 검증 보고서
│   └── ppt-scripts/                    # PPT 빌드 스크립트·spec·이미지·.pptx
│       ├── index.md                    # 선별 결과
│       ├── images/                     # Gemini 생성 일러스트
│       ├── {대상}-spec.md              # 시각 명세 (pptx-spec-writer 산출)
│       ├── {대상}-build.js             # pptxgenjs 빌드 스크립트
│       └── {대상}-deck.pptx            # 최종 PPT
├── references/                         # 교재·가이드
│   ├── am/finops.md                    # 1차 교재
│   └── finops/state-of-finops-2026-lab-guide.md
└── resources/                          # 샘플 데이터·규칙·템플릿
    ├── sample-billing/*.csv
    ├── schema/focus-v1.yaml
    ├── rulebook/                       # covers-principles / gate-criteria
    ├── mapping/                        # CSP→FOCUS 매핑 YAML
    └── templates/                      # kpi-dashboard / tag-policy 등
```

### 참고 문서

| 구분 | 경로 |
|------|------|
| 1차 교재 | `references/am/finops.md` §4.1~§4.16 |
| 2026 가이드 | `references/finops/state-of-finops-2026-lab-guide.md` |
| 샘플 데이터 | `resources/sample-billing/*.csv` |
| PPT 스타일 가이드 | `agents/pptx-spec-writer/references/pptx-build-guide.md` + `finops-ppt-addendum.md` |
