# 팀 기획서

## 기본 정보
- 플러그인명: am-strategy
- 목표: 엔터프라이즈 시스템을 AM(Application Modernization)으로 전환하기 위한 전략 수립을
  **WHY 정의 → 현황분석 → 전략수립** 3단계로 체계적·자동화 지원
- 대상 도메인: 엔터프라이즈 IT · Application Modernization · 레거시 현대화
- 대상 사용자: CIO/CTO 보좌 조직, 디지털혁신실, EA팀, PMO, 인프라·운영팀 리더

---

## 핵심기능
- **WHY 정의**: 비즈니스 동인(Speedy/Service Always/Save Cost/Security/혁신) 정리,
  기대 성과 3단계 정량화(L1 벤치마크 → L2 자동 측정 → L3 파일럿), 경영진 스폰서십 전략 설계
- **현황 분석**: 시스템 인벤토리 구축(6개 카테고리), 4차원 건강도 스코어카드, 기술 부채 비용 산정,
  A/B/C 등급 분류, 전환 적합도 판정(6R 매핑·TIME 모델), 서비스 경계 식별(Event Storming·Context Map),
  변화관리 조기 착수(이해관계자 맵)
- **전략 수립**: 6R 전략 상세화(시스템별 예산/기간/리스크), 전체 포트폴리오 Phase 구성,
  파일럿 대상 선정, TCO(As-Is/To-Be)·BEP 산정, 4영역 리스크 평가, 거버넌스 회의체 및 Phase별
  품질/보안 가드레일, 변화관리 기획(커뮤니케이션·교육·조직·문화)
- **최종 보고서**: 경영진 발표용 전략 보고서를 MS Word/PowerPoint로 산출

---

## 사용자 플로우

### STEP 1. WHY 정의
참고정보:
- `references\am-strategy\company-profile.md` (대상 기업 프로파일)
- `references\dora\` 디렉토리 (DORA 2025 벤치마크·인사이트 — 모든 Step에서 활용)
  - 특히 [`06-am-transformation-implications.md`](references/dora/06-am-transformation-implications.md) — 5S+혁신 동인별 DORA 근거 매핑
  - [`01-software-delivery-performance.md`](references/dora/01-software-delivery-performance.md) — 5개 지표 분포·Top % (L1 정량화 근거)
- `references\tco-benchmark\` 디렉토리 (한국 시장 검증된 2025+ 정량 데이터)
  - 특히 [`01-public-sector.md`](references/tco-benchmark/01-public-sector.md) — 행안부 7년 TCO 18.4%·81% 장애 감소·114% 처리속도
  - [`04-data-gap-and-supplement.md`](references/tco-benchmark/04-data-gap-and-supplement.md) — 한국 업종별 데이터 부족 영역 + 글로벌 보충 가이드

- Step 1-1. 비즈니스 동인 정의 (4S + 혁신)
  - 5개 동인별로 현재 이슈·목표·지표 매핑 → `output/{project}/step1/1-drivers.md`
  - DORA 2025 "AI mirror" 인사이트 활용 — 동인별 시급성 메시지 (`06`)
- Step 1-2. 기대 성과 정량화 (L1 단계)
  - DORA 2025 5개 지표(Throughput 3 + Instability 2) 분포 기반 Top % 목표 범위 제시 (`01`)
  - 산출물: `output/{project}/step1/2-quant-L1.md`
- Step 1-3. 경영진 스폰서십 확보 전략
  - L1(방향성) → L2(비용 근거) → L3(실증) 3단계 시나리오, KPI 합의안, 경영진 보고 템플릿
  - 핵심 카드: "AM 없이 AI 투자는 ROI 0" (`04`, `06`)
  - 산출물: `output/{project}/step1/3-sponsorship.md`
- Step 1-4. WHY 통합본 작성
  - 동인·정량화·스폰서십을 하나의 경영진 보고서로 통합 → `output/{project}/step1/why-statement.md`

### STEP 2. 현황 분석
참고정보:
- [`02-seven-team-profiles.md`](references/dora/02-seven-team-profiles.md) — 7개 팀 아키타입 (인벤토리·등급분류·진단에 활용)
- [`05-value-stream-management.md`](references/dora/05-value-stream-management.md) — VSM (서비스 경계 식별의 강력한 입력)

- Step 2-1. 시스템 인벤토리 구축
  - 참조: `references\am-strategy\system-inventory.md`
  - 6개 카테고리(기본정보·기술스택·아키텍처·운영현황·비용·의존성) 수집 템플릿 생성
  - 인터뷰 질문지(비즈니스팀·개발팀·운영팀·재무팀)
    - DORA 2025 기반 8개 추가 질문 (`06` 참조) — 배포빈도·리드타임·복구·CFR·AI 컨텍스트 가용성·작은 배치 비율 등
  - 산출물: `output/{project}/step2/1-inventory.md`
- Step 2-2. A/B/C 등급 분류
  - 비즈니스 가치·사용자 수·매출 기여도 기준으로 A/B/C 분류 → `output/{project}/step2/2-abc.md`
  - DORA 7개 클러스터 매핑 보강 (`02`, `06`) — A/B/C × Cluster 1~7 교차 분석
- Step 2-3. 건강도 4차원 스코어카드
  - 비즈니스 가치·기술 품질·데이터 결합도·운영 안정성 1~5점 평가
  - 자동 분석 도구(SonarQube/CAST Highlight) 결과 파싱 + 수동 평가 통합
  - DORA 8개 차원 자가진단 보강 (`02`) — 통합 12차원 진단으로 발전
  - 산출물: `output/{project}/step2/3-healthscore.md`
- Step 2-4. 기술 부채 비용 산정
  - 유지보수 추가 공수·장애 대응·보안 리스크·인재 이탈·기회 비용 정량화
  - + "AI ROI 잠금 비용" (DORA 2025 핵심 발견 — `04`, `06`)
  - 산출물: `output/{project}/step2/4-techdebt-cost.md`
- Step 2-5. 전환 적합도 판정
  - 건강도 → 6R 매핑, TIME 모델(Tolerate/Invest/Migrate/Eliminate) 2×2 매트릭스
  - DORA Cluster → 6R/TIME 권장 매핑 표 (`02`, `06`)
  - **6R/TIME 매칭 룰북 적용**: [`references/6r/`](references/6r/) 디렉토리의 8단계 결정 알고리즘으로 일관된 추천
  - 산출물: `output/{project}/step2/5-fit-6r-time.md`
- Step 2-6. 서비스 경계 식별 (Rearchitect/Rebuild 대상)
  - Event Storming 워크숍 가이드, Context Map, 유비쿼터스 언어 사전
  - VSM 매핑 워크숍 가이드 통합 (`05`, `07`) — code commit→production 범위 As-Is/To-Be 매핑
  - 산출물: `output/{project}/step2/6-bounded-context.md`
- Step 2-7. 변화관리 조기 착수
  - 이해관계자 맵, 참여형 워크숍 어젠다, 초기 커뮤니케이션 메시지
  - 클러스터별 차별화 메시지 (`02` Step 2-7 적용 가이드 참조)
  - 산출물: `output/{project}/step2/7-change-kickoff.md`

### STEP 3. 전략 수립
참고정보:
- [`03-ai-capabilities-model.md`](references/dora/03-ai-capabilities-model.md) — 7개 AI 역량 (개념·증거)
- [`04-platform-engineering.md`](references/dora/04-platform-engineering.md) — 플랫폼 엔지니어링이 6R·TCO에 미치는 영향
- [`07-ai-capabilities-implementation.md`](references/dora/07-ai-capabilities-implementation.md) — 역량별 실행 가이드·측정·안티패턴

- Step 3-1. 6R 전략 상세화
  - 시스템별 실행 내용·기간·예산(범위)·리스크·예비비(15~20%) 산정
  - 6R 전략에 "AM + AI 시너지" 분석 추가 (`06`) — 예: Lift & Shift는 AI ROI 잠금 효과 ↓
  - **6R 비용·기간 표준 프로파일 적용**: [`references/6r/05-cost-effort-risk-profile.md`](references/6r/05-cost-effort-risk-profile.md) — 시스템 규모(Small/Medium/Large) × 6R별 표준 범위 + 누락 빈도 높은 14개 비용 항목 체크리스트
  - 산출물: `output/{project}/step3/1-6r-detail.md`
- Step 3-2. 포트폴리오 Phase 구성
  - Phase 0(분석) → Phase 1(Quick Win) + Phase 1'(파일럿) → Phase 2~4, GO/NO-GO 게이트
  - **Phase 0 필수 항목** (`06`, `07`): 12개 플랫폼 특성 자가평가, VSM 매핑, 7개 AI 역량 베이스라인, AI 정책 초안
  - 파일럿 대상 선정(B등급·롤백 용이·독립 DB·팀 의지·성과 가시성)
  - + DORA 보강 기준 (`06`): 강한 버전관리 가능, 작은 배치 분할 가능, 사용자 중심 포커스 평균 이상
  - 산출물: `output/{project}/step3/2-portfolio-phase.md`
- Step 3-3. TCO 분석
  - As-Is TCO(기술 부채 비용 포함), To-Be TCO(클라우드·전환 투자·학습·병렬운영), BEP 산정(3·5년)
  - **DORA 권장 분리 항목** (`06`): 플랫폼 팀 인건비, AI 도구 라이선스, AI 컨텍스트 인프라(RAG/MCP), 데이터 생태계 정비, 변화관리·교육
  - 산출물: `output/{project}/step3/3-tco-bep.md`
- Step 3-4. 리스크 평가
  - 4영역(기술·조직·비즈니스·일정) × 발생확률·영향도 매트릭스, 상위 5개 리스크 완화 전략·책임자
  - DORA 2025 신규 리스크 추가 (`06`): AI 시스템 미진화 리스크, AM 부분 적용 시 AI ROI 잠금 실패, 사용자 중심 포커스 부재 리스크
  - 산출물: `output/{project}/step3/4-risk.md`
- Step 3-5. 거버넌스 + 품질/보안 가드레일
  - 5개 회의체(스티어링·워킹그룹·ARB·리스크·비용) 설계
  - Phase별 가드레일(SAST·SCA·회귀·Contract·DAST·Chaos), Phase 전환 게이트 조건
  - DORA 5메트릭 게이트 추가 (`01`, `06`) — Phase 전환 시 정량 측정 필수
  - **AI 정책 거버넌스 신설** (`07` 역량 1) — 3-bucket 정책 프레임워크
  - 산출물: `output/{project}/step3/5-governance-guardrail.md`
- Step 3-6. 변화관리 기획
  - Phase별 커뮤니케이션·교육 로드맵, 조직 구조·업무방식·문화·성과 측정 전환 계획
  - DORA "AI mirror" 메시지 라이브러리 활용 (`05`, `06`)
  - 90분 팀 우선순위 워크숍 가이드 도입 (`07`)
  - 지속적 개선 3대 원칙 (`07`): Celebrate Progress / Embrace Failure / Communities of Practice
  - 산출물: `output/{project}/step3/6-change-mgmt.md`
- Step 3-7. 전략 통합 보고서 작성
  - Step 1~3을 경영진·실무진용으로 통합 → `output/{project}/step3/strategy-report.md`
  - DORA 인용 모음 (`06`) — 경영진용 핵심 메시지 5장 + 직접 인용 권장 문구

### 최종 산출
- 최종 Review: WHY-현황-전략 정합성, 수치 일관성, 리스크 커버리지, Phase 게이트 조건 검증
- MS Word·PowerPoint 변환: 필요 시 인포그래픽 이미지 생성
  `output/{project}/final/strategy-report.docx` / `output/{project}/final/strategy-executive.pptx`

---

## 에이전트 구성

> 추천 근거: 핵심기능 4개(WHY/현황/전략/보고)와 사용자 플로우 STEP 1~3 + 최종 산출에서
> 도출되는 역할 클러스터를 분석하여 8개 에이전트로 구성. 동일 전문 영역 내에서
> 워크플로우가 독립적으로 분리되는 작업은 세부역할(sub-roles)로 캡슐화.

- **why-definer** (HIGH): WHY 정의 전문가 — 비즈니스 동인 도출, 기대 성과 L1 벤치마크 정량화,
  경영진 스폰서십 3단계 전략 수립 및 WHY 통합 보고서 작성 담당
  > 매칭 근거: STEP 1 전체(1-1~1-4)의 분석/설계/경영진 커뮤니케이션 역량 요구 → architect 계열 HIGH
  - **industry-benchmark**: 한국 공공부문 검증 데이터 ([`references/tco-benchmark/01`](references/tco-benchmark/01-public-sector.md) — 행안부 7년 TCO 18.4% 절감 등) +
    한국IDC 시장 전망 (`references/tco-benchmark/02`) + DORA 2025 글로벌 5메트릭 (`references/dora/01`) 통합 제공.
    한국 금융·제조·유통 업종별 정량 TCO 미확보 영역은 (`references/tco-benchmark/04`) 가이드대로 보충
  - **driver-mapper**: 기업이 제시한 비즈니스 이슈를 3S+보안+혁신 5개 동인으로 매핑.
    DORA 2025 동인별 근거 매핑 표 활용 (`references/dora/06`)

- **inventory-analyst** (MEDIUM): 시스템 인벤토리 및 건강도 평가 전문가 — 6개 카테고리 인벤토리 수집,
  4차원 스코어카드 평가, 기술 부채 비용 산정, A/B/C 등급 분류 담당
  > 매칭 근거: STEP 2-1~2-4의 데이터 수집·정량 평가 작업 → executor 계열 MEDIUM
  - **interview-template**: 비즈니스·개발·운영·재무팀별 인터뷰 질문지 생성
  - **code-scan-reader**: SonarQube/CAST Highlight 분석 결과 파싱 및 점수 변환
  - **dependency-mapper**: 시스템 간 연동·공유 DB·API 의존성을 그래프로 시각화

- **fit-analyzer** (HIGH): 전환 적합도·서비스 경계 식별 전문가 — 건강도→6R 매핑, TIME 모델 분류,
  Event Storming 워크숍 설계 및 Bounded Context·Context Map 도출 담당
  > 매칭 근거: STEP 2-5~2-6은 의사결정·도메인 모델링이 필요한 분석 작업 → architect 계열 HIGH
  - **event-storming-guide**: 도메인 이벤트 수집·분류·클러스터링 가이드 및 템플릿 제공
  - **6r-matcher**: 시스템 속성과 건강도 기반 6R 매칭 규칙 적용.
    [`references/6r/`](references/6r/) 룰북의 8단계 결정 알고리즘으로 일관된 추천 (Primary/Alternative 6R + TIME + 신뢰도 + rule_trace)

- **strategy-planner** (HIGH): 6R 전략·포트폴리오 수립 전문가 — 시스템별 실행안·예산 범위·기간 산정,
  전체 포트폴리오 Phase(0~4) 구성, 파일럿 대상 선정, GO/NO-GO 게이트 조건 설계 담당
  > 매칭 근거: STEP 3-1~3-2는 전략 수립과 의존성·일정 최적화 → planner 계열 HIGH
  - **budget-calculator**: 6R 전략별 투입 인력·기간·예비비 기반 예산 범위 계산
  - **phase-sequencer**: Phase 간 병렬·의존 관계 분석 및 일정 최적화

- **tco-analyst** (MEDIUM): TCO·BEP 분석 전문가 — As-Is TCO(기술 부채 비용 포함)·To-Be TCO 산정,
  BEP 3년/5년 계산, ROI 시각화 담당
  > 매칭 근거: STEP 3-3은 정량 모델링 중심 → executor 계열 MEDIUM
  - **cost-modeler**: 인프라·라이선스·인건비·장애·기회비용·병렬운영 비용 모델링

- **risk-governance** (HIGH): 리스크·거버넌스·가드레일 전문가 — 4영역 리스크 평가,
  발생확률×영향도 매트릭스, 5개 거버넌스 회의체 및 Phase별 품질/보안 가드레일(SAST·SCA·DAST·
  Contract·Chaos) 설계 담당
  > 매칭 근거: STEP 3-4~3-5는 위험 분석과 거버넌스 설계 → architect 계열 HIGH
  - **risk-matrix-tool**: 리스크 리스트 입력 시 매트릭스·히트맵 자동 생성
  - **guardrail-designer**: Phase별 CI/CD 파이프라인 단계·도구·실패 시 액션 설계

- **change-manager** (MEDIUM): 변화관리 전문가 — 이해관계자 맵, Phase별 커뮤니케이션 계획,
  교육·역량 로드맵, 조직 구조·업무방식·문화·성과 측정 전환 설계 담당
  > 매칭 근거: STEP 2-7 + STEP 3-6의 조직·커뮤니케이션 영역 → 도메인 특화 MEDIUM
  - **stakeholder-mapper**: 영향도·지지도 2×2 매트릭스 기반 이해관계자 분류

- **reviewer** (HIGH): 전략 검증 전문가 — WHY-현황-전략 3단계 정합성, 수치 일관성(TCO↔예산↔
  Phase 예산), 리스크 커버리지, 파일럿 선정 타당성, Phase 게이트 조건 충분성 검토 담당
  > 매칭 근거: 최종 Review 단계 — 별도 컨텍스트로 분리 실행하여 자체 산출물에 대한 독립적 검증
  > (`omc:execution_protocols`의 reviewer 분리 원칙 준수)

- **doc-exporter** (LOW): 문서 변환 전문가 (도메인 특화) — 최종 마크다운 전략 보고서를
  MS Word(.docx)·PowerPoint(.pptx)로 변환 출력 담당. 경영진용 요약본(30장 이내)과 실무진용
  상세본(100장 이상) 2종 출력. **(중요) 작성 전 사용자에게 출력 장수 질문 필수**
  > 매칭 근거: 최종 산출 단계의 단순 형식 변환 작업 → writer 계열 LOW

---

## 공유자원

> 매칭 근거 요약: 본 플러그인은 (1) 경영진용 PPT 출력, (2) 인포그래픽 이미지 생성,
> (3) Office 형식 입력 자료 처리, (4) 플러그인 README 작성이 필요하므로 아래 4개 자원을 매칭함.

### 외부 공유자원 (DMAP 마켓플레이스)

| 자원 유형 | 자원명 | 자원 경로 |
|----------|--------|------------|
| 가이드 | ppt-guide | {DMAP_PLUGIN_DIR}/resources/guides/docs/ppt-guide.md |
| 템플릿 | README-plugin-template | {DMAP_PLUGIN_DIR}/resources/templates/plugin/README-plugin-template.md |
| 샘플 | README | {DMAP_PLUGIN_DIR}/resources/samples/plugin/README.md |
| 도구 | generate_image | {DMAP_PLUGIN_DIR}/resources/tools/customs/general/generate_image.py |
| 도구 | convert-to-markdown | {DMAP_PLUGIN_DIR}/resources/tools/customs/general/convert-to-markdown.py |

### 플러그인 내장 참조 자료 (사전 수집·작성 완료)

| 자원 유형 | 자원명 | 자원 경로 |
|----------|--------|------------|
| 참조 자료 | DORA 2025 (사전 수집·분석) | `references/dora/` 디렉토리 (8개 파일 + 원본 PDF 2종) |
| 룰북 | 6R/TIME 매칭 룰북 | `references/6r/` 디렉토리 (7개 파일) |
| 벤치마크 | 한국 TCO 벤치마크 (2025+) | `references/tco-benchmark/` 디렉토리 (5개 파일) |

**DORA 2025 자료** (`references/dora/`):
- `README.md` — 인덱스 및 핵심 요약
- `01-software-delivery-performance.md` — 5개 지표 분포 (industry-benchmark용)
- `02-seven-team-profiles.md` — 7개 팀 클러스터 (inventory-analyst·fit-analyzer·change-manager용)
- `03-ai-capabilities-model.md` — 7개 AI 역량 개념 (why-definer·strategy-planner용)
- `04-platform-engineering.md` — 플랫폼 ROI (strategy-planner·tco-analyst용)
- `05-value-stream-management.md` — VSM 원칙 (fit-analyzer용)
- `06-am-transformation-implications.md` — AM 통합 시사점 (전체 에이전트용)
- `07-ai-capabilities-implementation.md` — 실행 가이드·측정·90분 워크숍 (strategy-planner·change-manager용)
- 원본 PDF: `2025_state_of_ai_assisted_software_development.pdf` (142p),
  `2025_dora_ai_capabilities_model.pdf` (97p)

**6R/TIME 매칭 룰북** (`references/6r/`):
- `README.md` — 인덱스 + 빠른 결정 트리
- `01-6r-definitions.md` — 6R 전략 정의·실행 방식·적합/부적합 기준 (`6r-matcher`, `strategy-planner`)
- `02-time-model.md` — TIME 2x2 매트릭스·축 정의·DORA 매핑 (`fit-analyzer`)
- `03-decision-criteria.md` — 14개 시스템 입력 속성 정의·점수화 기준 (`inventory-analyst`)
- `04-matching-rules.md` — 8단계 결정 알고리즘·STEP별 규칙·YAML 출력 양식 (`6r-matcher` 핵심)
- `05-cost-effort-risk-profile.md` — 6R별 비용·기간·인력·리스크·예비비 + 누락 빈도 항목 체크리스트 (`budget-calculator`, `cost-modeler`)
- `06-dora-integration.md` — 6R × DORA 2025 통합 + 변화관리 메시지 라이브러리 (전 에이전트)

**한국 TCO 벤치마크** (`references/tco-benchmark/`) — **2025년 이후 검증된 출처만 수록**:
- `README.md` — 출처 정책(Tier 1/2/3) + 인용 표기 의무 + 한 페이지 요약
- `01-public-sector.md` — 공공부문 (Tier 1) — 행정안전부 18.4% TCO·81% 장애 감소·114% 처리속도 (2026.03.11) + 근로복지공단 23배 응답 개선 (2025.12.23)
- `02-market-overview.md` — 한국IDC 2025년 클라우드 시장 10대 전망 (2025.01.31) — 시장 3조 8,952억원·CAGR 14.8%
- `03-financial-sector.md` — 금융권 (Tier 2) — 삼정KPMG 2025 디지털금융 7대 이슈 (정성적, 정량 미수록 명시)
- `04-data-gap-and-supplement.md` — **데이터 공백 영역 (제조·유통)** + DORA 2025 글로벌 보충 가이드 + 보고서 한계 표기 권장 문구

### 적합성 이유

| 자원 | 적합성 |
|------|--------|
| `ppt-guide` | 최종 산출물에 경영진 발표용 PowerPoint(.pptx)가 포함됨. PPT 컬러 팔레트·타이포그래피·레이아웃 표준 준수를 위해 필수 |
| `README-plugin-template` | 플러그인 자체 배포 시 표준 README 작성에 활용 |
| `README` (샘플) | Abra 플러그인의 README 작성 예시를 참고하여 일관된 문서 품질 유지 |
| `generate_image` | "최종 산출 → 필요 시 인포그래픽 이미지 생성" 요구사항에 직접 대응. 경영진 PPT의 다이어그램·인포그래픽 자동 생성 |
| `convert-to-markdown` | `references/am-strategy/`의 입력 자료가 추가 Office 문서(인터뷰 자료, 인벤토리 엑셀 등)로 확장될 경우를 대비한 입력 변환 |
| `references/dora/` | DORA 2025 보고서 2종(239페이지)을 AM 전략 수립 관점에서 분석·정리. WHY 정량화·시스템 진단·6R 매핑·플랫폼 투자·VSM·변화관리 등 전 단계에 직접 활용 |
| `references/6r/` | 6R/TIME 매칭 룰북 (7개 파일). `6r-matcher` 세부역할이 14개 시스템 속성 입력 → 8단계 알고리즘 → Primary/Alternative 6R + TIME + 신뢰도 + rule_trace 출력. DORA 2025 통합 (변화관리 메시지·AI ROI·플랫폼 투자 가이드 포함) |
| `references/tco-benchmark/` | 한국 TCO 벤치마크 (5개 파일). **2025년 이후 검증된 1차 정부·2차 산업 보고서만 수록**. 공공부문은 정량 데이터(행안부 18.4% 등) 충실, 금융·제조·유통은 데이터 공백 명시 + DORA 보충 가이드. 모든 수치에 출처(발표 주체·일자·URL) 명기 — 산출물에 직접 인용 가능 |

### 매칭 결과 없음 (직접 작성 필요)

- **md → docx/pptx 변환 도구**: 마켓플레이스에 출력 방향(md → Office) 변환 도구가 없음.
  `doc-exporter` 에이전트가 anthropic-skills의 `docx`/`pptx` 스킬을 활용하거나
  플러그인 내 커스텀 변환 스크립트를 직접 작성 필요
- **금융·제조·유통 업종별 정량 TCO 벤치마크 데이터**: 2025년 이후 공개된 한국 업종별
  정량 TCO 자료 부재 확인. `references/tco-benchmark/04-data-gap-and-supplement.md` 의
  4가지 보충 옵션 (가트너 컨설팅·한국IDC 맞춤·동종업계·DORA 글로벌) 중 선택 필요

---

## 비기능 요구사항

- **이식성**: DMAP 기반으로 Claude Code·Cursor·Cowork 어디서나 동작 (`gateway/runtime-mapping.yaml`)
- **보안/컴플라이언스**: 고객 데이터·개인정보를 플러그인 외부로 전송하지 않음.
  외부 벤치마크 데이터만 참조. 인벤토리 수집 시 민감 속성은 마스킹 권장 안내
- **증거 기반**: 모든 정량 지표는 출처(벤치마크 리포트·내부 측정값·파일럿 실측)를 명시
- **경영진 소통**: 최종 보고서는 경영진이 이해할 수 있는 용어로 작성 —
  "왜(WHY) → 얼마(TCO/BEP) → 언제(Phase) → 어떻게(6R) → 위험(Risk/완화)" 순서 고정

---

## 성공 기준

| 구분 | 성공 기준 |
|------|---------|
| 완결성 | WHY·현황·전략 3단계 모든 산출물이 체크리스트 100% 충족 |
| 정량화 | 기대 성과·TCO·BEP가 **범위**로 제시(단일 숫자 금지), 근거 출처 명시 |
| 실행 가능성 | Phase 1·1' 파일럿 대상·일정·예산이 4주 내 착수 가능한 수준으로 구체화 |
| 거버넌스 | 5개 회의체·3개 Gate·Phase별 가드레일이 조직 현실 기반으로 제안 |
| 변화관리 | Phase별 커뮤니케이션·교육·조직 전환 로드맵 포함, 실패 1위 원인(조직) 대응 명시 |
| 산출 형식 | 마크다운 + MS Word + PowerPoint 3종 일관성 유지 |
