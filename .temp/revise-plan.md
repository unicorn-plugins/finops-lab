# finops 플러그인 DMAP 표준 반영 계획서

## 변경 개요

DMAP 공통표준(`plugin-standard.md`), 스킬표준(`plugin-standard-skill.md`),  
`develop-plugin` 스킬의 개정 내용을 현재 `finops` 플러그인에 반영함.

### 핵심 변경 포인트
1. **AGENTS.md 도입** — CLAUDE.md는 `@AGENTS.md` 임포트만 유지 (주 문서 승격)
2. **런타임 어댑터 포인터 생성** — `.claude/`, `.cursor/`, `.codex/`, `.antigravity/` 하위 에이전트 스텁 일괄 생성
3. **runtime-mapping.yaml 4-런타임 tier_mapping 확장** — claude-code/cursor/codex/antigravity 엔트리 추가
4. **command 진입점 참조 파일 변경** — `CLAUDE.md` → `AGENTS.md`
5. **Help 스킬 구조 표준화** — `## 사용 안내`, `## 산출물 디렉토리 구조` 섹션 도입
6. **Setup 스킬 보강** — 런타임 어댑터 frontmatter 일괄 갱신 Phase 추가, `AI_RUNTIME` 변수명 반영
7. **변수명 정리** — `CLAUDE_RUNTIME` → `AI_RUNTIME` (DMAP 표준 명칭)

---

## 1. 프로젝트 최상위 파일

| 파일 | 라인 | 현재 내용 | 변경 내용 |
|------|------|----------|----------|
| `AGENTS.md` | (신규 전체) | (없음) | `CLAUDE.md` 현 콘텐츠를 그대로 이전. 단 변수명 `CLAUDE_RUNTIME` → `AI_RUNTIME`, 윈도우 경로를 현 macOS 절대경로(`/Users/dreamondal/plugins/dmap`, `/Users/dreamondal/plugins/finops-lab`)로 교체 |
| `CLAUDE.md` | 전체 | 137줄 전체 콘텐츠(팀 소개·멤버·행동원칙 등) | 상단에 `@AGENTS.md` 한 줄만 남기고 나머지 삭제 (develop-plugin Phase 4 표준) |

---

## 2. commands/ 진입점 (9개 파일)

모든 `commands/*.md`의 Step 1 참조 파일을 `CLAUDE.md` → `AGENTS.md`로 변경.

| 파일 | 라인 | 현재 내용 | 변경 내용 |
|------|------|----------|----------|
| `commands/setup.md` | 5 | ``...프로젝트의 `CLAUDE.md` 파일을...`` | ``...프로젝트의 `AGENTS.md` 파일을...`` |
| `commands/help.md` | 5 | 동일 | 동일 |
| `commands/core.md` | 5 | 동일 | 동일 |
| `commands/why-finops.md` | 5 | 동일 | 동일 |
| `commands/inform.md` | 5 | 동일 | 동일 |
| `commands/optimize.md` | 5 | 동일 | 동일 |
| `commands/operate.md` | 5 | 동일 | 동일 |
| `commands/review.md` | 5 | 동일 | 동일 |
| `commands/ppt-writer.md` | 5 | 동일 | 동일 |

---

## 3. gateway/runtime-mapping.yaml

`develop-plugin` 표준: "`tier_mapping`은 claude-code/cursor/codex/antigravity 4런타임 모두에 대한 tier별 모델 엔트리 포함 필수".

| 파일 | 라인 | 현재 내용 | 변경 내용 |
|------|------|----------|----------|
| `gateway/runtime-mapping.yaml` | 4-18 | `tier_mapping:` 하위에 `default:`, `pptx-spec-writer:` 만 존재 | `tier_mapping:` 하위에 `claude-code:`, `cursor:`, `codex:`, `antigravity:` 4런타임 엔트리 신설. claude-code/cursor/antigravity는 기존 `default` 값과 동일(Claude 최신 모델), codex는 `gpt-5.4`/`gpt-5.2-codex`/`gpt-5.4-mini`로 설정. `pptx-spec-writer` 오버라이드는 claude-code 하위로 이동 |

---

## 4. 런타임 어댑터 포인터 생성 (신규 36개 파일)

`develop-plugin` Step 4-A 준수. 9개 에이전트 × 4런타임 = 36개 얇은 포인터 스텁 생성.  
각 어댑터는 SSOT(`agents/{name}/`)를 가리키며 frontmatter의 `model:`은 `runtime-mapping.yaml`에서 해결.

**대상 에이전트(9종)**: `commit-planner`, `cost-analyst`, `finops-practitioner`, `focus-normalizer`, `pptx-spec-writer`, `reviewer`, `rightsize-advisor`, `strategy-director`, `tag-governor`

| 경로 | 포맷 | 템플릿 | 파일 수 |
|------|------|--------|---------|
| `.claude/agents/{name}.md` | Markdown + YAML frontmatter | `{DMAP}/resources/templates/runtime-adapters/claude-code.md.tmpl` | 9 |
| `.cursor/agents/{name}.md` | Markdown + YAML frontmatter | `{DMAP}/resources/templates/runtime-adapters/cursor.md.tmpl` | 9 |
| `.codex/agents/{name}.toml` | TOML | `{DMAP}/resources/templates/runtime-adapters/codex.toml.tmpl` | 9 |
| `.antigravity/agents/{name}.md` | Markdown + 수동 로드 안내 | `{DMAP}/resources/templates/runtime-adapters/antigravity.md.tmpl` | 9 |

**치환 변수**: `{name}` = 에이전트 디렉토리명, `{description}` = `AGENT.md` frontmatter.description, `{model}` = `runtime-mapping.yaml`의 해당 런타임/tier 해결값, `{plugin}` = `finops`, `{fqn}` = `finops:{name}:{name}`.

---

## 5. skills/help/SKILL.md

스킬표준 "Help 스킬 고유 섹션" 준수: `## 사용 안내`(필수), `## 산출물 디렉토리 구조`(필수), `@{skill-name}으로 Skill 직접 호출 가능` 명시.

| 파일 | 라인 | 현재 내용 | 변경 내용 |
|------|------|----------|----------|
| `skills/help/SKILL.md` | 19-32 | `## 명령어` 섹션 (표준 섹션명 아님) | `## 사용 안내` 섹션으로 rename. 하위에 `### 명령어`, `### 자동 라우팅 (키워드 감지)`, `### Quick Guide` 배치 |
| `skills/help/SKILL.md` | 33-62 | `## 워크플로우` 하위에 명령어·키워드·산출물 혼재 | `## 사용 안내` 하위에 통합. 명령어 테이블 뒤에 ```@{스킬명}으로 Skill 직접 호출 가능``` 문구 추가 |
| `skills/help/SKILL.md` | 63-84 | `### 핵심 산출물`, `### 참고` (워크플로우 안) | `## 산출물 디렉토리 구조` 최상위 섹션으로 승격, 트리 포맷 사용 |
| `skills/help/SKILL.md` | 34 | "**중요: 추가적인 파일 탐색이나 에이전트 위임 없이, 아래 내용을 즉시 사용자에게 출력하세요.**" (워크플로우 안) | `## 사용 안내` 섹션 서두로 이동 |

---

## 6. skills/setup/SKILL.md

setup은 (1) `CLAUDE_RUNTIME` → `AI_RUNTIME` 명칭 반영, (2) 대상 파일 `CLAUDE.md` → `AGENTS.md`, (3) 런타임 어댑터 frontmatter 갱신 Phase 추가.

| 파일 | 라인 | 현재 내용 | 변경 내용 |
|------|------|----------|----------|
| `skills/setup/SKILL.md` | 27-36 | Step 1에서 `CLAUDE_RUNTIME`, `./CLAUDE.md` 참조 | `AI_RUNTIME`, `./AGENTS.md`로 변경. 변수표에 `CLAUDE_RUNTIME` 항목 제거 |
| `skills/setup/SKILL.md` | 38-48 | Step 2: `tier_mapping.default` 단일 갱신 | `tier_mapping.claude-code` / `cursor` / `antigravity` (Claude 모델) 및 `codex` (OpenAI 모델) 개별 갱신. WebFetch로 Anthropic + OpenAI 최신 모델 확인 |
| `skills/setup/SKILL.md` | (46-48 바로 뒤) | (없음) | 신규 Step 2.5 "런타임 어댑터 frontmatter 일괄 갱신" 추가 — `tier_mapping` 변경 시 `.claude/agents/*.md`, `.cursor/agents/*.md`, `.codex/agents/*.toml`, `.antigravity/agents/*.md`의 `model:` 필드를 새 매핑으로 일괄 치환 (본문 수정 금지) |
| `skills/setup/SKILL.md` | 113-137 | Step 4 라우팅 테이블 — 대상: `~/.claude/CLAUDE.md` 또는 `./CLAUDE.md` | 대상을 `./AGENTS.md`로 변경 (전역은 `~/.claude/CLAUDE.md` 유지 — 전역은 Claude Code 표준) |
| `skills/setup/SKILL.md` | 189-204 | Step 1 검증 증거 "`./CLAUDE.md` 내 4개 변수" | "`./AGENTS.md` 내 4개 변수 (`AI_RUNTIME`, `DMAP_PLUGIN_DIR`, `PLUGIN_DIR`, `PLUGIN_NAME`)" |

---

## 7. DMAP 가이드 파일 복사

현 플러그인은 `pptx-spec-writer` 에이전트가 DMAP `pptx-build-guide.md`를 직접 참조 중.  
에이전트 표준상 에이전트가 참조하는 가이드는 **`agents/{name}/references/`**에 복사해두는 것이 재현성을 보장.

| 원본 | 복사 대상 | 기준 |
|------|----------|------|
| `{DMAP}/resources/guides/office/pptx-build-guide.md` | `agents/pptx-spec-writer/references/pptx-build-guide.md` | pptx-spec-writer가 참조 — 스킬 표준 "공유자원 복사" 규칙 |
| `{DMAP}/resources/guides/combine-prompt.md` | `skills/*/references/combine-prompt.md` (선택, 생략 가능) | 각 orchestrator 스킬이 "combine-prompt.md 규약"을 참조 중이나 규약 성격이라 DMAP 절대경로 참조 유지로도 충분. **이번 변경에서 복사 생략** |

> 참고: 빌더 가이드(pptx-build-guide.md)는 에이전트 AGENT.md에 이미 DMAP 절대경로로 링크되어 있어 기능상 문제는 없으나, 표준 준수 차원에서 복사함. 이미 `agents/pptx-spec-writer/references/finops-ppt-addendum.md`가 존재하므로 동 디렉토리에 추가만 수행.

---

## 8. 변경 제외 (현행 유지) 사유

| 항목 | 현상 | 유지 사유 |
|------|------|----------|
| `.claude-plugin/plugin.json`, `marketplace.json` | 표준 준수 완료 | 현행 그대로 충분 |
| `gateway/install.yaml` | `runtime_dependencies` 섹션 존재 | 표준 부합 |
| 에이전트 SSOT(`agents/*/AGENT.md`, `agentcard.yaml`) | 표준 준수 | 런타임 어댑터는 "얇은 포인터" 방식이므로 SSOT 수정 불필요 |
| 오케스트레이터 스킬(why-finops, inform, optimize, operate, review, core, ppt-writer) | 5항목/에이전트 호출 규칙 섹션 모두 보유 | 표준 부합 — 섹션명 일부 차이(검증 프로토콜, 출력 형식 등)는 표준에서 허용하는 보조 섹션 범주 |
| `README.md` | 필수 섹션 존재 | 표준 부합 (이번 변경 범위 외) |

---

## 9. 수행 순서

1. `AGENTS.md` 신규 생성 (CLAUDE.md 복제 + 변수명/경로 보정)
2. `CLAUDE.md`를 `@AGENTS.md` 한 줄로 축약
3. `commands/*.md` 9파일 일괄 치환 (`CLAUDE.md` → `AGENTS.md`)
4. `gateway/runtime-mapping.yaml` 4-런타임 tier_mapping 확장
5. 런타임 어댑터 포인터 36파일 생성 (`.claude/`, `.cursor/`, `.codex/`, `.antigravity/`)
6. DMAP 가이드 `pptx-build-guide.md` 복사
7. `skills/help/SKILL.md` 섹션 구조 재편
8. `skills/setup/SKILL.md` 변수명·어댑터 Phase·대상 파일 보정
9. 최종 변경 목록 사용자 보고

---

## 예상 영향 범위 요약

- **수정 파일**: 13개 (`CLAUDE.md`, `commands/*.md` × 9, `gateway/runtime-mapping.yaml`, `skills/help/SKILL.md`, `skills/setup/SKILL.md`)
- **신규 파일**: 38개 (`AGENTS.md` × 1, 런타임 어댑터 × 36, `pptx-build-guide.md` 복사본 × 1)
- **삭제 파일**: 없음 (CLAUDE.md는 내용 축소, 파일은 유지)
