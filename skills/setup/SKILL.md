---
name: setup
description: finops 플러그인 초기 설정 (모델 버전 확인, generate_image 설치, DMAP Office 빌더 런타임 설치, 라우팅 등록)
type: setup
user-invocable: true
---

# Setup

[SETUP 활성화]

## 목표

finops 플러그인의 도구/환경/라우팅을 초기화하여 즉시 사용 가능 상태로 만듦.
`gateway/runtime-mapping.yaml` 모델 버전 갱신, `generate_image` 선택적 설치,
**DMAP Office 빌더 런타임(`pptxgenjs`) 자동 검증·설치**,
CLAUDE.md 라우팅 등록을 순차 수행함.

## 활성화 조건

사용자가 `/finops:setup` 호출 시 또는 "finops 설치" 키워드 감지 시.

## 워크플로우

### Step 1: 플러그인 변수 확인 (`ulw` 활용)

프로젝트 AGENTS.md(`./AGENTS.md`)의 `## 플러그인 변수` 섹션에서 아래 4개 변수를 확인함.

| 변수 | 기대값 예시 |
|------|------------|
| `AI_RUNTIME` | `Claude Code` |
| `DMAP_PLUGIN_DIR` | `/Users/dreamondal/plugins/dmap` |
| `PLUGIN_DIR` | `/Users/dreamondal/plugins/finops-lab` |
| `PLUGIN_NAME` | `finops` |

누락된 변수 발견 시 사용자에게 해당 변수명과 예시값을 안내하고 `./AGENTS.md`의 `## 플러그인 변수` 섹션에 추가할 것을 요청함. 4개 모두 확인 시 Step 2로 진행함.

### Step 2: 런타임 최신 모델 버전 확인 (`ulw` 활용)

`gateway/runtime-mapping.yaml`의 `tier_mapping.{claude-code, cursor, codex, antigravity}` 4런타임 엔트리를 읽어 사용자에게 표시함.

**Claude 계열 런타임**(claude-code / cursor / antigravity):
- WebFetch로 `https://docs.anthropic.com/en/docs/about-claude/models` 조회 → 최신 Opus/Sonnet/Haiku 확인

**OpenAI 계열 런타임**(codex):
- WebFetch로 OpenAI 모델 페이지 조회 → `gpt-5.4`(flagship), `gpt-5.2-codex`, `gpt-5.1-codex-max`, `gpt-5.4-mini` 중 최신 버전 확인

WebFetch 접근 불가 시 사용자에게 최신 모델명 직접 입력을 안내함.

현재 값과 최신 값을 비교하여 차이가 있을 경우 AskUserQuestion으로 4런타임 일괄 갱신 여부를 질의함.

- "Yes" 선택 시: `gateway/runtime-mapping.yaml`의 해당 tier_mapping 엔트리를 최신 모델명으로 갱신함 + **Step 2.5 실행**
- "No" 선택 시: 현재 버전 유지, Step 3으로 진행함

### Step 2.5: 런타임 어댑터 frontmatter 일괄 갱신 (`ulw` 활용)

Step 2에서 tier_mapping이 갱신된 경우, 런타임 어댑터 포인터 스텁의 frontmatter `model:` 필드를 새 매핑값으로 일괄 치환함 (본문·주석은 절대 수정 금지).

| 대상 경로 | 파일 | 매핑 참조 |
|-----------|------|-----------|
| `.claude/agents/*.md` | 9개 | `tier_mapping.claude-code.{tier}.model` |
| `.cursor/agents/*.md` | 9개 | `tier_mapping.cursor.{tier}.model` |
| `.codex/agents/*.toml` | 9개 | `tier_mapping.codex.{tier}.model` |
| `.antigravity/agents/*.md` | 9개 | `tier_mapping.antigravity.{tier}.model` |

각 어댑터 파일의 에이전트 이름으로 `agents/{name}/agentcard.yaml`을 참조하여 tier를 해결한 뒤, 런타임·tier 조합에 따른 최신 모델명으로 frontmatter `model:` 한 줄만 치환함. 총 36개 파일 일괄 처리.

본 Step은 Step 2의 갱신 여부와 무관하게 어댑터 파일 존재 여부를 점검하며, 누락된 어댑터가 있으면 사용자에게 보고함.

### Step 3-A: generate_image 도구 설치 (`ulw` 활용)

`gateway/install.yaml`에서 `generate_image` 항목의 `required: false` 확인 후 AskUserQuestion으로 설치 여부를 질의함.

**"Yes" 선택 시:**

1. Python 의존성 설치:
   ```bash
   pip install python-dotenv google-genai
   ```
2. 설치 검증:
   ```bash
   python gateway/tools/generate_image.py --help
   ```
3. `.env` 파일 생성:
   - `gateway/tools/.env.example` 존재 시: 해당 파일을 `gateway/tools/.env`로 복사 후 `GEMINI_API_KEY` 값 입력을 요청함
   - `.env.example` 부재 시: `GEMINI_API_KEY` 한 줄만 받아 `gateway/tools/.env`를 직접 생성함
   - AskUserQuestion으로 `GEMINI_API_KEY` 값을 수집하여 파일에 기록함

**"No" 선택 시:**

설치를 스킵함. 이후 `/finops:ppt-writer` 실행 시 이미지 생성 없이 텍스트 슬라이드로만 제작됨을 안내함.

### Step 3-B: DMAP Office 빌더 런타임(`pptxgenjs`) 설치 (`ulw` 활용)

`gateway/install.yaml`의 `runtime_dependencies` 섹션을 파싱하여 `pptxgenjs` 엔트리를 처리함.

#### 3-B-1. 사전 런타임 확인

- `node --version` 실행 → v18 이상 확인
- 미설치 또는 v18 미만 시 Node.js 18+ 설치 안내(https://nodejs.org/) 후 Step 3-B 중단
- `npm --version` 실행 → npm 사용 가능 확인

#### 3-B-2. pptxgenjs 설치 검증·설치

1. **check 명령 실행** (`install.yaml`의 `runtime_dependencies.pptxgenjs.check`):
   ```bash
   node -e "require('pptxgenjs')"
   ```
2. exit code 0이면 이미 설치됨 → 표시하고 3-B-3으로 진행
3. 실패 시 AskUserQuestion으로 설치 동의 요청 → 동의 시 install 명령 실행:
   ```bash
   # 설치 위치: 플러그인 루트(finops-lab/)
   #   사유: Node 모듈 해석은 스크립트 디렉토리에서 상위로 탐색함.
   #        out/ppt-scripts/{대상}-build.js 에서 require('pptxgenjs')가
   #        finops-lab/node_modules/를 찾아야 하므로 플러그인 루트 설치 필수.
   #        gateway/는 out/과 형제라 해석 경로에 포함되지 않음.
   cd "$PLUGIN_DIR"
   [ -f package.json ] || npm init -y
   npm install pptxgenjs
   ```
4. 설치 후 `check` 재실행으로 결과 검증
5. `.gitignore`에 `node_modules/` 등록 권장 (미등록 시 자동 추가)

#### 3-B-3. 실사용 CWD 해석 검증

`/finops:ppt-writer`가 실제 빌드를 실행하는 CWD에서 모듈 해석 성공 여부 확인:

```bash
cd "$PLUGIN_DIR/out" && node -e "require('pptxgenjs')"
```

실패 시 설치 위치 오류(예: `gateway/` 설치됨) — 플러그인 루트 재설치 안내.

### Step 4: 라우팅 테이블 등록 (`ulw` 활용)

AskUserQuestion으로 라우팅 등록 적용 범위를 질의함.

| 선택지 | 대상 파일 | 동작 |
|--------|----------|------|
| 모든 프로젝트 | `~/.claude/CLAUDE.md` | 전역 라우팅 섹션 추가 (Claude Code 전역 설정) |
| 이 프로젝트만 | `./AGENTS.md` | 현재 프로젝트 AGENTS.md에 섹션 추가 |

등록 내용 (`## finops 플러그인` 섹션):

```markdown
## finops 플러그인

### 라우팅 키워드
- `@setup`, "finops 설치" → `/finops:setup`
- `@help`, "finops 도움말", "finops 뭘 할 수 있어" → `/finops:help`
- `@why-finops`, "FinOps 왜" → `/finops:why-finops`
- `@inform`, "FOCUS 정규화", "대시보드" → `/finops:inform`
- `@optimize`, "Right-sizing", "약정" → `/finops:optimize`
- `@operate`, "KPI", "리뷰 런북" → `/finops:operate`
- `@review`, "최종 검증" → `/finops:review`
- `@ppt-writer`, "PPT deck", "발표자료" → `/finops:ppt-writer`
- `@core`, "FinOps 랩 전체" → `/finops:core`
```

### Step 5: 설치 결과 요약 보고 (`ulw` 활용)

모든 Step 완료 후 결과를 체크리스트 형식으로 출력함.

```
✅ Step 1: 플러그인 변수 4개 확인 완료 (AI_RUNTIME·DMAP_PLUGIN_DIR·PLUGIN_DIR·PLUGIN_NAME)
✅ Step 2: 4런타임 모델 버전 확인/갱신 완료 (claude-code·cursor·codex·antigravity)
✅ Step 2.5: 런타임 어댑터 36개 frontmatter 일괄 갱신 완료
✅ Step 3-A: generate_image 설치 [완료 | 스킵]
✅ Step 3-B: pptxgenjs 설치 [완료 | 이미 설치됨 | 스킵(Node 미설치)]
✅ Step 4: 라우팅 테이블 등록 완료 ([모든 프로젝트 | 이 프로젝트만])

다음 단계:
- 전체 명령 목록 확인: /finops:help
- FinOps 전체 파이프라인 실행: /finops:core
- PPT deck 빌드: /finops:ppt-writer
```

## 사용자 상호작용

AskUserQuestion을 활용한 5가지 질의 (최대 5회):

| 순서 | 질의 내용 | 선택지 |
|------|----------|--------|
| 1 | 최신 모델 버전으로 `runtime-mapping.yaml` 갱신 여부 | Yes / No |
| 2 | `generate_image` 도구 설치 여부 | Yes / No |
| 3 | `GEMINI_API_KEY` 입력 (Step 3-A "Yes" 선택 시에만) | 문자열 입력 |
| 4 | `pptxgenjs` 설치 여부 (check 실패 시에만) | Yes / No |
| 5 | 라우팅 등록 적용 범위 | 모든 프로젝트 / 이 프로젝트만 |

## 스킬 위임

없음. 모두 직결형 Gateway 도구(Bash, Read, Write, AskUserQuestion, WebFetch) 직접 사용.

## 문제 해결

| 문제 | 대응 |
|------|------|
| Python 미설치 | `python --version` 확인 후 미설치 시 https://python.org 에서 3.9 이상 버전 설치 안내함 |
| Node.js 미설치 / v18 미만 | `node --version` 확인 후 https://nodejs.org/ 에서 18 LTS 이상 설치 안내함 |
| Gemini API Key 발급 필요 | https://ai.google.dev/ 에서 Google 계정으로 로그인 후 API 키 발급 안내함 |
| `GEMINI_API_KEY` 오류 (401/403) | 키 값 오타 확인 및 `gateway/tools/.env` 파일 내 `GEMINI_API_KEY=<값>` 형식 점검 안내함 |
| `node -e "require('pptxgenjs')"` 오류 | pptxgenjs 미설치 | 플러그인 루트(`finops-lab/`)에서 `npm install pptxgenjs` |
| `/ppt-writer` 실행 시 `Cannot find module 'pptxgenjs'` | `gateway/` 등 하위 디렉토리에 설치됨 (Node 해석 경로 밖) — 플러그인 루트로 재설치: `cd "$PLUGIN_DIR" && npm install pptxgenjs` |
| CLAUDE.md 쓰기 권한 오류 | 해당 파일 권한(`chmod 644` 또는 Windows ACL) 확인 및 수동 등록 방법 안내함 |
| WebFetch 접근 불가 | Anthropic 최신 모델 목록(https://docs.anthropic.com/en/docs/about-claude/models) 수동 확인 후 직접 입력 요청함 |

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | `disable-model-invocation` 설정 금지 — 설정 시 스킬 로드 자체가 불가함 |
| 2 | 모델명은 항상 Anthropic 공식 최신 버전을 반영해야 함 |
| 3 | AskUserQuestion 없이 사용자 선택을 임의 결정하지 않음 |

## 검증

각 Step 완료 증거:

| Step | 완료 증거 |
|------|----------|
| Step 1 | `./AGENTS.md` 내 4개 변수(`AI_RUNTIME`·`DMAP_PLUGIN_DIR`·`PLUGIN_DIR`·`PLUGIN_NAME`) 존재 확인 (Read 도구 출력) |
| Step 2 | `gateway/runtime-mapping.yaml` diff — 4런타임 변경 전/후 모델명 출력 (갱신 선택 시) |
| Step 2.5 | `.claude/agents/*.md`, `.cursor/agents/*.md`, `.codex/agents/*.toml`, `.antigravity/agents/*.md` frontmatter `model:` 필드가 runtime-mapping.yaml 값과 일치 |
| Step 3-A | `python gateway/tools/generate_image.py --help` 정상 출력 (설치 선택 시) |
| Step 3-B | `cd "$PLUGIN_DIR/out" && node -e "require('pptxgenjs')"` 정상 종료(exit 0) |
| Step 4 | 대상 파일(AGENTS.md 또는 ~/.claude/CLAUDE.md) 내 `## finops 플러그인` 섹션 존재 확인 (Read 도구 출력) |
| Step 5 | 체크리스트 출력 및 다음 단계 안내 완료 |
