# finops

> **멀티클라우드 FinOps + FinOps for AI** 실습 플러그인 — 4단계(WHY → Inform → Optimize → Operate) + 검증 + PPT 제작까지
> FinOps 교재·State of FinOps 2026 프레임워크를 가상 기업 (주)하이브리지텔레콤(HBT) 데이터로 손으로 돌려보며 체득.

---

## 개요

`finops`는 FinOps 도메인을 4단계 순환(보이기 → 줄이기 → 체계화)과 2025~2026 업데이트
(FOCUS · Ownership×Capability · Cloud+ · FinOps for AI)를 적용해 실습하는
DMAP(Declarative Multi-Agent Plugin) 표준 플러그인.

### 주요 기능

| 스킬 | 역할 | 핵심 산출물 |
|------|------|-------------|
| `@why-finops` | WHY 정의 & 성숙도 진단 | `out/why-statement.md` + Ownership×Capability 진단 + COVERS 로드맵 |
| `@inform` | FOCUS 정규화 & 통합 가시성 | `out/focus-normalized.csv` + `out/dashboard.html` (Chart.js 9차트) |
| `@optimize` | Right-sizing & 약정 전략 | `out/rightsize-plan.md` + `out/commit-strategy.md` (RI/SP/Spot 3시나리오) |
| `@operate` | KPI · 자동화 · 리뷰 런북 | `out/review-runbook.md` + KPI 6종 + 게이트 6종 |
| `@review` | 최종 독립 검증 | `out/review-report.md` (판정 APPROVED/REJECTED) |
| `@ppt-writer` | PPT Deck + 실제 .pptx 제작 | `out/ppt-scripts/*-deck.pptx` (DMAP 2단계: pptx-spec-writer → pptxgenjs build.js 직접 실행) |
| `@core` | 풀 파이프라인 | 위 5개 순차 실행 (ppt-writer 제외) |

### 하이라이트

- **FOCUS v1.3 + AI 확장 5종**: TokenCountInput/Output · ModelName · GpuHours · GpuUtilization
- **FinOps for AI**: LLM 토큰·GPU 특화 메트릭 + 단위경제 KPI(토큰 1M당·추론 1K당·GPU 시간당)
- **인터랙티브 대시보드**: 단일 HTML 파일(<1.2MB, Chart.js 4.x CDN, 9차트, 오프라인 열람)
- **PPT 제작**: DMAP 표준 2단계 패턴 — `pptx-spec-writer` 명세 + `pptxgenjs` 직접 빌드 (Node.js ≥18 필요)
- **증거 기반**: 모든 권고가 COVERS 규칙 ID(`COVERS-*-##`)·게이트 항목으로 역참조 가능

---

## 설치

### 1. 마켓플레이스 등록 + 플러그인 설치

```bash
# 로컬 디렉토리 마켓플레이스로 등록
claude plugin marketplace add C:\Users\hiond\workshop\finops-lab

# 또는 GitHub에서 설치 (publish 후)
# claude plugin marketplace add hiondal/finops-lab

# 플러그인 설치
claude plugin install finops@finops
```

### 2. 플러그인 초기 설정 실행

```
/finops:setup
```

이 스킬은 아래를 수행:

- CLAUDE.md 플러그인 변수 확인
- 런타임 최신 모델 버전 확인 후 `gateway/runtime-mapping.yaml` 갱신
- `generate_image` 도구 설치 여부 질의 (선택):
  - 설치 시: `pip install python-dotenv google-genai` + `.env` 생성 + `GEMINI_API_KEY` 입력
  - 스킵 시: `@ppt-writer`에서 텍스트 슬라이드로 제작
- **DMAP Office 빌더 런타임 설치 (필수)**:
  - `pptxgenjs` (Node.js ≥18) — 플러그인 루트(`finops-lab/`)에 설치
  - `node -e "require('pptxgenjs')"` 성공 여부 자동 검증
  - 미설치 시 `npm install pptxgenjs` 제안 및 실행
- 라우팅 테이블 등록 (`~/.claude/CLAUDE.md` 또는 프로젝트 `CLAUDE.md`)

### 3. (선택) DMAP 플러그인 디렉토리 접근 권한 설정

`.claude/settings.local.json.example`을 `.claude/settings.local.json`으로 복사하여
플러그인 디렉토리에 대한 Read/Write/Edit/Bash 권한을 부여함.

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
```

> 이 파일은 보안 정책상 Claude Code가 자동 생성하지 않으므로 사용자가 직접 복사해야 함.

---

## 업그레이드

### GitHub 마켓플레이스

```bash
claude plugin marketplace update finops
claude plugin install finops@finops
claude plugin list
```

### 로컬 마켓플레이스

```bash
cd C:\Users\hiond\workshop\finops-lab
git pull origin main   # 최신 변경 반영
claude plugin marketplace update finops
claude plugin install finops@finops
```

### 업그레이드 후 재설정

`gateway/install.yaml`에 새 도구가 추가된 경우 반드시 재실행:

```
/finops:setup
```

---

## 사용법

### 빠른 시작 — 전체 파이프라인 한 번에

```
/finops:core
```

자동으로 `@why-finops → @inform → @optimize → @operate → @review` 5단계를 순차 실행.

### 개별 스킬 실행 (단계별)

```
/finops:why-finops    # STEP 1: WHY 정의
/finops:inform        # STEP 2: FOCUS 정규화 + 대시보드
/finops:optimize      # STEP 3: Right-sizing + 약정 전략
/finops:operate       # STEP 4: KPI + 자동화 + 리뷰 런북
/finops:review        # STEP 5: 최종 검증
/finops:ppt-writer    # (선택) PPT Deck + .pptx 제작
```

### 자연어 라우팅

CLAUDE.md에 라우팅이 등록되어 있으면 아래 키워드만으로 호출:

- "@why-finops", "FinOps 왜" → why-finops
- "@inform", "FOCUS 정규화", "대시보드" → inform
- "@optimize", "Right-sizing", "약정" → optimize
- "@operate", "KPI", "리뷰 런북" → operate
- "@review", "최종 검증" → review
- "@ppt-writer", "PPT deck", "발표자료" → ppt-writer
- "@core", "FinOps 랩 전체" → core

### 사용 안내

```
/finops:help
```

명령 목록·라우팅·핵심 산출물을 즉시 출력.

### 산출물 위치

```
out/
├── step1/ step2/ step3/ step4/   # 단계별 세부 산출물
├── why-statement.md               # 경영진 WHY 통합본 + 12개월 OKR
├── focus-normalized.csv           # FOCUS v1.3 + AI 확장 5종 (~2,500 rows)
├── dashboard.html                 # 단일 파일 대시보드 (Chart.js 9차트)
├── rightsize-plan.md              # Right-sizing 3대안 + GPU + 모델 다운그레이드
├── commit-strategy.md             # RI/SP/Spot 3시나리오 (Conservative/Base/Optimistic)
├── review-runbook.md              # 주/월/분기 리뷰 런북 + 게이트 6종
├── review-report.md               # 독립 검증 리포트 (판정 APPROVED/REJECTED)
└── ppt-scripts/                   # @ppt-writer 산출물 (DMAP 2단계 빌드)
    ├── index.md                   # 선별 결과
    ├── images/                    # Gemini 생성 일러스트 (선택)
    ├── {대상}-spec.md             # pptx-spec-writer 명세 (패턴 A~F)
    ├── {대상}-build.js            # pptxgenjs 빌드 스크립트 (skills/ppt-writer 직접 작성)
    └── {대상}-deck.pptx           # 최종 PowerPoint 파일
```

---

## 요구사항

### 런타임

- Claude Code / Claude CoWork / Claude.ai
- DMAP 빌더 표준 지원 런타임
- Node.js ≥ 18 (`@ppt-writer` .pptx 빌드용 — 필수)
- Python ≥ 3.9 (`@ppt-writer` 이미지 생성 시 — 선택)

### MCP/LSP 서버

- **없음** — Claude Code 빌트인 + OMC 기본 제공으로 완결

### DMAP Office 빌더 런타임 (필수 — `/finops:setup`이 자동 설치)

| 항목 | 용도 | 설치 | 설치 위치 |
|------|------|------|----------|
| Node.js ≥ 18 | `pptxgenjs` 실행 환경 | https://nodejs.org/ | 시스템 |
| `pptxgenjs` | `.pptx` 빌드 (spec.md → build.js) | `npm install pptxgenjs` | **플러그인 루트** (`finops-lab/node_modules/`) |

> `pptxgenjs`는 반드시 **플러그인 루트**에 설치함. `gateway/`는 `out/`과 형제라 Node 모듈 해석 경로에 포함되지 않음.

### 외부 의존성 (선택 — `@ppt-writer` 이미지 생성 시만)

| 항목 | 용도 | 설치 |
|------|------|------|
| Python ≥ 3.10 | `generate_image.py` 실행 | 시스템 기본 |
| `python-dotenv` | `.env` 로드 | `pip install python-dotenv` |
| `google-genai` | Gemini Nano Banana API | `pip install google-genai` |
| `GEMINI_API_KEY` | Gemini API 접근 | https://ai.google.dev/ |

> 이미지 없는 텍스트 슬라이드만 생성할 경우 Python 의존성은 **0**. `.pptx` 바이너리 빌드는 `skills/ppt-writer`가 `pptxgenjs`로 `build.js`를 직접 실행 (외부 스킬 위임 없음).

### 샘플 데이터 (플러그인 내장)

| 자원 | 경로 |
|------|------|
| HBT 회사 프로파일 | `resources/basic-info/company-profile.md` |
| AWS CUR 2.0 샘플 | `resources/sample-billing/aws-cur-sample.csv` |
| Azure Cost Export 샘플 | `resources/sample-billing/azure-export-sample.csv` |
| GCP Billing Export 샘플 | `resources/sample-billing/gcp-billing-sample.csv` |
| utilization (CPU/Memory/GPU) | `resources/sample-billing/utilization-sample.csv` |
| SaaS LLM (OpenAI/Anthropic) | `resources/sample-billing/saas-llm-sample.csv` |
| FOCUS v1.3 스키마 | `resources/schema/focus-v1.yaml` |
| COVERS 6원칙 룰북 | `resources/rulebook/covers-principles.yaml` |
| 게이트 기준 6종 | `resources/rulebook/gate-criteria.yaml` |

### 1차 교재

- `references/am/finops.md` — FinOps 교재 §4.1~§4.16
- `references/finops/state-of-finops-2026-lab-guide.md` — State of FinOps 2026 실습 가이드

---

## 아키텍처

```
Skills (Controller+UseCase)       Agents (Service)                Gateway (Infrastructure)
────────────────────────────      ────────────────────            ──────────────────────
setup (Setup)                     strategy-director    HIGH       install.yaml
help (Utility)                    focus-normalizer     MEDIUM       └─ runtime_dependencies
why-finops (Orchestrator)  ─────▶ cost-analyst         MEDIUM         └─ pptxgenjs (Node)
inform (Orchestrator)             tag-governor         LOW        runtime-mapping.yaml
optimize (Orchestrator)           rightsize-advisor    MEDIUM     tools/
operate (Orchestrator)            commit-planner       HIGH        └─ generate_image.py
review (Orchestrator)             finops-practitioner  MEDIUM
ppt-writer (Orchestrator)  ─────▶ pptx-spec-writer     MEDIUM     플러그인 루트:
core (Orchestrator, 파이프라인)   reviewer             HIGH        └─ node_modules/pptxgenjs
```

- **스킬 9종** + **에이전트 9종** + **Gateway 1세트** + **commands 9개 진입점**
- 에이전트 간 직접 호출 없음 — 스킬이 순차 오케스트레이션
- `.pptx` 바이너리 빌드는 `skills/ppt-writer`가 `pptxgenjs` `build.js`를 **직접 작성·실행** (외부 스킬 위임 없음, DMAP 2단계 패턴)

---

## 라이선스

MIT License — © 2026 hiondal
