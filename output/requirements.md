# finops-lab 요구사항 정의서

> 팀 기획서(`output/team-plan-finops-lab.md`)를 기반으로 수집·확정된 요구사항 정의.
> Phase 1 산출물 — Phase 2(설계) 입력으로 사용.

---

## 1. 기본 정보

| 항목 | 내용 |
|------|------|
| 플러그인명 | `finops-lab` |
| 마켓플레이스명 | `finops-lab` (플러그인명과 동일) |
| Owner (GitHub) | `hiondal` |
| Version | `0.0.1` |
| License | MIT |
| 대상 도메인 | 멀티클라우드 FinOps · FinOps for AI(LLM 토큰·GPU) · 비용 거버넌스 · 단위경제 · 이상 비용 탐지 |
| 대상 사용자 | FinOps 실무자/팀장, 클라우드 아키텍트, DevOps/SRE, CCoE 준비 조직, 재무·사업부 Cost Owner |
| 목표 (한 줄) | FinOps 교재·2026 프레임워크를 4단계(WHY → Inform → Optimize → Operate)로 가상 기업 HBT 데이터에 적용해 체득 |

---

## 2. 핵심기능 (4종)

### 2.1 `@why-finops` — WHY 정의 & 성숙도 진단
- 비즈니스 이슈를 FinOps 3대 가치로 매핑
- Ownership×Capability 다차원 성숙도 자가진단 (Crawl/Walk/Run)
- COVERS 6원칙 정렬 + 12개월 스킬셋 로드맵(AI Cost · Tooling · Automation · Forecasting)

### 2.2 `@inform` — FOCUS 정규화 & 통합 가시성
- 3 CSP 빌링(AWS CUR 2.0 · Azure Cost Export · GCP Billing) + SaaS LLM(OpenAI/Anthropic) → FOCUS v1.3 정규화
- AI 확장 컬럼 5종(TokenCountInput/Output · ModelName · GpuHours · GpuUtilization)
- 태깅 거버넌스 갭 분석 + 이상 비용 탐지
- **단일 파일 인터랙티브 웹 대시보드** (`out/dashboard.html`, Chart.js 4.x CDN, 9차트=CSP 5 + AI 4, <1.2MB)

### 2.3 `@optimize` — Right-sizing & 약정 전략
- 유휴 리소스 탐지(CPU 40% / Memory 60% / 2주 지속)
- Right-sizing 3대안 (Downsize-1/Downsize-2/Terminate)
- GPU 활용률 <60% 탐지 + 모델 다운그레이드 권고(GPT-4o → GPT-4o-mini 등)
- RI/SP/Spot 혼합 3시나리오 (Conservative/Base/Optimistic)

### 2.4 `@operate` — 운영 체계화
- 단위경제 KPI 6종 (CSP 3: 가입자당·API 100만 건당·ML 학습 1회당 / AI 3: 토큰 1M당·추론 1,000건당·GPU 시간당)
- 자동화 파이프라인 5단계 (탐지→권고→승인→적용→검증)
- 게이트 기준 6종 (태깅≥95% · MAPE≤10% · RI≥80% · 이상탐지≤24h · 유휴≤3% · GPU 활용률≥60%)
- 주/월/분기 리뷰 런북 + Crawl→Walk 12개월 전환 플랜

---

## 3. 사용자 플로우

4-STEP 순차 실행. 각 스텝 세부 작업 및 참고 문서는 팀 기획서 §사용자 플로우 참조.

| STEP | 스킬 | 핵심 산출물 |
|------|------|------------|
| STEP 1 | `@why-finops` | `out/why-statement.md`, `out/step1/1~3-*.md` |
| STEP 2 | `@inform` | `out/focus-normalized.csv`, `out/dashboard.html`, mapping YAML 4종 |
| STEP 3 | `@optimize` | `out/rightsize-plan.md`, `out/commit-strategy.md` |
| STEP 4 | `@operate` | `resources/templates/kpi-dashboard.md`, `out/review-runbook.md` |

---

## 4. 에이전트 구성 (8종 확정)

> 페르소나(이름·닉네임·성별·나이·성향·배경)는 Phase 3에서 자동 생성 후 일괄 승인.

| # | 에이전트 | 티어 | 역할 | 세부역할 |
|---|---------|------|------|---------|
| 1 | `strategy-director` | HIGH | WHY 정의·성숙도 진단 | maturity-assessor, driver-mapper |
| 2 | `focus-normalizer` | MEDIUM | FOCUS 변환·매핑·병합 | schema-profiler, unit-converter, ai-extension-mapper |
| 3 | `cost-analyst` | MEDIUM | 비용 분석·이상 탐지·웹 대시보드 | anomaly-detector, ai-cost-analyzer, chart-renderer |
| 4 | `tag-governor` | LOW | 태깅 거버넌스·tag-policy 생성 | — |
| 5 | `rightsize-advisor` | MEDIUM | Right-sizing·GPU·모델 다운그레이드 | utilization-joiner, model-selector |
| 6 | `commit-planner` | HIGH | RI/SP/Spot 3시나리오 설계 | scenario-modeler, workload-classifier |
| 7 | `finops-practitioner` | MEDIUM | KPI·자동화·리뷰 런북 | kpi-designer, automation-architect |
| 8 | `reviewer` | HIGH | 독립 최종 검증 | — |

---

## 5. 스킬 구성

### 5.1 기능 스킬 (Orchestrator 유형)

| 스킬명 | 설명 | 오케스트레이션 |
|-------|------|---------------|
| `why-finops` | WHY 정의 + 성숙도 진단 + COVERS 정렬 + 스킬셋 로드맵 | strategy-director (단독) |
| `inform` | FOCUS 정규화 + 이상 탐지 + 웹 대시보드 + 태깅 갭 분석 | focus-normalizer → tag-governor → cost-analyst |
| `optimize` | 유휴/Right-sizing + GPU/모델 + RI/SP/Spot 3시나리오 | rightsize-advisor → commit-planner |
| `operate` | 단위경제 KPI + 자동화 파이프라인 + 리뷰 런북 + 성숙도 전환 | finops-practitioner |
| `review` | 최종 산출물 독립 검증 | reviewer |

### 5.2 시스템 스킬

| 스킬명 | 유형 | 설명 |
|-------|------|------|
| `setup` | Setup | 도구 설치·모델 버전 확인·runtime-mapping 갱신 (필수) |
| `help` | Utility | 명령 목록·라우팅 규칙 하드코딩 즉시 출력 |
| `core` | Core (위임형) | `@why-finops → @inform → @optimize → @operate → @review` 풀 파이프라인 |

### 5.3 자연어 라우팅 키워드

| 키워드 | 라우팅 |
|-------|-------|
| `@why`, `@why-finops`, "FinOps 왜" | `why-finops` |
| `@inform`, "FOCUS 정규화", "대시보드" | `inform` |
| `@optimize`, "Right-sizing", "약정" | `optimize` |
| `@operate`, "KPI", "리뷰 런북" | `operate` |
| `@review`, "최종 검증" | `review` |
| `@core`, "FinOps 랩 전체", "처음부터 끝까지" | `core` |

---

## 6. 기술 요구사항

### 6.1 커스텀 도구 (Python/CLI)
**없음** — 모든 산출은 에이전트 프롬프트 주도 (CSV 읽기·YAML 생성·HTML 렌더링 포함). Claude의 Read/Write/Edit 내장 도구만 사용.

### 6.2 외부 공유자원 (DMAP 마켓플레이스)

| 자원 유형 | 자원명 | 원본 경로 | 복사 위치 |
|----------|--------|----------|----------|
| 템플릿 | README-plugin-template | `{DMAP_PLUGIN_DIR}/resources/templates/plugin/README-plugin-template.md` | (참조 전용, README 작성 참고) |
| 샘플 | README | `{DMAP_PLUGIN_DIR}/resources/samples/plugin/README.md` | (참조 전용) |
| 도구 | convert-to-markdown | `{DMAP_PLUGIN_DIR}/resources/tools/customs/general/convert-to-markdown.py` | `{PLUGIN_DIR}/gateway/tools/convert-to-markdown.py` (선택적 — references 확장 시) |

### 6.3 플러그인 내장 자산 (finops-lab 전용, 사전 작성됨)

| # | 자원 유형 | 자원명 | 위치 |
|---|----------|--------|------|
| 0 | 회사정보 | HBT 회사 프로파일 | `resources/basic-info/company-profile.md` |
| 1 | 샘플 CSV | AWS CUR 2.0 (~830 rows, Bedrock·p4d GPU 포함) | `resources/sample-billing/aws-cur-sample.csv` |
| 2 | 샘플 CSV | Azure Cost Export (~985 rows, Azure OpenAI·NC/ND GPU) | `resources/sample-billing/azure-export-sample.csv` |
| 3 | 샘플 CSV | GCP Billing (~470 rows, Vertex AI·A2/A3 GPU) | `resources/sample-billing/gcp-billing-sample.csv` |
| 3-1 | 샘플 CSV | utilization (CPU/Memory + `gpu_util_pct`) | `resources/sample-billing/utilization-sample.csv` |
| 3-2 | 샘플 CSV | SaaS LLM (OpenAI/Anthropic ~200 rows) | `resources/sample-billing/saas-llm-sample.csv` |
| 4 | 가이드 | 스키마·학습 이벤트 위치 가이드 | `resources/sample-billing/README.md` |
| 5 | 스키마 | FOCUS v1.3 + AI 확장 5종 | `resources/schema/focus-v1.yaml` |
| 11 | 템플릿 | RI/SP/Spot 의사결정 매트릭스 | `resources/templates/ri-sp-decision-matrix.md` |
| 12 | 템플릿 | 월간 FinOps 리뷰 60분 아젠다 | `resources/templates/monthly-review-agenda.md` |
| 14 | 룰북 | COVERS 6원칙 | `resources/rulebook/covers-principles.yaml` |
| 15 | 룰북 | 게이트 기준 6종 | `resources/rulebook/gate-criteria.yaml` |

### 6.4 참조 문서 (학습 1차 자료)

| 문서 | 경로 | 용도 |
|------|------|------|
| FinOps 교재 | `references/am/finops.md` | §4.1~§4.16 전 섹션이 스킬·에이전트에 1:1 매핑 |
| State of FinOps 2026 실습 가이드 | `references/finops/state-of-finops-2026-lab-guide.md` | 2026 트렌드 · AI 98% · FOCUS 85%· Top 스킬셋 |

### 6.5 에이전트 런타임 생성 산출물 (사전 작성 제외)

| 경로 | 생성 주체 | 스킬 |
|------|----------|------|
| `resources/mapping/aws-cur-to-focus.yaml` | focus-normalizer | `@inform` |
| `resources/mapping/azure-export-to-focus.yaml` | focus-normalizer | `@inform` |
| `resources/mapping/gcp-billing-to-focus.yaml` | focus-normalizer | `@inform` |
| `resources/mapping/saas-llm-to-focus.yaml` | focus-normalizer | `@inform` |
| `resources/mapping/README.md` | focus-normalizer | `@inform` |
| `resources/templates/tag-policy.yaml` | tag-governor | `@inform` |
| `resources/templates/kpi-dashboard.md` | finops-practitioner | `@operate` |
| `out/focus-normalized.csv` | focus-normalizer | `@inform` |
| `out/dashboard.html` (Chart.js 9차트) | cost-analyst | `@inform` |
| `out/rightsize-plan.md` | rightsize-advisor | `@optimize` |
| `out/commit-strategy.md` | commit-planner | `@optimize` |
| `out/review-runbook.md` | finops-practitioner | `@operate` |
| `out/why-statement.md` | strategy-director | `@why-finops` |

### 6.6 프로그래밍/런타임
- **언어**: 마크다운·YAML·CSV·HTML(+Chart.js CDN) — 런타임 서버 불필요
- **모델 티어 매핑**: runtime-mapping.yaml에 LOW/MEDIUM/HIGH 지정 (Phase 3 setup 스킬에서 최신 버전 확인)
- **의존성**: 브라우저만 있으면 대시보드 열람 가능 (오프라인)
- **환경변수**: `.env` 파일 **불필요** (API 연동 없음, 전량 정적 CSV)

---

## 7. 비기능 요구사항

| 항목 | 기준 |
|------|------|
| 이식성 | DMAP 기반 Claude Code·Cursor·Cowork 공통 동작 |
| 재현성 | 동일 샘플 CSV 입력 → 동일 이상 5건·유휴·약정 기회 탐지 (태깅 ±2%p 허용) |
| 크기 제한 | CSV 1종 ≤ 1,000 rows · AI 샘플 ≤ 400 rows · 정규화 결과 ≤ 2,500 rows · 대시보드 HTML ≤ 1.2MB |
| 증거 기반 | 모든 권고에 교재 §번호 · COVERS 규칙 ID · 게이트 항목 역참조 가능 |
| 스펙 고정 | FOCUS v1.3 고정, 변경 시 changelog 필수 |
| 보안 | 실 CSP 청구 데이터 외부 전송 금지, PII 가능 필드 마스킹 권고를 README에 명시 |
| AI 가시성 | 토큰·모델·GPU 단위 Granular 모니터링 (태깅 누락 시 경고) |

---

## 8. 외부 시스템 연동

**MVP 범위: 없음** (정적 CSV 기반 학습 랩).

2차 이터레이션 후보(현 스코프 제외):
- AWS Cost Explorer API · Azure Cost Management API · GCP Billing BigQuery
- OpenAI/Anthropic Usage API 실데이터
- Infracost / PR Gate (Shift-Left IaC)

---

## 9. 성공 기준 (팀 기획서 §성공기준 승계)

| 구분 | 기준 |
|------|------|
| 교재 커버리지 | finops.md §4.4~§4.16 전 섹션이 스킬·에이전트·자산에 1:1 매핑 — reviewer 100% 통과 |
| FOCUS 완전성 | Mandatory 15종 + AI 확장 5종, 월 총합 원본 ±0.01 KRW 일치 |
| 가시성 | Chart.js 9차트 + 이상 비용 5건(CSP 3 + AI 2) 자동 식별, 오프라인 열람 가능 |
| AI 비용 가시성 | 모델별 비용·토큰 추이·GPU 히트맵·AI 단위경제 표 연동 |
| 태그 거버넌스 | 누락률 ±2%p 내 재현, tag-policy.yaml 런타임 생성 |
| 최적화 | 유휴 6종+ · Right-sizing 3대안 · RI/SP/Spot 3시나리오 |
| 운영 | KPI 6종 · 자동화 5단계 · 게이트 6종 리뷰 런북 삽입 |
| 룰북 추적성 | COVERS-*-## · gate-criteria 규칙 ID 역참조 |
| 성숙도 | Crawl→Walk 12개월 로드맵 Ownership별 연결 |
| DMAP 준수 | `dmap:develop-plugin` Phase 6 검증 전 항목 통과 |

---

## 10. Phase 1 단계 확정 사항 요약

| 결정 항목 | 확정 |
|----------|------|
| Owner (GitHub) | `hiondal` |
| 에이전트 페르소나 | Phase 3에서 자동 생성 후 일괄 승인 |
| 커스텀 도구 | 없음 (에이전트 프롬프트로 완결) |
| 외부 API 연동 | MVP 범위 제외 |
| 환경변수(.env) | 불필요 |
| 커스텀 도구 개발 필요 외부 공유자원 | `convert-to-markdown` (선택 참조 전용, 필수 복사 아님) |
