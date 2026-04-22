---
name: ppt-writer
description: "DMAP 표준 2단계 PPT 빌드 오케스트레이션 — N 산출물을 pptx-spec-writer로 명세 작성 후 pptxgenjs build.js를 직접 실행하여 각 .pptx 생성 (다중 deck 루프)"
type: orchestrator
user-invocable: true
---

# PPT-Writer

[PPT_WRITER 활성화]

## 목표

FinOps 파이프라인 산출물을 선별하여 **DMAP 표준 2단계 PPT 빌드 패턴**으로 다중 `.pptx`를 생성함:
- **Phase 1**: orchestrator가 직접 산출물 선별 + (선택) 이미지 생성
- **Phase 2**: `pptx-spec-writer` 에이전트가 산출물당 1 `spec.md` 작성 (N회 루프)
- **Phase 3**: orchestrator가 `pptxgenjs`로 `build.js`를 직접 작성·실행 (N회 루프, 각 deck.pptx 생성)
- **Phase 4**: 자가 검증 + 사용자 보고

**DMAP 표준 Office 빌드 패턴 준수**:
- PPT: 2단계(Spec Agent + Orchestrator Builder) — `{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md`
- 외부 변환 스킬(`anthropic-skills:pptx` 등) **의존 제거**
- Marp deck md 산출 **폐기** — `spec.md`가 유일한 중간 산출물

## 활성화 조건

다음 중 하나 이상 해당 시 활성화됨:
- `@ppt-writer` 멘션
- "PPT deck", "발표자료", "PPT 스크립트" 키워드 포함
- `/finops:ppt-writer` 직접 호출

## 에이전트 호출 규칙

### 에이전트 FQN

| 에이전트 | FQN | 티어 | 담당 |
|----------|-----|------|------|
| pptx-spec-writer | `finops:pptx-spec-writer:pptx-spec-writer` | MEDIUM | Phase 2 (산출물당 1 spec 작성, N회 루프) |

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

### PPT 빌드는 위임 없이 오케스트레이터가 직접 수행

- DMAP 2단계 패턴 Phase 3은 orchestrator가 pptxgenjs `build.js`를 Write + Bash로 직접 작성·실행
- `anthropic-skills:pptx`에 Skill→Skill 위임 **금지**
- spec.md → build.js 변환 로직은 본 스킬이 DMAP pptx-build-guide.md 6절 11항을 필독 후 직접 작성

## 워크플로우

### Phase 0: 선행 확인 & 옵션 수집 (`ulw` 활용)

다음 항목을 순서대로 확인:
- `out/` 디렉토리에 PPT 선별 가능한 산출물 **최소 2종 존재** 확인
  - 미존재 시 `/finops:core` 선행 실행 안내 후 중단
- `gateway/tools/.env` 존재 여부 확인 → `GEMINI_API_KEY` 유효성 체크
- **`pptxgenjs` 설치 확인**: Bash `cd out && node -e "require('pptxgenjs')"` 실행
  - 실패 시 `/finops:setup` 재실행 안내 후 중단 (runtime_dependencies 설치 필요)

AskUserQuestion으로 이미지 포함 여부를 질의:
- "이미지 포함 (Gemini 호출)" — `GEMINI_API_KEY` 존재 시에만 선택지 제공
- "텍스트만 (이미지 스킵)" — 항상 제공

### Phase 1: 산출물 선별 + (선택) 이미지 생성 (오케스트레이터 직접 수행 — `ulw` 활용)

**외부 에이전트 위임 없이 orchestrator가 직접 수행**:

1. **산출물 선별**: Read + Glob로 `out/**/*.md` 스캔
   - 평가 후보: `why-statement`, `maturity-diagnosis`, `rightsize-plan`, `commit-strategy`,
     `review-runbook`, `maturity-transition`, `review-report` 등
   - 선정 기준: 경영진·의사결정·교육 관점 중요도, 시각화 적합성, 슬라이드 밀도
   - **선별 결과**를 `out/ppt-scripts/index.md`에 저장 — 대상 목록 + 선정 근거 + 예상 슬라이드 수
2. **이미지 생성 (이미지 모드 시)**: `generate_image` 커스텀 도구 직접 호출
   - 각 산출물 핵심 개념에 대해 `finops-ppt-addendum.md §6`의 파일명 규칙 준수
   - 교육용 일러스트 스타일(§7) 프롬프트 적용
   - 산출: `out/ppt-scripts/images/{finops_*}.png` + `out/ppt-scripts/images/index.md` (이미지↔슬라이드 매핑)
3. **이미지 스킵 모드**: `out/ppt-scripts/index.md`에 "이미지 모드: 스킵" 명기

### Phase 2: Spec 작성 → Agent: pptx-spec-writer (산출물당 1회 루프, `ulw` 활용)

Phase 1에서 선별된 산출물 N건 각각에 대해 pptx-spec-writer 에이전트에 **루프 위임**:

- **TASK**: 산출물 1건을 분석하여 PPT 시각 명세(`{대상}-spec.md`) 작성
- **EXPECTED OUTCOME**: `out/ppt-scripts/{대상}-spec.md` (패턴 A~F 매핑 + 이미지 참조)
- **MUST DO**:
  - `{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md` 1~5절 필독
  - `{PLUGIN_DIR}/agents/pptx-spec-writer/references/finops-ppt-addendum.md` 필독 (산출물별 표준 흐름 §1)
  - 슬라이드당 본문 ≤7줄, 이미지는 `![설명](images/파일명.png)` 형식
  - 모든 수치에 범위·출처 명시 (addendum §3·§4)
- **MUST NOT DO**: 실제 PPT 파일 생성 금지, 컬러·폰트 직접 지정 금지, 단일 숫자 수치 표기 금지
- **CONTEXT (산출물별 다름)**: 해당 `out/{대상}.md` 경로, 이미지 목록, 목표 슬라이드 수, 대상 청중

루프 완료 후 N개 `{대상}-spec.md` 존재 확인.

### Phase 3: PPT 파일 빌드 (오케스트레이터 직접 수행, 산출물당 1회 루프 — `ulw` 활용)

**외부 스킬 위임 없이 orchestrator가 직접 수행** (산출물 N건 각각):

1. **가이드 로드** (루프 외부, 1회만): `{DMAP_PLUGIN_DIR}/resources/guides/office/pptx-build-guide.md` 전체 읽기
   (특히 6절 "코드 생성 시 필수 검증 규칙" 11항 모두 준수)
2. **각 산출물에 대해** (루프):
   a. `out/ppt-scripts/{대상}-spec.md` 읽고 슬라이드별 패턴(A~F) 매핑
   b. **빌드 코드 작성**: Write 도구로 `out/ppt-scripts/{대상}-build.js` 생성
      - pptxgenjs 사용
      - **반드시 가이드 6절 전체 규칙 준수**:
        - `pptx.shapes.RECTANGLE`/`ROUNDED_RECTANGLE` 사용 (`ShapeType` 금지)
        - `defineLayout({name:"CUSTOM", width:16, height:9})`
        - `async function createSlideXX(pptx)` 패턴
        - `slide.addTable()` 사용 (수동 셀 그리기 금지)
        - `fs12()` 헬퍼로 12pt 미만 폰트 차단
        - 이미지 임베딩 전 경로·크기 검증
        - Pretendard 폰트 통일
        - `main().catch(e => { console.error(...); process.exit(1); })` 진입점
   c. **빌드 실행**: Bash로 `cd out/ppt-scripts && node {대상}-build.js` 실행
      → `out/ppt-scripts/{대상}-deck.pptx` 생성
      - 전제: `pptxgenjs`가 **플러그인 루트**(`finops-lab/node_modules/`)에 설치됨
        (Node 해석 경로: `out/ppt-scripts → out → finops-lab/node_modules` ✓)
      - `Cannot find module 'pptxgenjs'` 발생 시 `/finops:setup` 재실행하여 플러그인 루트에 설치
   d. **검증 A — 빌드 확인**:
      - 빌드 종료 코드 0 확인
      - `.pptx` 파일 존재 및 0바이트 초과 확인
      - 자가 검증 체크리스트 11항 통과
      - 실패 시 에러 분석 → 코드 수정 → 재실행 (해당 deck만 최대 3회)
   e. **검증 B — PowerShell COM 시각적 검토**:
      - 아래 PS1 템플릿으로 `.temp/export-{대상}.ps1`을 생성 후 슬라이드별 PNG 추출
      ```powershell
      $pptxPath = '<절대경로\{대상}-deck.pptx>'
      $outDir   = '<절대경로\preview\{대상}>'
      if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }
      Add-Type -AssemblyName Microsoft.Office.Interop.PowerPoint
      $ppt  = New-Object -ComObject PowerPoint.Application
      $pres = $ppt.Presentations.Open($pptxPath, 0, 0, 0)
      foreach ($i in 1..$pres.Slides.Count) {
          $pres.Slides.Item($i).Export("$outDir\slide-$i.png", 'PNG', 1600, 900)
      }
      $pres.Close(); $ppt.Quit()
      ```
      - PowerShell 실행 전 `Get-Process POWERPNT -ErrorAction SilentlyContinue | Stop-Process -Force`로 파일 잠금 해제
      - 추출된 PNG를 Read 도구로 열어 레이아웃·이미지 비율·텍스트 잘림 시각 확인
      - 이상 발견 시 `{대상}-build.js` 수정 → 재빌드 → 재검토 (최대 2회)
      - **기존 이미지 파일(`images/` 폴더)은 절대 삭제하지 말 것 — 레이아웃·크기만 조정**
      - 시각 검토 완료 후 임시 파일 정리: `Remove-Item '<preview경로>\*.png' -Force; Remove-Item '.temp\export-{대상}.ps1' -Force`
3. **루프 집계**: 성공 deck / 실패 deck을 리스트로 분리 수집

### Phase 4: 자가 검증 & 사용자 보고 (`/oh-my-claudecode:verify` 활용)

루프 전체에 대해 다음 항목을 검증:
- [ ] 각 `{대상}-spec.md` 파일 존재 (Phase 2 결과)
- [ ] 각 `{대상}-build.js` 파일 존재 (Phase 3 결과)
- [ ] 각 `{대상}-deck.pptx` 파일 존재 및 크기 > 10KB
- [ ] 슬라이드 수가 spec md의 `## 슬라이드 N:` 항목 수와 일치
- [ ] 이미지 모드 시 `images/*.png` 파일이 실제 존재 (참조된 항목)
- [ ] 빌드 실패 deck 리스트 비어있음 (또는 사용자에게 원인 보고)

완료 시 생성된 `.pptx` 파일 목록·경로·크기·슬라이드 수를 표로 안내.

## 완료 조건

- [ ] 선별 결과(`out/ppt-scripts/index.md`) 존재
- [ ] N개 `{대상}-spec.md` 생성 (Phase 2)
- [ ] N개 `{대상}-build.js` 생성 (Phase 3)
- [ ] 동일 수의 `{대상}-deck.pptx` 생성 (Phase 3)
- [ ] 이미지 모드 시 `out/ppt-scripts/images/` 디렉토리 및 `index.md` 존재
- [ ] 각 `.pptx` 크기 > 10KB

## 검증 프로토콜

1. ppt-writer SKILL.md의 완료 조건 체크박스 전항목 통과
2. 각 `{대상}-spec.md`의 `## 슬라이드 N:` 매치 수 = 빌드된 `.pptx`의 슬라이드 수
3. 이미지 모드 시 spec.md 내 `![](images/*.png)` 참조 파일 모두 디스크에 존재
4. 빌드 실패 deck은 별도 리스트로 사용자에게 원인과 함께 보고
5. pptxgenjs 미설치 시 graceful failure + `/finops:setup` 안내

## MUST / MUST NOT

**MUST**
- Phase 순차 수행 및 완료 시마다 사용자 보고
- Phase 0에서 pptxgenjs 설치 확인 (`cd out && node -e "require('pptxgenjs')"`)
- Phase 1은 orchestrator가 직접 수행 (artifact 선별 + 이미지 생성)
- Phase 2는 산출물당 1회 pptx-spec-writer 에이전트 위임 (5항목 프롬프트)
- Phase 3는 orchestrator가 직접 `build.js` 작성·실행 (산출물당 1회 루프)
- Phase 3 시작 시 `pptx-build-guide.md` 전체(특히 6절 11항) 필독
- 빌드 스크립트(`{대상}-build.js`)를 산출물로 보존
- 실제 `.pptx` 파일 생성 및 `>10KB` 검증

**MUST NOT**
- `anthropic-skills:pptx` 등 외부 변환 스킬 호출
- `anthropic-skills:pptx`에 Skill→Skill 위임
- pptx-spec-writer 에이전트 우회 (orchestrator가 spec 직접 작성 금지)
- Phase 순서 건너뛰기
- 가이드 미독상태로 `build.js` 작성
- 검증 없이 "생성 완료" 보고
- Marp deck md(`*-deck.md`) 산출 (폐기됨 — spec.md가 유일한 중간 산출물)
- 시각적 검토 후 수정 시 `images/` 폴더의 기존 이미지 파일 삭제 (레이아웃·크기 조정만 허용)

## 상태 정리

임시 상태 파일 미사용. 산출물은 `out/ppt-scripts/` 경로에 영구 저장.
빌드 스크립트(`*-build.js`)도 산출물과 함께 보존 → 재빌드·디버깅 가능.

## 취소

`cancelomc` 입력 시 현재 Phase 중단. 이미 생성된 `.pptx` 파일은 보존.

## 재개

- `out/ppt-scripts/index.md` 존재 → Phase 1 완료 판정
- `{대상}-spec.md` 존재 → Phase 2 해당 deck 완료 판정
- `{대상}-deck.pptx` 존재 → Phase 3 해당 deck 완료 판정
- 실패 deck만 선택 재빌드 가능 (Phase 3만 재실행)

## 출력 형식

### 사용자 보고 형식 (권장)

```
## PPT-Writer 생성 결과 (DMAP 2단계 빌드)

### 성공한 .pptx 파일
| 파일명 | 슬라이드 수 | 파일 크기 | 빌드 스크립트 |
|---|---|---|---|
| out/ppt-scripts/{대상1}-deck.pptx | N | NKB | {대상1}-build.js |
| out/ppt-scripts/{대상2}-deck.pptx | N | NKB | {대상2}-build.js |

### 실패한 deck (있을 경우)
| 대상 | 단계 | 오류 | 조치 |
|---|---|---|---|
| {대상3} | Phase 3 빌드 | ... | 재빌드 또는 spec 수정 |

### 이미지 생성 현황
- 모드: [이미지 포함 | 텍스트만]
- 이미지 수: N개

### 파일 경로
- 선별 결과: out/ppt-scripts/index.md
- 이미지: out/ppt-scripts/images/ (이미지 모드 시)
- Spec md: out/ppt-scripts/{대상}-spec.md
- 빌드 스크립트: out/ppt-scripts/{대상}-build.js
- PowerPoint: out/ppt-scripts/{대상}-deck.pptx
```
