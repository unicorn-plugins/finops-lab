# DMAP Office 문서 생성 패턴 정합화 계획서 (finops-lab)

> **목적**: `finops-lab` 플러그인의 PPT 생성 파이프라인을  
> DMAP 표준(`{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md`) **2단계(Spec + Builder) 패턴**에 맞춰 전환함.  
> **현재**: 단일 `ppt-writer` 에이전트가 Marp deck md 작성 → `anthropic-skills:pptx`에 Skill→Skill 위임.  
> **목표**: `pptx-spec-writer` 에이전트(명세 작성) + `skills/ppt-writer` 오케스트레이터가 `pptxgenjs`로 `build.js` 직접 실행.  
> **전제**: 본 전환은 **PPT 전용**. finops-lab에는 docx 생성 파이프라인이 없으므로 **범위 외**로 명시.

---

## 1. 배경 · 차이 요약

| 구분 | 현행 (finops-lab) | DMAP 표준 | 갭 |
|------|--------------------|-----------|----|
| 구조 | 단일 `ppt-writer` 에이전트 + 3 sub_roles(artifact-selector, image-renderer, slide-designer) | `pptx-spec-writer` 에이전트(명세만) + Builder Skill(pptxgenjs 직접 실행) | 에이전트 책임 축소·spec 단계 명시화 |
| 산출 형식 | Marp deck md(`{대상}-deck.md`) + frontmatter CSS style | `ppt-spec.md` (패턴 A~F 매핑, 슬라이드별 콘텐츠·시각요소·발표자 노트) | 산출 형식 근본 교체 |
| PPT 빌드 | `anthropic-skills:pptx` Skill→Skill 위임 | 오케스트레이터가 `pptxgenjs` `build.js`를 **직접 작성·실행** | 외부 스킬 제거·Node 런타임 의존 |
| 입력 구조 | N 산출물(why/maturity/optimize/operate/review 등) → N deck | 동일 (루프 유지) | 루프는 orchestrator가 수행 |
| 런타임 의존성 | `custom_tools.generate_image` (Python + Gemini)만 | + `pptxgenjs` (Node.js ≥18) 필수 | `runtime_dependencies` 섹션 신설 |
| 디자인 가이드 | `agents/ppt-writer/references/ppt-guide.md` (로컬 복제본) | `{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md` (유일 기준) | DMAP 가이드 상속 + 도메인 addendum 분리 |
| 검증 | `.pptx` 크기 > 10KB + `---` 개수 일치 | + PPT 6절 11항 자가 검증 (fs12, defineLayout, addTable, Pretendard 등) | 검증 규칙 강화 |

---

## 2. 아키텍처 전환 Before → After

```
[Before]
out/{artifact1,artifact2,...}.md  (N 산출물)
   ↓
skills/ppt-writer
 ├─ Phase 0: 이미지 모드 확인
 ├─ Phase 1: agents/ppt-writer(artifact-selector + image-renderer)
 │          → out/ppt-scripts/index.md + images/*.png
 ├─ Phase 2: agents/ppt-writer(slide-designer)
 │          → out/ppt-scripts/{대상}-deck.md  (Marp, N개)
 ├─ Phase 3: anthropic-skills:pptx (Skill→Skill)
 │          → out/ppt-scripts/{대상}-deck.pptx  (N개)
 └─ Phase 4: 자가 검증


[After]
out/{artifact1,artifact2,...}.md
   ↓
skills/ppt-writer  (orchestrator)
 ├─ Phase 0: 이미지 모드 확인 + pptxgenjs 설치 확인
 ├─ Phase 1: orchestrator 직접 수행
 │          - artifact 선별 (Read·Glob)  → out/ppt-scripts/index.md
 │          - 이미지 모드 시 generate_image 직접 호출 → out/ppt-scripts/images/*.png
 ├─ Phase 2: agents/pptx-spec-writer (루프, N회)
 │          → out/ppt-scripts/{대상}-spec.md  (패턴 A~F 명세, N개)
 ├─ Phase 3: orchestrator 직접 수행 (루프, N회)
 │          - DMAP pptx-build-guide.md 필독 + finops-ppt-addendum.md 필독
 │          - Write → out/ppt-scripts/{대상}-build.js
 │          - Bash → node {대상}-build.js
 │          → out/ppt-scripts/{대상}-deck.pptx
 └─ Phase 4: 자가 검증 (11항 + 루프별 결과 집계)
```

---

## 3. 결정 필요 사항 (플랜 착수 전 사용자 확정)

### D1. ppt-guide.md 처리 방침 (am-strategy와 동일 구조)
- **옵션 A (권장)**: 기존 `agents/ppt-writer/references/ppt-guide.md`를 **폐기**하고  
  `{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md`를 **유일 기준**.  
  장점: DMAP 정합성 · 중복 제거.
- **옵션 B (차선)**: DMAP 가이드 + `agents/pptx-spec-writer/references/finops-ppt-addendum.md`  
  (FinOps 도메인 특화 규칙 — 교육용 일러스트 스타일, KPI 카드, Maturity Matrix, 3 시나리오 컬러 등).
- **옵션 C**: 기존 로컬 가이드만 사용 — DMAP 정합성 낮음.
- **디폴트 제안**: **B** — DMAP 준수 + FinOps 특화(교육·경영진 소통) 보존.

### D2. Marp deck md 산출 방식
- **옵션 1 (권장)**: Marp deck md **폐기**. `pptx-spec-writer`가 `ppt-spec.md`만 생성. 빌더가 spec→pptxgenjs 직접 변환.  
  사유: Marp+spec 이중 관리 시 drift 위험 (advisor 지적).
- **옵션 2**: Marp deck md도 참고용으로 병행 생성 (중간 산출물로 보관, 빌더는 사용 안 함).  
  단점: 혼동 증가.

### D3. 에이전트 이름·역할 처리
- **옵션 α (권장)**: `agents/ppt-writer` → `agents/pptx-spec-writer`로 **개명**. sub_roles 3 → 1 축소(slide-designer만 남김, artifact-selector/image-renderer는 orchestrator로 이관).
- **옵션 β**: 이름 `ppt-writer` 유지, sub_roles만 축소.  
  단점: DMAP 표준명과 불일치.

### D4. 다중 deck 명세 산출 구조
- **옵션 ⅰ (권장)**: 산출물당 1 spec 파일 (`out/ppt-scripts/{대상}-spec.md`) — 병렬 처리 용이, 재빌드 독립.
- **옵션 ⅱ**: 단일 통합 spec (`out/ppt-scripts/spec.md` + 섹션 구분) — 관리 일원화되나 부분 재빌드 복잡.

### D5. 스킬 이름
- 현재: `skills/ppt-writer` (유지 권장) — 사용자 진입점 변화 없음.  
- 에이전트 FQN만 변경 (`finops:ppt-writer:ppt-writer` → `finops:pptx-spec-writer:pptx-spec-writer`).

### D6. 범위
- **DOCX 빌더 추가 제안**: 현재 finops-lab에 docx 생성이 없음. 필요 시점에 별도 요청으로 도입 권장.  
- **이번 마이그레이션은 PPT 전용** 명시.

---

## 4. 변경 작업 목록

### 4.1 신규 · 개명 · 삭제

| # | 경로 | 작업 | 근거 |
|---|------|------|------|
| T1 | `agents/pptx-spec-writer/AGENT.md` | **신규** (DMAP 템플릿 + FinOps 도메인 섹션) | DMAP 2단계 패턴 Phase 2 |
| T2 | `agents/pptx-spec-writer/agentcard.yaml` | **신규** (tier: MEDIUM, sub_roles = slide-designer 단일) | 명세 작성 품질 확보 |
| T3 | `agents/pptx-spec-writer/tools.yaml` | **신규** (`file_read`·`file_write`만 — 실행 도구 없음) | 에이전트는 명세만 산출 |
| T4 | `agents/pptx-spec-writer/references/finops-ppt-addendum.md` | **신규** (D1-B 선택 시) | FinOps 도메인 특화 규칙 |
| T5 | `agents/ppt-writer/*` | **삭제 또는 개명**(D3) | 역할 소멸 |
| T6 | `agents/ppt-writer/references/ppt-guide.md` | D1 확정에 따라 처리 (폐기/addendum 추출) | — |

### 4.2 skills/ppt-writer 재설계

| # | 변경점 | 상세 |
|---|-------|------|
| S1 | `type`/`description` 갱신 | "Marp deck + anthropic-skills:pptx" → "DMAP 2단계 spec + pptxgenjs 직접 빌드" |
| S2 | Phase 0 보강 | 기존: 이미지 모드 + API Key 확인. 신규: **pptxgenjs 설치 확인**(`node -e "require('pptxgenjs')"`) 추가. 미설치 시 `/finops:setup` 재실행 안내. |
| S3 | Phase 1 단순화 | artifact 선별 + (선택) 이미지 생성을 **orchestrator가 직접 수행**. agents/ppt-writer 위임 제거. |
| S4 | Phase 2 위임 대상 변경 | `finops:pptx-spec-writer:pptx-spec-writer`에 **산출물별 루프 위임** (N회). 각 호출 → `{대상}-spec.md`. |
| S5 | Phase 3 재설계 | **오케스트레이터 직접 수행**. 루프별로: DMAP pptx-build-guide 필독 → `{대상}-build.js` Write → `node {대상}-build.js` 실행 → `{대상}-deck.pptx` 생성. 실패 시 최대 3회 재빌드. |
| S6 | Phase 4 검증 강화 | 기존(파일 존재·크기·`---` 개수) + PPT 6절 **11항 자가 검증**(fs12, defineLayout, addTable, Pretendard, 이미지 존재 등). |
| S7 | MUST/MUST NOT 업데이트 | `anthropic-skills:pptx` 위임 → **금지로 반전**. pptxgenjs 직접 실행을 강제. |

### 4.3 gateway/install.yaml

```yaml
# 기존 custom_tools 유지 (generate_image)
# 신규 섹션 추가:
runtime_dependencies:
  - name: pptxgenjs
    description: "PPT 빌드용 Node.js 라이브러리 — skills/ppt-writer가 build.js 직접 실행"
    runtime: node                             # 사전 요구: node ≥ 18
    install: "npm install pptxgenjs"
    check: "node -e \"require('pptxgenjs')\""
    required: true
```

**주의**: am-strategy 마이그레이션에서 확인된 함정 회피  
→ pptxgenjs는 **플러그인 루트**(`finops-lab/node_modules/`)에 설치할 것.  
Node 모듈 해석 경로가 `out/ppt-scripts/{대상}-build.js`에서 시작해 상위로 탐색하므로  
`out/ → finops-lab/node_modules` 순으로 해석 성공.  
`gateway/`는 `out/`과 형제라 해석 경로에 포함되지 않음.

### 4.4 gateway/runtime-mapping.yaml

- `ppt-writer` 키(암묵적 default 사용 중) → `pptx-spec-writer` 키 신설.  
- tier: **MEDIUM** 유지 (`claude-sonnet-4-6`).  
- tool_mapping: 변경 없음.

### 4.5 skills/setup/SKILL.md

| Step | 변경 |
|------|------|
| Step 2 (모델 최신화) | 변경 없음 |
| Step 3 (generate_image 설치) | 현재 Python만 → **Node 의존성 추가**. `install.yaml`의 `runtime_dependencies` 엔트리(`pptxgenjs`)를 `check → install` 루프로 검증·설치. |
| Step 3-2 신설 | Node.js 18+ 사전 확인 → `npm install pptxgenjs`를 **플러그인 루트**에 설치. |
| Step 3-3 신설 | 설치 검증: `cd out && node -e "require('pptxgenjs')"` 실행 → 실사용 CWD에서 해석 보장 |
| Step 4 (라우팅) | 변경 없음 |
| 문제 해결 표 | pptxgenjs/Node 관련 항목 추가. |

### 4.6 CLAUDE.md · README.md

- 에이전트 이름 변경 반영(`ppt-writer` → `pptx-spec-writer`)
- 런타임 의존성 섹션에 Node.js 18+ 추가
- `anthropic-skills:pptx` 언급 제거 (없어도 동작)
- 페르소나 "덱메이커 장슬라이드" 배경에 "Anthropic Agent Skills" → "DMAP Office 빌더(pptxgenjs)" 표현 교체

---

## 5. 작업 순서 (권장 시퀀스)

```
[D1 · D2 · D3 · D4 사용자 확정]
      ↓
1. gateway/install.yaml · runtime-mapping.yaml 업데이트
      ↓
2. agents/pptx-spec-writer 신규 생성 (AGENT.md / agentcard.yaml / tools.yaml / addendum)
      ↓
3. skills/ppt-writer/SKILL.md 재설계 (Phase 0~4)
      ↓
4. skills/setup/SKILL.md 확장 (Node 의존성 · pptxgenjs 설치 · 검증)
      ↓
5. agents/ppt-writer 제거 (D3 확정 후)
      ↓
6. CLAUDE.md · README.md 업데이트 (에이전트명·런타임·의존성)
      ↓
7. 통합 시뮬레이션: 샘플 out/*.md → build.js 실행 (다중 deck E2E)
      ↓
8. 기존 out/ppt-scripts/*-deck.md (Marp) 처리 결정 (보관/삭제/아카이브)
```

---

## 6. 검증 기준 (완료 판정)

- [ ] `gateway/install.yaml`의 `runtime_dependencies.pptxgenjs` 엔트리 존재
- [ ] `agents/pptx-spec-writer/` 3 파일 + addendum 존재
- [ ] `agents/ppt-writer/` 부재 (또는 개명 완료)
- [ ] `skills/ppt-writer/SKILL.md` 내 `anthropic-skills:pptx` 언급이 **금지 명시**에만 존재 (`grep -c "anthropic-skills:pptx"` = 1~2 라인, 모두 MUST NOT 컨텍스트)
- [ ] 샘플 산출물 1종으로 E2E 실행 시: `{대상}-spec.md` · `{대상}-build.js` · `{대상}-deck.pptx` 3파일 모두 생성 및 크기 > 0
- [ ] PPT 6절 검증 11항 빌드 스크립트 내 helper 구현(fs12, pptx.shapes.*, defineLayout 등)
- [ ] `gateway/runtime-mapping.yaml`에 `pptx-spec-writer` 키 존재

---

## 7. 리스크 · 완화

| 리스크 | 영향 | 완화 |
|-------|-----|-----|
| pptxgenjs 설치 경로 오류 (am-strategy에서 확인) | `/ppt-writer` 런타임 실패 | 플러그인 루트(`finops-lab/`)에 설치. setup Step 3-3에서 `cd out && node -e "require('pptxgenjs')"`로 실사용 CWD 검증 |
| 다중 deck 루프에서 일부 실패 시 부분 성공 처리 | 사용자 혼란 | Phase 3 루프 내 실패 deck은 별도 리스트 집계 + 나머지는 성공 보고. 재빌드는 해당 deck만 |
| 이미지 모드 + API Key 부재 상호작용 변경 | 기존 동작 유지 필요 | Phase 0 분기 보존 (GEMINI_API_KEY 미존재 시 이미지 스킵 옵션만 제공) |
| Marp deck 폐기 시 기존 `out/ppt-scripts/*-deck.md` 소비자 | README/CLAUDE.md 링크 깨짐 | 업데이트 시 파일명 규칙을 `{대상}-spec.md`(중간) / `{대상}-deck.pptx`(최종)로 공지 |
| 다수 build.js 파일 생성 시 산출물 디렉토리 복잡도 증가 | 유지보수 부담 | `out/ppt-scripts/` 내부를 spec/ · build/ · images/ · pptx/ 서브디렉토리로 분리 검토 (옵션) |
| DMAP addendum 분리 시 가이드 drift | 규칙 충돌 | addendum은 **추가 규칙만** 기술 — DMAP 표준을 재정의 금지 (룰 작성 시 MUST 선언) |

---

## 8. 후속 오픈 이슈

- **루프별 generate_image 호출 설계**: 산출물당 1~3개 일러스트가 필요할 때 Phase 1에서 일괄 생성할지, Phase 2에서 spec 작성 중 필요 시점에 요청할지 재검토.
- **다중 deck 병렬 빌드**: Node 서브프로세스 병렬 실행으로 총 빌드 시간 단축 여부 (예: `Promise.all`로 5개 deck 동시 빌드).
- **ppt-writer 스킬명 유지 vs 개명**: 사용자 진입점은 유지(D5) 권장이나 에이전트와 네이밍 괴리 발생 가능. 장기적으로 `skills/generate-pptx` 이관 검토.
- **차트 생성 전략**: Maturity Radar, 3 시나리오 누적 곡선 등을 pptxgenjs `addChart`로 네이티브 차트로 그릴지, `generate_image` PNG로 대체할지 Phase 3에서 결정.
