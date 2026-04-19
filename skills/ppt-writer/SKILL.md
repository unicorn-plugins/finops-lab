---
name: ppt-writer
description: "PPT Deck 작성 + 실제 .pptx 제작 — 산출물 선별 → Marp deck md → anthropic-skills:pptx로 .pptx 빌드 (post-hoc)"
type: orchestrator
user-invocable: true
---

# PPT-Writer

[PPT_WRITER 활성화]

## 목표

FinOps 파이프라인 산출물을 선별하여 Marp deck md를 작성하고, `anthropic-skills:pptx`를 통해 실제 `.pptx` 바이너리 파일을 생성함. 교육용·발표용 고품질 PowerPoint 덱을 자동으로 산출함.

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@ppt-writer` 멘션
- "PPT deck", "발표자료", "PPT 스크립트" 키워드 포함
- `/finops:ppt-writer` 직접 호출

## 에이전트 호출 규칙

### FQN 테이블

| 에이전트/스킬 | FQN | 티어 |
|---|---|---|
| ppt-writer | `finops:ppt-writer:ppt-writer` | MEDIUM |
| pptx 빌드 스킬 | `anthropic-skills:pptx` | 외부 스킬 |

### 프롬프트 조립 지시 (Agent 위임)

호출 전 다음 순서로 프롬프트를 조립함 (combine-prompt.md 규약):
1. `agents/ppt-writer/AGENT.md` 전문 로드
2. `agents/ppt-writer/agentcard.yaml` 역량·제약·핸드오프 섹션 로드
3. Phase 1/2 TASK·EXPECTED OUTCOME·MUST DO·MUST NOT DO·CONTEXT를 조합하여 단일 프롬프트 완성

### 호출 (Agent)

```
Agent(
  subagent_type="finops:ppt-writer:ppt-writer",
  model=MEDIUM 티어 모델,
  prompt=조립된 프롬프트
)
```

### 호출 (Skill→Skill 위임)

```
Skill(
  skill="anthropic-skills:pptx",
  args={...}
)
```

## 워크플로우

### Phase 0: 선행 확인 & 이미지 모드 문의 (`ulw` 활용)

다음 항목을 순서대로 확인함:
- `out/` 디렉토리에 PPT 선별 가능한 산출물 최소 2종 존재 확인
  - 미존재 시 `/finops:core` 선행 실행 안내 후 중단
- `gateway/tools/.env` 존재 여부 확인 → `GEMINI_API_KEY` 유효 여부 간단 체크

AskUserQuestion으로 이미지 포함 여부를 질의함:
- "이미지 포함 (Gemini 호출)" — `GEMINI_API_KEY` 존재 시에만 선택지 제공
- "텍스트만 (이미지 스킵)" — 항상 제공

### Phase 1: 대상 선별 & 이미지 생성 → Agent: ppt-writer (`/oh-my-claudecode:ralph` 활용)

→ Agent: ppt-writer

- **TASK**: `artifact-selector` sub_role로 PPT 적합 산출물을 선별하고, 이미지 모드인 경우 `image-renderer` sub_role로 교육용 일러스트 이미지를 생성함
- **EXPECTED OUTCOME**:
  - `out/ppt-scripts/index.md` — 선별 대상 목록 + 선정 근거 + 예상 슬라이드 수
  - (이미지 모드 시) `out/ppt-scripts/images/*.png` — 각 산출물 대응 교육용 일러스트
  - (이미지 모드 시) `out/ppt-scripts/images/index.md` — 이미지 목록 + 각 사용 위치
- **MUST DO**:
  - 교육용 일러스트 스타일(흰 배경·깔끔한 선·전문적·텍스트 최소) 준수
  - 이미지 스킵 모드 선택 시 `out/ppt-scripts/index.md`에 "이미지 모드: 스킵" 명기
  - 선별 기준(중요도·시각화 적합성·슬라이드 밀도) 근거 기술
- **MUST NOT DO**:
  - Marp deck md 작성 금지 (Phase 2 전담)
  - 이미지 생성 시 저작권·개인정보 포함 요소 삽입 금지
- **CONTEXT**:
  - `out/*` 하위 전체 산출물
  - `agents/ppt-writer/references/ppt-guide.md`

### Phase 2: Marp deck md 작성 → Agent: ppt-writer (`/oh-my-claudecode:ralph` 활용)

→ Agent: ppt-writer

- **TASK**: `slide-designer` sub_role로 Phase 1에서 선별된 각 대상에 대해 Marp deck md를 작성함
- **EXPECTED OUTCOME**:
  - `out/ppt-scripts/{대상}-deck.md` (선별 대상 수만큼, 각 10~20슬라이드)
    - 구조: 표지 / 목차 / 본문 / 요약 섹션 포함
    - DMAP ppt-guide 준수 `style:` frontmatter CSS 포함
    - 이미지 모드 시 `images/*.png` 상대 경로 임베딩
    - 발표자 노트 HTML 주석(`<!-- -->`) 포함
- **MUST DO**:
  - 최소 12pt 폰트, 1152×648pt 슬라이드 크기, Pretendard 폰트 지정
  - 컬러 팔레트 HEX(`#2C2926`, `#059669`, `#0D9488`, `#505060`)를 `style` frontmatter CSS로 기술
  - `---` 구분자로 슬라이드 경계 명확히 표시
  - 각 슬라이드에 발표자 노트(HTML 주석) 작성
- **MUST NOT DO**:
  - 직접 `.pptx` 빌드 시도 금지 (Phase 3 스킬 담당)
  - 12pt 미만 폰트 사용 금지
  - 이미지 모드 스킵 시 `images/` 경로 참조 금지
- **CONTEXT**:
  - Phase 1 산출물 (`out/ppt-scripts/index.md`, `out/ppt-scripts/images/`)
  - `agents/ppt-writer/references/ppt-guide.md`

### Phase 3: .pptx 빌드 → Skill: anthropic-skills:pptx (Skill→Skill 위임, deck별 반복)

→ Skill: anthropic-skills:pptx

Phase 2에서 생성된 Marp deck md 목록을 루프 돌며 각각 위임함.

- **INTENT**: Phase 2에서 생성된 Marp deck md를 PowerPoint 바이너리(`.pptx`)로 변환. DMAP ppt-guide 스타일(최소 12pt, 1152×648, Pretendard, 컬러 팔레트)을 반영하여 생성
- **ARGS**:
  ```json
  {
    "source_plugin": "finops",
    "source_deck_path": "out/ppt-scripts/{대상}-deck.md",
    "output_pptx_path": "out/ppt-scripts/{대상}-deck.pptx",
    "style_spec": "Marp frontmatter의 style 블록 준수 — 최소 12pt, Pretendard, 1152×648pt, 컬러 팔레트(#2C2926·#059669·#0D9488·#505060), 이미지는 images/ 상대 경로 사용"
  }
  ```
- **RETURN**: 각 deck의 `.pptx` 파일이 `output_pptx_path`에 존재. 슬라이드 수가 deck md의 `---` 구분 수와 일치

### Phase 4: 자가 검증 & 사용자 보고 (`/oh-my-claudecode:verify` 활용)

다음 항목을 순서대로 검증함:
- [ ] 각 `{대상}-deck.pptx` 파일 존재 확인
- [ ] 각 `.pptx` 파일 크기 > 10KB (빈 파일 아님) 확인 (Glob으로 파일 크기 확인)
- [ ] 슬라이드 수가 deck md의 `---` 구분 수와 일치하는지 확인 (텍스트 역추출 가능 시)
- [ ] 생성 실패 deck 발견 시 재시도 또는 사용자에게 원인 보고

완료 시 생성된 `.pptx` 파일 목록과 경로를 사용자에게 안내함.

## 완료 조건

- [ ] 대상 선별 결과 (`out/ppt-scripts/index.md`) 존재
- [ ] Marp deck md 다수 생성 (선별 대상 수만큼)
- [ ] 동일 수의 `.pptx` 파일 생성
- [ ] 이미지 모드 시 `out/ppt-scripts/images/` 디렉토리 및 `index.md` 존재
- [ ] 각 `.pptx` 파일 크기 > 10KB (빈 파일 아님)

## 검증 프로토콜

1. ppt-writer AGENT.md의 검증 섹션 체크박스 전항목 통과
2. `out/ppt-scripts/` 디렉토리 내 `index.md` 존재 확인
3. 각 `{대상}-deck.md` 파일에서 `---` 구분자 수 카운트
4. 대응하는 `{대상}-deck.pptx` 존재 및 크기 > 10KB 확인
5. 이미지 모드 시 `images/` 디렉토리 존재 및 `index.md` 포함 확인

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/ppt-scripts/` 경로에 영구 저장됨.

## 취소

`cancelomc` 입력 시 현재 Phase 중단 및 스킬 종료. 이미 생성된 `.pptx` 파일은 보존됨.

## 재개

`out/ppt-scripts/index.md` 존재 여부로 Phase 1 완료를 판단함. 각 `{대상}-deck.md` 존재 여부로 Phase 2 완료를 판단함. 각 `{대상}-deck.pptx` 존재 여부로 Phase 3 완료를 판단함.

## 출력 형식

### 사용자 보고 형식 (권장)

```
## PPT-Writer 생성 결과

### 생성된 .pptx 파일
| 파일명 | 슬라이드 수 | 파일 크기 |
|---|---|---|
| out/ppt-scripts/{대상1}-deck.pptx | N슬라이드 | NKB |
| out/ppt-scripts/{대상2}-deck.pptx | N슬라이드 | NKB |

### 이미지 생성 현황
- 모드: [이미지 포함 | 텍스트만]
- 이미지 수: N개

### 파일 경로
- 선별 결과: out/ppt-scripts/index.md
- 이미지: out/ppt-scripts/images/ (이미지 모드 시)
- Marp deck md: out/ppt-scripts/{대상}-deck.md
- PowerPoint: out/ppt-scripts/{대상}-deck.pptx
```
