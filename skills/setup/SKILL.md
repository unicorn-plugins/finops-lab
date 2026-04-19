---
name: setup
description: finops 플러그인 초기 설정 (모델 버전 확인, generate_image 설치, 라우팅 등록)
type: setup
user-invocable: true
---

# Setup

[SETUP 활성화]

## 목표

finops 플러그인의 도구/환경/라우팅을 초기화하여 즉시 사용 가능 상태로 만듦.
`gateway/runtime-mapping.yaml` 모델 버전 갱신, `generate_image` 선택적 설치, CLAUDE.md 라우팅 등록을 순차 수행함.

## 활성화 조건

사용자가 `/finops:setup` 호출 시 또는 "finops 설치" 키워드 감지 시.

## 워크플로우

### Step 1: 플러그인 변수 확인 (`ulw` 활용)

프로젝트 CLAUDE.md(`./CLAUDE.md`)에서 아래 4개 변수를 확인함.

| 변수 | 기대값 예시 |
|------|------------|
| `CLAUDE_RUNTIME` | `Claude Code` |
| `DMAP_PLUGIN_DIR` | `C:\Users\hiond\workspace\dmap` |
| `PLUGIN_DIR` | `C:\Users\hiond\workshop\finops-lab` |
| `PLUGIN_NAME` | `finops` |

누락된 변수 발견 시 사용자에게 해당 변수명과 예시값을 안내하고 `./CLAUDE.md`의 `## 플러그인 변수 설정` 섹션에 추가할 것을 요청함. 4개 모두 확인 시 Step 2로 진행함.

### Step 2: 런타임 최신 모델 버전 확인 (`ulw` 활용)

`gateway/runtime-mapping.yaml`의 현재 `tier_mapping.default` 값을 읽어 사용자에게 표시함.

WebFetch로 `https://docs.anthropic.com/en/docs/about-claude/models` 를 조회하여 Anthropic의 최신 Opus/Sonnet/Haiku 모델 버전을 확인함. WebFetch 접근 불가 시 사용자에게 최신 모델명 직접 입력을 안내함.

현재 값과 최신 값을 비교하여 차이가 있을 경우 AskUserQuestion으로 갱신 여부를 질의함.

- "Yes" 선택 시: `gateway/runtime-mapping.yaml`의 `tier_mapping.default` 항목을 최신 모델명으로 갱신함
- "No" 선택 시: 현재 버전 유지, Step 3으로 진행함

### Step 3: generate_image 도구 설치 (`ulw` 활용)

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

### Step 4: 라우팅 테이블 등록 (`ulw` 활용)

AskUserQuestion으로 라우팅 등록 적용 범위를 질의함.

| 선택지 | 대상 파일 | 동작 |
|--------|----------|------|
| 모든 프로젝트 | `~/.claude/CLAUDE.md` | 전역 라우팅 섹션 추가 |
| 이 프로젝트만 | `./CLAUDE.md` | 현재 프로젝트 CLAUDE.md에 섹션 추가 |

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
✅ Step 1: 플러그인 변수 4개 확인 완료
✅ Step 2: 모델 버전 확인/갱신 완료 (HEAVY: claude-opus-4-7, MEDIUM: claude-sonnet-4-6, LOW: claude-haiku-4-5)
✅ Step 3: generate_image 설치 [완료 | 스킵]
✅ Step 4: 라우팅 테이블 등록 완료 ([모든 프로젝트 | 이 프로젝트만])

다음 단계:
- 전체 명령 목록 확인: /finops:help
- FinOps 전체 파이프라인 실행: /finops:core
```

## 사용자 상호작용

AskUserQuestion을 활용한 4가지 질의 (최대 4회):

| 순서 | 질의 내용 | 선택지 |
|------|----------|--------|
| 1 | 최신 모델 버전으로 `runtime-mapping.yaml` 갱신 여부 | Yes / No |
| 2 | `generate_image` 도구 설치 여부 | Yes / No |
| 3 | `GEMINI_API_KEY` 입력 (Step 3 "Yes" 선택 시에만) | 문자열 입력 |
| 4 | 라우팅 등록 적용 범위 | 모든 프로젝트 / 이 프로젝트만 |

## 스킬 위임

없음. 모두 직결형 Gateway 도구(Bash, Read, Write, AskUserQuestion, WebFetch) 직접 사용.

## 문제 해결

| 문제 | 대응 |
|------|------|
| Python 미설치 | `python --version` 확인 후 미설치 시 https://python.org 에서 3.9 이상 버전 설치 안내함 |
| Gemini API Key 발급 필요 | https://ai.google.dev/ 에서 Google 계정으로 로그인 후 API 키 발급 안내함 |
| `GEMINI_API_KEY` 오류 (401/403) | 키 값 오타 확인 및 `gateway/tools/.env` 파일 내 `GEMINI_API_KEY=<값>` 형식 점검 안내함 |
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
| Step 1 | `./CLAUDE.md` 내 4개 변수 존재 확인 (Read 도구 출력) |
| Step 2 | `gateway/runtime-mapping.yaml` diff — 변경 전/후 모델명 출력 (갱신 선택 시) |
| Step 3 | `python gateway/tools/generate_image.py --help` 정상 출력 (설치 선택 시) |
| Step 4 | 대상 CLAUDE.md 내 `## finops 플러그인` 섹션 존재 확인 (Read 도구 출력) |
| Step 5 | 체크리스트 출력 및 다음 단계 안내 완료 |
