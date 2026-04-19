# finops-lab 개발 계획서

> DMAP 표준 기반 플러그인 개발 계획. Phase 2 산출물.
> 입력: `output/team-plan-finops-lab.md`, `output/requirements.md`
> 참조: DMAP plugin/agent/skill/gateway 표준

---

## 1. 기본 정보

| 항목 | 값 |
|------|-----|
| 플러그인명 | `finops` |
| 마켓플레이스명 | `finops` |
| Owner | `hiondal` |
| Version | `0.0.1` |
| License | MIT |
| 대상 도메인 | 멀티클라우드 FinOps · FinOps for AI · 비용 거버넌스 · 단위경제 · 이상 비용 탐지 |
| 대상 사용자 | FinOps 실무자/팀장, 클라우드 아키텍트, DevOps/SRE, CCoE 준비 조직, 재무·사업부 Cost Owner |
| 목표 | FinOps 교재·2026 프레임워크를 4단계(WHY→Inform→Optimize→Operate) + 최종 Review로 HBT 가상 기업 데이터에 적용해 체득 |

---

## 2. 핵심기능

### 2.1 `@why-finops` (WHY 정의 & 성숙도 진단)
- 비즈니스 이슈 → FinOps 3대 가치(투자가치·비용최적화·문화정착) 매핑
- Ownership×Capability 다차원 성숙도 자가진단 (Crawl/Walk/Run)
- COVERS 6원칙 정렬 + 12개월 스킬셋 로드맵(AI Cost · Tooling · Automation · Forecasting)
- 경영진 보고용 WHY 통합본 1-Pager + 12개월 OKR 초안
- 산출물: `out/step1/1~3-*.md`, `out/why-statement.md`

### 2.2 `@inform` (FOCUS 정규화 & 통합 가시성)
- 3 CSP 빌링(AWS CUR 2.0, Azure Cost Export, GCP Billing) + SaaS LLM(OpenAI/Anthropic) → FOCUS v1.3 정규화
- AI 확장 컬럼 5종 통합: TokenCountInput/Output, ModelName, GpuHours, GpuUtilization
- USD→KRW 환산(×1,500), Amortized 비용 산출
- 태깅 거버넌스 갭 분석 + tag-policy.yaml 런타임 생성
- 이상 비용 5단계 탐지 (CSP 이벤트 3건 + AI 이벤트 2건)
- 단일 파일 웹 대시보드(`out/dashboard.html`, Chart.js 4.x CDN, 9차트, <1.2MB)

### 2.3 `@optimize` (줄이기: Right-sizing · 약정 전략)
- 유휴 리소스 5종 탐지 (미연결 EBS · 유휴 EC2 · 미사용 Disk · 방치 LB · 오래된 스냅샷)
- Right-sizing 3대안 (Downsize-1단/Downsize-2단/Terminate) 절감액·SLA 비교
- AI 특화: GPU 활용률 <60% 탐지 + 모델 다운그레이드 권고(GPT-4o → GPT-4o-mini 등)
- RI/SP/Spot 혼합 Conservative/Base/Optimistic 3시나리오 절감액·BEP·리스크

### 2.4 `@operate` (체계화: KPI · 자동화 · 거버넌스)
- 단위경제 KPI 6종 (CSP 3: 가입자·API·ML / AI 3: 토큰 1M·추론 1K·GPU 시간)
- 자동화 파이프라인 5단계 (탐지→권고→승인→적용→검증) + Shift-Left 훅
- 게이트 기준 6종 (태깅≥95% · MAPE≤10% · RI≥80% · 이상탐지≤24h · 유휴≤3% · GPU≥60%)
- 주/월/분기 리뷰 런북 + Crawl→Walk 12개월 전환 플랜

### 2.5 `@review` (최종 독립 검증)
- WHY-Inform-Optimize-Operate 4단계 정합성 검증
- FOCUS 필수 15종 + AI 확장 5종 커버리지
- COVERS·게이트 규칙 ID 역참조 가능성
- 3시나리오 수치 일관성, Ownership별 전환 실행 가능성

### 2.6 `@ppt-writer` (PPT Deck + 실제 .pptx 제작)
- 전체 산출물 중 **경영진 보고·의사결정·교육 소통용으로 PPT 적합한 문서**를 선별
- 각 대상을 슬라이드 단위 Marp 스크립트(deck md)로 재구성 — **DMAP `ppt-guide.md` 스타일 준수**
- 생성된 deck md를 **Claude 기본 제공 `anthropic-skills:pptx`** 스킬로 Skill→Skill 위임하여 `.pptx` 바이너리 생성
- 외부 의존성(Node.js/Python/npm/.env) **0** — Claude 런타임만으로 완결
- 대상 후보:
  - `out/why-statement.md` → 경영진 1-Pager 브리핑 (12개월 OKR 포함)
  - `out/step1/2-maturity-diagnosis.md` → Ownership×Capability 성숙도 결과
  - `out/rightsize-plan.md` → Right-sizing 3대안 의사결정
  - `out/commit-strategy.md` → RI/SP/Spot 3시나리오 약정 전략
  - `out/review-runbook.md` → 주/월/분기 리뷰 런북 교육
  - `out/step4/4-maturity-transition.md` → Crawl→Walk 12개월 전환 플랜
  - `out/review-report.md` → 최종 검증 보고 요약
- 산출물:
  - `out/ppt-scripts/index.md` (선별 결과 + deck 목록)
  - `out/ppt-scripts/{대상}-deck.md` (Marp 스크립트 — 사람이 읽는 소스)
  - `out/ppt-scripts/{대상}-deck.pptx` (최종 PPT 바이너리 — `anthropic-skills:pptx` 생성)
- **이미지는 MVP 범위 제외** (텍스트·표·발표자 노트 중심). 2차 이터레이션에서 이미지 생성 도구 연계 검토
- **런타임 이식성**: `anthropic-skills:pptx`는 Anthropic 공식 Agent Skills로 Claude Code · CoWork · Claude.ai 전반에서 동일 네임스페이스로 호출 가능

---

## 3. 업무 플로우

### STEP 1. `@why-finops` — WHY 정의 & 성숙도 진단
- Step 1-1. 비즈니스 이슈 → FinOps 동인 매핑 → `out/step1/1-drivers.md`
- Step 1-2. 성숙도 자가진단 (Ownership × Capability) → `out/step1/2-maturity-diagnosis.md`
- Step 1-3. COVERS 원칙 정렬 & 12개월 스킬셋 로드맵 → `out/step1/3-covers-roadmap.md`
- Step 1-4. WHY 통합본 (경영진 보고용) → `out/why-statement.md`

### STEP 2. `@inform` — FOCUS 정규화 & 통합 가시성
- Step 2-1. 원본 빌링 + SaaS LLM 로드 & 스키마 프로파일링 → `out/step2/1-source-profile.md`
- Step 2-2. FOCUS 매핑 YAML 4종 + README 런타임 생성 → `resources/mapping/*.yaml`
- Step 2-3. FOCUS 정규화 병합 (CSP + SaaS LLM + AI 확장) → `out/focus-normalized.csv`
- Step 2-4. 태그 거버넌스 갭 분석 & `tag-policy.yaml` 생성 → `out/step2/4-tag-coverage.md`, `resources/templates/tag-policy.yaml`
- Step 2-5. 이상 비용 탐지 & 웹 대시보드(9차트) → `out/dashboard.html`

### STEP 3. `@optimize` — 줄이기
- Step 3-1. 유휴 리소스 탐지 → `out/step3/1-idle-resources.md`
- Step 3-2. 과잉 프로비저닝 & Right-sizing 3대안 (CSP + AI) → `out/rightsize-plan.md`
- Step 3-3. 스케일링 정책 체크리스트 → `out/step3/3-scaling-policy-checklist.md`
- Step 3-4. 약정 할인 3시나리오 (RI/SP/Spot) → `out/commit-strategy.md`

### STEP 4. `@operate` — 체계화
- Step 4-1. 단위경제 KPI 대시보드 생성 (CSP + AI) → `resources/templates/kpi-dashboard.md`, `out/step4/1-unit-economics.md`
- Step 4-2. 자동화 파이프라인 설계 (5단계) → `out/step4/2-automation-pipeline.md`
- Step 4-3. 게이트 기준 운영화 & 리뷰 런북 → `out/review-runbook.md` (및 `out/step4/3-*`)
- Step 4-4. 성숙도 전환 플랜 (Crawl → Walk) → `out/step4/4-maturity-transition.md`

### STEP 5. `@review` — 최종 검증
- WHY-Inform-Optimize-Operate 정합성 + FOCUS 커버리지 + 규칙 ID 역참조 + Ownership 전환 실현성 → `out/review-report.md`

### STEP 6. `@ppt-writer` — PPT Deck + 실제 제작
- Step 6-1. (Agent) PPT 적합 산출물 선별 → `out/ppt-scripts/index.md`
- Step 6-2. (Agent) 대상별 deck md 작성 (Marp 호환, ppt-guide 스타일 반영) → `out/ppt-scripts/*-deck.md`
- Step 6-3. (Skill→Skill 위임) 각 deck md를 `anthropic-skills:pptx`로 위임하여 `.pptx` 빌드 → `out/ppt-scripts/*-deck.pptx`
- Step 6-4. (Skill) 자가 검증 — `.pptx` 파일 존재·슬라이드 수·텍스트 역추출 대조 → 검증 통과 후 사용자 보고

### `@core` 풀 파이프라인
- `@why-finops → @inform → @optimize → @operate → @review` 순차 실행
- `@ppt-writer`는 **core에서 제외** — 산출물이 확정된 뒤 사용자가 "PPT로 만들 부분"을 선택적으로 실행하는 post-hoc 스킬

---

## 4. 기술 요구사항

### 4.1 기술 스택
- **언어/포맷 (코어 학습 랩)**: Markdown + YAML + CSV + HTML (Chart.js 4.x CDN 인라인)
- **런타임 서버**: 불필요 — 대시보드는 단일 HTML 파일, 브라우저 오프라인 열람
- **PPT 바이너리 생성**: `@ppt-writer` 스킬이 `anthropic-skills:pptx`(Anthropic 공식 Agent Skill)를 Skill→Skill 위임으로 호출 — Node.js/pptxgenjs 등 외부 런타임 불필요
- **이미지 생성 (`@ppt-writer` 슬라이드 일러스트)**: Python + `python-dotenv google-genai` + Gemini Nano Banana (`gateway/tools/generate_image.py`)
- **환경변수 (.env)**: `@ppt-writer` 이미지 생성 시 `GEMINI_API_KEY` 필요 (setup 스킬이 `.env.example` 생성 및 입력 안내)
- **커스텀 도구**: `gateway/tools/generate_image.py` — DMAP 마켓플레이스 복사 (신규 개발 없음)

### 4.2 런타임 티어 매핑 (plugin 생성 시점 최신 버전)

| 티어 | 모델 |
|------|------|
| HEAVY | `claude-opus-4-7` |
| HIGH | `claude-opus-4-7` |
| MEDIUM | `claude-sonnet-4-6` |
| LOW | `claude-haiku-4-5` |

> setup 스킬에서 최신 버전 확인 후 사용자 승인 받아 갱신.

### 4.3 MCP/LSP 서버
- 런타임 빌트인 + OMC 기본 제공 외 **추가 필요 없음**

### 4.4 PPT 디자인 표준 (`@ppt-writer` 전용)
- **준거 문서**: DMAP `{DMAP_PLUGIN_DIR}/resources/guides/docs/ppt-guide.md` (컬러 팔레트 · 타이포 · 레이아웃 · 컴포넌트 스타일 · 디자인 규칙 · 코드 레벨 검증)
- **슬라이드 사양**: 1152 × 648pt (16:9)
- **서체**: Pretendard (Bold/Regular) · 폴백: 맑은 고딕, Arial
- **필수 강제**: 최소 폰트 12pt · 하단 여백 ≤ 1인치 · 테이블 2개 이상 시 좌우/수직 배치 규칙 적용 (Marp deck의 `style:` frontmatter에 CSS로 표현하여 `anthropic-skills:pptx`에 전달)
- **생성 후 자가 검증**: 5종 체크리스트 — 최소 폰트 · 하단 여백 · 콘텐츠 누락(markitdown 역추출 대조) · 이미지 임베딩 · 슬라이드 크기

---

## 5. 공유자원

### 5.1 외부 자원 (DMAP 마켓플레이스에서 복사)

| 자원 유형 | 자원명 | 원본 경로 | 복사 위치 | 복사 여부 |
|----------|--------|----------|----------|----------|
| 템플릿 | README-plugin-template | `{DMAP_PLUGIN_DIR}/resources/templates/plugin/README-plugin-template.md` | (참조 전용, README.md 작성 시 참고) | ✕ |
| 샘플 | README | `{DMAP_PLUGIN_DIR}/resources/samples/plugin/README.md` | (참조 전용) | ✕ |
| 도구 | convert-to-markdown | `{DMAP_PLUGIN_DIR}/resources/tools/customs/general/convert-to-markdown.py` | (선택 참조, MVP 불필요) | ✕ |
| **가이드** | **ppt-guide** | `{DMAP_PLUGIN_DIR}/resources/guides/docs/ppt-guide.md` | `agents/ppt-writer/references/ppt-guide.md` | ✅ |
| **도구** | **generate_image** | `{DMAP_PLUGIN_DIR}/resources/tools/customs/general/generate_image.py` | `gateway/tools/generate_image.py` | ✅ |

> **결정**:
> - `ppt-guide`: `ppt-writer` 에이전트 전용 참조로 **복사** (슬라이드 스타일 일관성 확보)
> - `generate_image`: `gateway/tools/`에 **복사**하여 `ppt-writer` 에이전트가 슬라이드 일러스트 생성 시 `{tool:image_generate}`로 호출 (Python + Gemini API)
> - 실제 `.pptx` 빌드는 `@ppt-writer` 스킬이 Claude 공식 `anthropic-skills:pptx`에 Skill→Skill 위임 (Node.js/pptxgenjs 불필요)

### 5.2 플러그인 내장 참조 자산 (사전 작성 완료, `references/` + `resources/` 에 보존)

| # | 자원 유형 | 자원명 | 경로 |
|---|----------|--------|------|
| R1 | 교재 | FinOps 교재 | `references/am/finops.md` |
| R2 | 가이드 | State of FinOps 2026 실습 가이드 | `references/finops/state-of-finops-2026-lab-guide.md` |
| 0 | 회사정보 | HBT 회사 프로파일 | `resources/basic-info/company-profile.md` |
| 1 | 샘플 CSV | AWS CUR 2.0 | `resources/sample-billing/aws-cur-sample.csv` |
| 2 | 샘플 CSV | Azure Cost Export | `resources/sample-billing/azure-export-sample.csv` |
| 3 | 샘플 CSV | GCP Billing Export | `resources/sample-billing/gcp-billing-sample.csv` |
| 3-1 | 샘플 CSV | utilization (CPU/Memory/GPU) | `resources/sample-billing/utilization-sample.csv` |
| 3-2 | 샘플 CSV | SaaS LLM (OpenAI/Anthropic) | `resources/sample-billing/saas-llm-sample.csv` |
| 4 | 가이드 | 스키마·학습 이벤트 위치 가이드 | `resources/sample-billing/README.md` |
| 5 | 스키마 | FOCUS v1.3 + AI 확장 5종 | `resources/schema/focus-v1.yaml` |
| 11 | 템플릿 | RI/SP/Spot 의사결정 매트릭스 | `resources/templates/ri-sp-decision-matrix.md` |
| 12 | 템플릿 | 월간 FinOps 리뷰 60분 아젠다 | `resources/templates/monthly-review-agenda.md` |
| 14 | 룰북 | COVERS 6원칙 | `resources/rulebook/covers-principles.yaml` |
| 15 | 룰북 | 게이트 기준 6종 | `resources/rulebook/gate-criteria.yaml` |

### 5.3 에이전트 런타임 생성 산출물 (사전 작성 제외)

Phase 3에서 복사하지 않음 — 에이전트가 스킬 실행 시 생성.

| 경로 | 생성 주체 | 스킬 |
|------|----------|------|
| `resources/mapping/{aws-cur,azure-export,gcp-billing,saas-llm}-to-focus.yaml` | focus-normalizer | `@inform` |
| `resources/mapping/README.md` | focus-normalizer | `@inform` |
| `resources/templates/tag-policy.yaml` | tag-governor | `@inform` |
| `resources/templates/kpi-dashboard.md` | finops-practitioner | `@operate` |
| `out/focus-normalized.csv` | focus-normalizer | `@inform` |
| `out/dashboard.html` | cost-analyst | `@inform` |
| `out/rightsize-plan.md` | rightsize-advisor | `@optimize` |
| `out/commit-strategy.md` | commit-planner | `@optimize` |
| `out/why-statement.md` | strategy-director | `@why-finops` |
| `out/review-runbook.md` | finops-practitioner | `@operate` |
| `out/review-report.md` | reviewer | `@review` |
| `out/ppt-scripts/index.md` | ppt-writer (artifact-selector) | `@ppt-writer` |
| `out/ppt-scripts/images/*.png` | ppt-writer (image-renderer) + `generate_image` 도구 | `@ppt-writer` |
| `out/ppt-scripts/images/index.md` | ppt-writer (image-renderer) | `@ppt-writer` |
| `out/ppt-scripts/{target}-deck.md` (7종) | ppt-writer (slide-designer) | `@ppt-writer` |
| `out/ppt-scripts/{target}-deck.pptx` (7종) | `anthropic-skills:pptx` Skill 위임 산출 | `@ppt-writer` |

### 5.4 커스텀 도구 개발 계획
**추가 개발 없음** — DMAP 마켓플레이스의 `generate_image.py`를 `gateway/tools/`로 **복사 사용**.
Phase 3 Step 3(공유자원 복사)에서 `generate_image.py` 복사 + `.env.example` 템플릿 생성.
`.pptx` 빌드는 별도 도구 없이 `anthropic-skills:pptx`에 Skill→Skill 위임.

---

## 6. 플러그인 구조 설계

### 6.1 에이전트 구성 설계 (9종)

#### 6.1.1 에이전트 목록 및 역할

| # | 에이전트 | 디렉토리 | 티어 | 역할 | 주요 책임 |
|---|---------|---------|------|------|----------|
| 1 | strategy-director | `agents/strategy-director/` | HIGH | 전략 책임자 | WHY 정의·성숙도 진단·COVERS 정렬·OKR 로드맵 |
| 2 | focus-normalizer | `agents/focus-normalizer/` | MEDIUM | FOCUS 변환 전문가 | CSP 4종 매핑 YAML 생성·USD/KRW 환산·Amortized·AI 확장 통합 |
| 3 | cost-analyst | `agents/cost-analyst/` | MEDIUM | 비용 분석가 | 이상 탐지 5단계·Chart.js 9차트 대시보드 HTML 생성 |
| 4 | tag-governor | `agents/tag-governor/` | LOW | 태깅 거버너 | 필수 태그 커버리지·tag-policy.yaml 생성 |
| 5 | rightsize-advisor | `agents/rightsize-advisor/` | MEDIUM | Right-sizing 권고자 | 유휴/과잉 3대안·GPU 활용·모델 다운그레이드 |
| 6 | commit-planner | `agents/commit-planner/` | HIGH | 약정 설계자 | Workload 분류·RI/SP/Spot 3시나리오·BEP·리스크 |
| 7 | finops-practitioner | `agents/finops-practitioner/` | MEDIUM | 운영 체계화 전문가 | 단위경제 KPI·자동화 5단계·리뷰 런북·성숙도 전환 |
| 8 | reviewer | `agents/reviewer/` | HIGH | 독립 검증자 | 4단계 정합성·FOCUS 커버리지·규칙 ID 역참조·수치 일관성 |
| 9 | ppt-writer | `agents/ppt-writer/` | MEDIUM | PPT Deck 작성자 | PPT 적합 산출물 선별 · Gemini 일러스트 생성 · ppt-guide 준수 Marp deck 작성 (.pptx 빌드는 스킬이 `anthropic-skills:pptx`에 위임) |

#### 6.1.2 세부역할(sub_roles) 분화

팀 기획서에서 정의된 서브역할은 개별 에이전트를 만들지 않고 `agentcard.yaml`의 `sub_roles` + AGENT.md 워크플로우 서브섹션으로 구현.

| 에이전트 | sub_roles |
|---------|-----------|
| strategy-director | `maturity-assessor`, `driver-mapper` |
| focus-normalizer | `schema-profiler`, `unit-converter`, `ai-extension-mapper` |
| cost-analyst | `anomaly-detector`, `ai-cost-analyzer`, `chart-renderer` |
| tag-governor | — (단일 역할) |
| rightsize-advisor | `utilization-joiner`, `model-selector` |
| commit-planner | `scenario-modeler`, `workload-classifier` |
| finops-practitioner | `kpi-designer`, `automation-architect` |
| reviewer | — (단일 역할) |
| ppt-writer | `artifact-selector`, `image-renderer`, `slide-designer` |

#### 6.1.3 에이전트 간 핸드오프

```
strategy-director ──(WHY 확정)──► focus-normalizer
focus-normalizer ──(정규화 CSV)──► tag-governor ──(태그 정책)──► cost-analyst
cost-analyst ──(이상 이벤트)──► rightsize-advisor ──(권고안)──► commit-planner
commit-planner ──(3시나리오)──► finops-practitioner ──(KPI·런북)──► reviewer
reviewer ──(검증 완료)──► ppt-writer ──(슬라이드 스크립트)──► (사용자/image-generator 연계)
```

에이전트는 서로 직접 호출하지 않고, 스킬이 순차 오케스트레이션.
`ppt-writer`는 참고한 `courseware:document-converter` · `courseware:image-generator` 패턴을 따라
**입력 문서 선별 → 슬라이드 스크립트 생성** 워크플로우를 수행하며, 실제 이미지 렌더링/PPT 파일 생성은
2차 이터레이션에서 외부 도구(image-generator MCP / python-pptx 등) 연계로 확장.

#### 6.1.4 ppt-writer 상세 설계 (참고: courseware)

**AGENT.md 워크플로우 구조** (sub_roles 4단계):

```
### artifact-selector
#### STEP 1. 산출물 스캔        — out/ 아래 파일 목록 수집, 대상 후보 필터
#### STEP 2. 적합성 평가        — 경영진/의사결정/교육 관점 점수화
#### STEP 3. 선별 결과 정리     — out/ppt-scripts/index.md 생성

### image-renderer   (각 선별된 대상에 대해 반복 수행)
#### STEP 1. 가이드 로드        — agents/ppt-writer/references/ppt-guide.md 의 이미지 스타일 제약 파악
#### STEP 2. 슬라이드 요지 추출 — 해당 대상의 주요 개념·다이어그램 후보를 리스트업
#### STEP 3. 프롬프트 작성      — 교육용 일러스트 스타일(흰 배경·깔끔한 선·전문적·텍스트 최소)
#### STEP 4. Gemini 호출        — `{tool:image_generate}`로 `out/ppt-scripts/images/*.png` 생성 (slug 명명)
#### STEP 5. 인덱스 갱신        — out/ppt-scripts/images/index.md 에 이미지↔슬라이드 매핑 기록

### slide-designer
#### STEP 1. 가이드 로드        — agents/ppt-writer/references/ppt-guide.md 의 컬러/타이포/레이아웃 규칙 파악
#### STEP 2. 슬라이드 구조 결정 — 표지·목차·본문·핵심 메시지·부록 배치
#### STEP 3. Marp 스크립트 작성 — `---` 슬라이드 구분, 제목·불릿·표 요약·image-renderer 산출 이미지 경로 삽입·발표자 노트
#### STEP 4. 스타일 지시 주입   — ppt-guide 요지(최소 12pt, 1152×648, Pretendard, 컬러 팔레트)를 deck md 상단 또는 인접 `{deck}-style.md`에 명시해 `anthropic-skills:pptx` 위임 시 전달되도록 함
#### STEP 5. 검증               — 슬라이드 수·필수 섹션·이미지 파일 존재·스타일 지시 무결성
```

> **PPT 바이너리 빌드는 스킬 `@ppt-writer`의 책임** — DMAP 표준상 에이전트는 Skill 도구를 보유하지 않으므로 `anthropic-skills:pptx` 위임은 스킬 레이어에서 수행.
> `ppt-writer` 에이전트는 deck md + 이미지까지 완성해서 스킬에게 전달.

**슬라이드 스크립트 포맷** (Marp 호환, `anthropic-skills:pptx` 입력으로 사용):

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  /* DMAP ppt-guide 준수 — min font 12pt, Pretendard, 1152x648 */
  section { font-family: Pretendard, "맑은 고딕", Arial; color: #2C2926; }
  h1 { font-size: 36pt; font-weight: bold; }
  h2 { font-size: 28pt; font-weight: bold; }
  p, li { font-size: 16pt; color: #505060; }
  .small { font-size: 12pt; }
---

# {덱 제목}
{부제}

---

## 슬라이드 제목

- 핵심 불릿 1
- 핵심 불릿 2

![개념 다이어그램](images/{slug}.png)

<!-- Speaker Notes:
- 이 슬라이드에서 강조할 내용
- 숫자 근거 출처: references/am/finops.md §4.x
-->
```

**tools.yaml 추상 도구**:
- `{tool:file_read}` — 산출물·ppt-guide·이미지 확인
- `{tool:file_write}` — Marp deck md 작성, 이미지 인덱스 기록
- `{tool:image_generate}` — `gateway/tools/generate_image.py`에 매핑되어 Gemini Nano Banana로 슬라이드용 일러스트 생성

**역할 경계**:
- **is**: PPT Deck 작성자, Marp 스크립터, 이미지 프롬프터, PPT 디자인 가이드 집행자
- **is_not**: `.pptx` 바이너리 빌더(스킬 책임), 데이터 분석가, FinOps 도메인 전문가

**핸드오프**:
- `.pptx` 빌드 단계 → 스킬 `@ppt-writer` (자동, Skill→Skill 위임으로 `anthropic-skills:pptx` 호출)
- FinOps 도메인 질의 시 → 관련 에이전트로 위임 안내

**제약**: `forbidden_actions: ["agent_delegate"]` (다른 에이전트 직접 호출 금지).
사용자 입력(`user_interact`)은 스킬이 주도하므로 에이전트 자체도 금지 목록에 포함 고려 가능하나, 이미지 재시도 확인 등을 위해 제외 유지.

#### 6.1.5 페르소나 자동 생성 정책

- 이름/닉네임: 역할에 어울리는 한국식 이름 + 역할 약어 닉네임 (예: strategy-director → "송태희"/"태희")
- 성별/나이: 경력 기반 합리적 배분 (35~50세)
- style/background: FinOps 경력·성향을 1~2줄로 간결 기술
- Phase 3 Step 4에서 일괄 생성 후 CLAUDE.md 멤버 섹션에 반영

---

### 6.2 스킬 구성 설계

#### 6.2.1 스킬 목록

| # | 스킬명 | 디렉토리 | 유형 | 필수 | 설명 | 오케스트레이션 |
|---|-------|---------|------|------|------|---------------|
| 1 | setup | `skills/setup/` | Setup | ✅ | 플러그인 초기 설정 (모델 버전 확인, CLAUDE.md 라우팅) | 직결형 |
| 2 | help | `skills/help/` | Utility | 권장 | 명령 목록·라우팅 즉시 출력 | 직결형 (하드코딩) |
| 3 | why-finops | `skills/why-finops/` | Orchestrator | ✅ | WHY 정의 & 성숙도 진단 | strategy-director |
| 4 | inform | `skills/inform/` | Orchestrator | ✅ | FOCUS 정규화 + 대시보드 | focus-normalizer → tag-governor → cost-analyst |
| 5 | optimize | `skills/optimize/` | Orchestrator | ✅ | Right-sizing + 약정 3시나리오 | rightsize-advisor → commit-planner |
| 6 | operate | `skills/operate/` | Orchestrator | ✅ | KPI + 자동화 + 리뷰 런북 | finops-practitioner |
| 7 | review | `skills/review/` | Orchestrator | ✅ | 최종 독립 검증 | reviewer |
| 8 | ppt-writer | `skills/ppt-writer/` | Orchestrator | ✅ | 산출물 중 PPT 적합 문서 선별 후 Marp 스타일 슬라이드 스크립트 생성 (post-hoc) | ppt-writer |
| 9 | core | `skills/core/` | Orchestrator | ✅ | 풀 파이프라인 (`@why-finops → @inform → @optimize → @operate → @review`). PPT는 별도 `@ppt-writer` 호출 | Skill→Skill 체이닝 |

> **user-invocable**: setup/help/why-finops/inform/optimize/operate/review/ppt-writer/core 모두 `true`

#### 6.2.2 스킬 워크플로우 — Phase별 간략

| 스킬 | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| why-finops | 요구사항 수집 | Agent: strategy-director (Step 1-1~1-4) | WHY 통합본 검증 (`ulw`) | 사용자 보고 |
| inform | 원본 프로파일링 | Agent: focus-normalizer (매핑·정규화) | Agent: tag-governor (태깅 갭) | Agent: cost-analyst (대시보드) |
| optimize | 정규화 결과 로드 | Agent: rightsize-advisor (유휴·3대안·GPU·모델) | Agent: commit-planner (3시나리오) | 통합 권고 보고 |
| operate | 전 단계 산출 수집 | Agent: finops-practitioner (KPI·파이프라인·런북·성숙도) | 게이트 기준 검증 (`ulw`) | 리뷰 런북 확정 |
| review | 전체 산출 로드 | Agent: reviewer (독립 검증) | 검증 리포트 (`ulw`) | 승인/반려 사용자 안내 |
| ppt-writer | 대상 식별 + 이미지 포함 여부 문의 (AskUserQuestion) | Agent: ppt-writer — artifact-selector + image-renderer (선별·이미지) | Agent: ppt-writer — slide-designer (Marp deck md) | Skill: `anthropic-skills:pptx` 위임으로 각 deck → `.pptx` 빌드 · 검증 (`ulw`) |
| core | why-finops 호출 | inform 호출 | optimize → operate 호출 | review 호출 (ppt-writer 제외) |

- 모든 워크플로우 Phase에 대응 오케스트레이션 스킬(`/oh-my-claudecode:ulw` 폴백) 명시

---

### 6.3 Gateway 설정 설계

#### 6.3.1 install.yaml

```yaml
# finops 플러그인: 코어는 정적 CSV+프롬프트로 완결, @ppt-writer에서만 이미지 생성 도구 필요
mcp_servers: []
lsp_servers: []
custom_tools:
  - name: generate_image
    description: "Gemini(Nano Banana) 기반 교육용 이미지 생성 — @ppt-writer 슬라이드 일러스트"
    source: tools/generate_image.py
    required: false                       # 이미지 없는 텍스트 슬라이드도 가능
```

#### 6.3.2 runtime-mapping.yaml

```yaml
tier_mapping:
  default:
    HEAVY:
      model: "claude-opus-4-7"
    HIGH:
      model: "claude-opus-4-7"
    MEDIUM:
      model: "claude-sonnet-4-6"
    LOW:
      model: "claude-haiku-4-5"

tool_mapping:
  image_generate:
    - type: custom
      source: "tools/generate_image.py"
      tools: ["generate_image"]

action_mapping:
  file_write: ["Write", "Edit"]
  file_delete: ["Bash"]
  code_execute: ["Bash"]
  network_access: ["WebFetch", "WebSearch"]
  user_interact: ["AskUserQuestion"]
  agent_delegate: ["Task"]
```

> `.pptx` 바이너리 빌드는 `@ppt-writer` 스킬이 Skill→Skill 위임으로 `anthropic-skills:pptx`를 호출 — 도구 매핑이 아닌 스킬 위임이므로 `tool_mapping`에 포함하지 않음.

#### 6.3.3 각 에이전트 tools.yaml (최소 추상 도구)

모든 에이전트 공통으로 빌트인 도구만 사용 — `file_read`, `file_write` 같은 builtin은 런타임이 내장 처리하므로 `tools.yaml`은 **선택적**. 생략하고 AGENT.md에 필요한 작업만 명시.

> 예외: cost-analyst의 HTML 대시보드 생성은 `{tool:file_write}`로 명시하면 프롬프트 명확성 향상. Phase 3에서 각 에이전트 판단.

---

### 6.4 디렉토리 구조 설계

```
finops-lab/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .claude/
│   └── settings.local.json              # Phase 5에서 권한 설정
├── .gitignore
├── CLAUDE.md                            # Phase 4에서 생성
├── README.md                            # Phase 3 Step 8에서 생성
│
├── commands/
│   ├── setup.md
│   ├── help.md
│   ├── why-finops.md
│   ├── inform.md
│   ├── optimize.md
│   ├── operate.md
│   ├── review.md
│   ├── ppt-writer.md
│   └── core.md
│
├── skills/
│   ├── setup/SKILL.md
│   ├── help/SKILL.md
│   ├── why-finops/SKILL.md
│   ├── inform/SKILL.md
│   ├── optimize/SKILL.md
│   ├── operate/SKILL.md
│   ├── review/SKILL.md
│   ├── ppt-writer/SKILL.md
│   └── core/SKILL.md
│
├── agents/
│   ├── strategy-director/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── focus-normalizer/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── cost-analyst/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── tag-governor/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── rightsize-advisor/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── commit-planner/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── finops-practitioner/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   ├── reviewer/
│   │   ├── AGENT.md
│   │   └── agentcard.yaml
│   └── ppt-writer/
│       ├── AGENT.md
│       ├── agentcard.yaml
│       ├── tools.yaml                    # file_read, file_write, image_generate 선언
│       └── references/
│           └── ppt-guide.md              # DMAP 마켓플레이스 복사 (스타일·레이아웃·검증 규칙)
│
├── gateway/
│   ├── install.yaml
│   ├── runtime-mapping.yaml
│   └── tools/
│       ├── generate_image.py             # DMAP 마켓플레이스 복사 (Gemini Nano Banana)
│       └── .env.example                  # GEMINI_API_KEY 템플릿
│
├── references/                          # 사전 작성 (보존)
│   ├── am/finops.md
│   └── finops/state-of-finops-2026-lab-guide.md
│
├── resources/                           # 사전 작성 (보존) + 런타임 생성
│   ├── basic-info/
│   │   └── company-profile.md
│   ├── sample-billing/
│   │   ├── aws-cur-sample.csv
│   │   ├── azure-export-sample.csv
│   │   ├── gcp-billing-sample.csv
│   │   ├── utilization-sample.csv
│   │   ├── saas-llm-sample.csv
│   │   └── README.md
│   ├── schema/
│   │   └── focus-v1.yaml
│   ├── templates/
│   │   ├── ri-sp-decision-matrix.md
│   │   └── monthly-review-agenda.md
│   ├── rulebook/
│   │   ├── covers-principles.yaml
│   │   └── gate-criteria.yaml
│   └── mapping/                         # 런타임 생성 (비워 둠)
│
├── output/                              # 이미 존재 (team-plan, requirements, develop-plan)
└── out/                                 # 사용자 실행 시 생성 (산출물)
    ├── step1/
    ├── step2/
    ├── step3/
    ├── step4/
    ├── ppt-scripts/                     # @ppt-writer 산출물
    │   ├── index.md                     # 선별 결과 + deck 목록
    │   ├── images/                      # Gemini 생성 슬라이드 일러스트
    │   │   ├── index.md                 # 이미지↔슬라이드 매핑
    │   │   └── *.png
    │   ├── {대상}-deck.md               # Marp deck md (7종, anthropic-skills:pptx 입력)
    │   └── {대상}-deck.pptx             # 최종 PPT 바이너리 (7종, anthropic-skills:pptx 산출)
    ├── why-statement.md
    ├── focus-normalized.csv
    ├── dashboard.html
    ├── rightsize-plan.md
    ├── commit-strategy.md
    ├── review-runbook.md
    └── review-report.md
```

---

## 7. 개발 계획

### 7.1 개발 순서 (순차적)

| 순번 | 단계 | 파일/디렉토리 | 검증 방법 |
|------|------|--------------|----------|
| 1 | 스켈레톤 & 매니페스트 | `.claude-plugin/plugin.json`, `marketplace.json`, `.gitignore` | JSON 유효성 + DMAP 표준 필수 필드 |
| 2 | Gateway 설정 | `gateway/install.yaml`, `gateway/runtime-mapping.yaml` | tier_mapping 모델 최신화, action_mapping, custom_tools 포함 |
| 3 | 공유자원 복사 | `gateway/tools/generate_image.py`, `agents/ppt-writer/references/ppt-guide.md`, `gateway/tools/.env.example` | 원본과 바이트 일치, .env 템플릿에 GEMINI_API_KEY |
| 4 | 에이전트 9종 작성 | `agents/*/AGENT.md`, `agentcard.yaml` (ppt-writer는 tools.yaml 포함) | agent 표준 검증 체크리스트 |
| 5 | 스킬 9종 작성 | `skills/*/SKILL.md` | skill 표준 검증 체크리스트, 위임 5항목/3항목 |
| 6 | commands 진입점 | `commands/*.md` | 9개 스킬 각각 1:1 |
| 6 | CLAUDE.md 생성 | `CLAUDE.md` | Phase 4 구조 준수, 멤버·변수·Advisor 섹션 포함 |
| 7 | 권한 설정 | `.claude/settings.local.json` | DMAP 권한 5종 포함 |
| 8 | README.md 작성 | `README.md` | 필수 6섹션 + 변수 치환 |
| 9 | 최종 검증 | 전체 | Phase 6 체크리스트 13항목 통과 |

### 7.2 병렬 가능 단계

| 묶음 | 병렬 대상 |
|------|----------|
| 에이전트 작성 (3단계) | 9종 에이전트를 5개씩 2배치로 병렬 작성 |
| 스킬 작성 (4단계) | 기능 스킬 6종(why-finops/inform/optimize/operate/review/ppt-writer) 병렬 작성 |
| commands 파일 (5단계) | 9개 동일 패턴 → 일괄 생성 |

### 7.3 공유 자원 활용 계획

| 자원 | 활용 방법 |
|------|----------|
| `references/am/finops.md` | 각 에이전트 AGENT.md의 "참조" 섹션에서 §번호로 링크 |
| `references/finops/state-of-finops-2026-lab-guide.md` | 특히 strategy-director, cost-analyst, finops-practitioner에서 활용 |
| `resources/sample-billing/*.csv` | focus-normalizer·cost-analyst·rightsize-advisor가 Read 도구로 직접 로드 |
| `resources/schema/focus-v1.yaml` | focus-normalizer 스키마 목표 |
| `resources/rulebook/*.yaml` | 모든 에이전트 권고·판정의 규칙 ID 소스 |
| `resources/templates/*` | commit-planner, finops-practitioner 템플릿 입력 |
| `{DMAP_PLUGIN_DIR}/resources/templates/plugin/README-plugin-template.md` | README.md 작성 시 구조 참조 |
| `courseware:document-converter` 패턴 | `ppt-writer` AGENT.md 워크플로우 구조(sub_roles 2단계) 참조 |
| `courseware:image-generator` 패턴 | `ppt-writer` 슬라이드별 이미지 플레이스홀더 작성 규칙 참조 (2차 이터레이션에서 실제 생성 연계) |

### 7.4 기술 요구사항 확인

#### Python 라이브러리 (`@ppt-writer` 이미지 생성 시만 필요)
- `python-dotenv` — `.env` 로드
- `google-genai` — Gemini Nano Banana API 호출

설치: `pip install python-dotenv google-genai`
검증: `python gateway/tools/generate_image.py --help`

#### Node.js 의존성
**없음** — `.pptx` 빌드는 `@ppt-writer` 스킬이 Skill→Skill 위임으로 `anthropic-skills:pptx`(Claude 공식 Agent Skill)를 호출하여 수행.

#### 환경 변수 (`gateway/tools/.env`, `@ppt-writer` 이미지 생성 시만)

| 변수명 | 필수 | 설명 |
|--------|:----:|------|
| `GEMINI_API_KEY` | 이미지 생성 시 필수 | Google Gemini API Key (https://ai.google.dev/) |

> setup 스킬이 `.env.example` 생성 및 값 입력 안내. 이미지 없는 텍스트 슬라이드만 생성할 경우 불필요.

#### MCP/LSP 서버
**없음** — Claude Code 빌트인 + OMC 기본 제공으로 완결.

#### 스킬 의존성 (Skill→Skill 위임)
- `anthropic-skills:pptx` — Anthropic 공식 Agent Skill, Claude Code/CoWork/Claude.ai 전반에서 기본 제공. 별도 설치 불필요.

### 7.5 품질 게이트

| 단계 | 게이트 |
|------|-------|
| Phase 3 (에이전트) | agent 표준 체크리스트 22항목 통과 |
| Phase 3 (스킬) | skill 표준 체크리스트 25항목 통과 |
| Phase 3 (Gateway) | gateway 표준 체크리스트 12항목 통과 |
| Phase 6 (최종) | 검증표 13항목 전수 통과 |

---

## 8. 제약 및 가정

- **MVP 범위**: 정적 CSV 학습. 실 API 연동은 2차 이터레이션
- **샘플 데이터 결정성**: 동일 CSV → 동일 이상·유휴·약정 기회 재현 필수
- **브라우저 전용**: 대시보드 HTML은 Chart.js 4.x CDN을 로드하므로 최초 로드 시 인터넷 필요. 이후 오프라인 가능 (CDN 캐시)
- **모델 버전**: setup 스킬에서 최신 Opus/Sonnet/Haiku 버전 확인 후 runtime-mapping.yaml 갱신
- **@ppt-writer 의존성 격리**: Python + `google-genai`는 **이미지 생성이 필요한 경우에만** 설치. 이미지 없는 텍스트 슬라이드는 의존성 0으로 생성 가능. `.pptx` 바이너리 빌드는 `anthropic-skills:pptx`(Claude 내장)가 수행하므로 Node/npm 불필요
- **PPT 품질 표준**: DMAP `ppt-guide.md` 준수 필수 — 최소 12pt 폰트, 1152×648pt 슬라이드, Pretendard 서체. Marp deck의 `style:` frontmatter에 규칙을 기술하여 `anthropic-skills:pptx`에 전달
- **이미지 생성 선택**: `GEMINI_API_KEY` 미설정 시 이미지 없이 텍스트·표·발표자 노트 중심 슬라이드로 PPT 생성 (AskUserQuestion으로 분기)
- **런타임 이식성**: `anthropic-skills:pptx`는 Anthropic 공식 Agent Skill로 Claude Code · CoWork · Claude.ai 전반 공통 제공. 런타임 교체 시에도 동일 스킬명으로 호출

---

## 9. Phase별 산출물 명세

| Phase | 산출물 |
|-------|--------|
| Phase 1 | `output/requirements.md` ✅ (완료) |
| Phase 2 | `output/develop-plan.md` (이 문서) |
| Phase 3 | 플러그인 전체 구조 (에이전트 9 + 스킬 9 + gateway/tools/ + commands 9 + README + ppt-guide 복사) |
| Phase 4 | `CLAUDE.md` |
| Phase 5 | `.claude/settings.local.json` |
| Phase 6 | 검증 리포트 + 최종 보고 |
