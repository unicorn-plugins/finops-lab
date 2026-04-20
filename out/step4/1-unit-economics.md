# 단위경제 KPI 6종 분석

**작성일**: 2026-04-19  
**작성자**: 최운영/프랙티셔너 (FinOps Operate)  
**참조**: finops.md §4.12, gate-criteria.yaml, out/step2/4-tag-coverage.md  
**HBT 사업 포트폴리오**: MNO · MVNO · IoT · B2B

---

## 1. KPI 설계 배경

HBT는 월 42,256,382 KRW(2,335행 FOCUS 데이터 기준) 규모의 멀티클라우드(AWS·Azure·GCP) 운영 조직임.  
현재 rightsize-plan.md 기준 월 9,724,250 KRW 절감 기회가 식별된 상태이며,  
commit-strategy.md의 Conservative/Base/Optimistic 시나리오 BEP 28~36개월 달성을 위해  
단위경제 기반의 지속 가능한 비용 거버넌스 체계 수립이 요구됨.

단위경제 KPI는 **"총 비용 증가 ≠ FinOps 실패"** 원칙 아래, 비즈니스 성장을 수반한  
단위당 비용 감소를 목표로 설계함 (finops.md §4.12 준거).

---

## 2. CSP KPI 3종 (클라우드 인프라 효율성)

### KPI-CSP-1: 태깅 커버리지

| 항목 | 내용 |
|------|------|
| **계산식** | (태그 4종 완비 리소스 수 / 전체 리소스 수) × 100 |
| **기준값** | 96.12% (현재 측정값, 2026-04-19) |
| **목표값** | ≥ 95% (gate-criteria.yaml TAGGING_COVERAGE 기준) |
| **측정 주기** | 주간 (매주 월요일) |
| **데이터 소스** | focus-normalized.csv Tags 컬럼 (Project·Environment·Owner·CostCenter 4종) |
| **HBT 맥락** | Project 96.45%·Environment 100%·Owner 97.26%·CostCenter 95.76%. 현재 게이트 **통과** 상태. AWS dev 환경(91.84%)이 약점 — 레거시 인스턴스 64개 미태깅 |

**세부 현황 (out/step2/4-tag-coverage.md 기준)**

| CSP | 종합 커버리지 | 주요 미태깅 원인 |
|-----|------------|--------------|
| AWS | ~92% (dev 환경 약점) | 레거시 리소스(i-legacy-001 등) Project·Owner 누락 |
| Azure | ~98% | 개발/스테이징 CostCenter 미귀속 |
| AI 리소스 | 미적용 | Anthropic API LLMApiKey·ModelName·ChargebackUnit 3종 미적용 |

---

### KPI-CSP-2: RI/SP 활용률

| 항목 | 내용 |
|------|------|
| **계산식** | (CommitmentDiscountStatus=Used EffectiveCost 합) / (Used+Unused EffectiveCost 합) × 100 |
| **기준값** | 측정 시작 단계 (commit-strategy.yaml Conservative 시나리오 적용 예정) |
| **목표값** | ≥ 80% (gate-criteria.yaml RI_UTILIZATION 기준) |
| **측정 주기** | 월간 (매월 첫째 주 화요일) |
| **데이터 소스** | focus-normalized.csv CommitmentDiscountStatus 컬럼 |
| **HBT 맥락** | commit-strategy.md Base 시나리오(BEP 36개월) 기준 RI 구매 집행 후 활용률 추적 시작. 활용률 60% 미만 시 RI 추가 구매 즉시 중단 |

---

### KPI-CSP-3: 이상 탐지 응답 시간

| 항목 | 내용 |
|------|------|
| **계산식** | 이상 비용 알림 발송 시각 − 이상 비용 발생 시각 (시간 단위, 이벤트별 최대값) |
| **기준값** | 측정 시작 단계 |
| **목표값** | ≤ 24h (gate-criteria.yaml ANOMALY_DETECT_LATENCY 기준) |
| **측정 주기** | 이벤트별 실시간 측정 + 월간 집계 |
| **데이터 소스** | CSP 청구 데이터(AWS·Azure·GCP 일별 데이터) + Slack #finops-review 채널 알림 타임스탬프 |
| **HBT 맥락** | 탐지 임계값: 전주 동기간 대비 +20% 이상 급증. AWS EC2 c5.2xlarge 3배 급등(2026-03-15) 사례 대응 시간을 Baseline으로 설정 |

---

## 3. AI KPI 3종 (AI/LLM 비용 효율성)

### KPI-AI-1: GPU 활용률

| 항목 | 내용 |
|------|------|
| **계산식** | (실제 GPU 사용 시간 / 프로비저닝 GPU 시간) × 100 |
| **기준값** | 측정 시작 단계 (Vertex AI 추가 도입 예정 2026년 3분기) |
| **목표값** | ≥ 60% (gate-criteria.yaml GPU_UTILIZATION 기준) |
| **측정 주기** | 주간 |
| **데이터 소스** | GCP Billing + Vertex AI 사용 로그, utilization-sample.csv |
| **HBT 맥락** | 현재 GCE gce-idle-1(n2-standard-4, CPU 20% 유지)이 과잉 프로비저닝 상태. AI 워크로드 GPU 유휴 시간 최소화 목표. ML 학습 1회당 비용(GCP 비용 ÷ 학습 실행 횟수) 연동 측정 |

---

### KPI-AI-2: AI 비용/토큰 (백만 토큰당 비용)

| 항목 | 내용 |
|------|------|
| **계산식** | AI 총 비용(KRW) / 총 토큰 수(입력+출력, 백만 단위) |
| **기준값** | AI 리소스 월 843,695 KRW (Anthropic API + Vertex AI, 2026-04-19) |
| **목표값** | 전월 대비 ≥ 5% 감소 (YAML 미정의, State of FinOps 2026 §4.2 AI 비용 가시성 기준 자체 설정) |
| **측정 주기** | 월간 |
| **데이터 소스** | focus-normalized.csv (ServiceName=Anthropic API·Vertex AI) + LLM API 호출 로그 |
| **HBT 맥락** | Anthropic API Project 태그 미적용 → 먼저 ChargebackUnit(CC-300) 태그 적용 후 측정 시작. AI 지출 관리율 98%(State of FinOps 2026) 트렌드 대응 |

---

### KPI-AI-3: 모델 효율 (유효 출력률)

| 항목 | 내용 |
|------|------|
| **계산식** | 유효 출력 토큰 수 / (입력 + 출력) 총 토큰 수 × 100 |
| **기준값** | 측정 시작 단계 (LLM API 응답 로그 수집 체계 구축 후) |
| **목표값** | ≥ 70% (YAML 미정의, State of FinOps 2026 §4.2 AI 비용 가시성 기준 자체 설정) |
| **측정 주기** | 월간 |
| **데이터 소스** | LLM API 응답 로그 (ModelName 태그 연계 — anthropic-claude·google-vertex-ai-gemini) |
| **HBT 맥락** | 불필요한 입력 토큰(과잉 컨텍스트·시스템 프롬프트 비대화) 탐지 및 개선 목표. 모델 다운그레이드(Claude Sonnet → Haiku 등) ROI 측정에 활용 |

---

## 4. Ownership별 KPI 연결 관계

FinOps 6대 원칙(COVERS) 중 **Ownership** 원칙에 따라, 각 KPI를 재무·엔지니어링·경영진 3개 Ownership으로 연결함.

| Ownership | 연결 KPI | 책임 내용 | 리뷰 주기 |
|-----------|---------|---------|---------|
| **재무팀** | KPI-CSP-2 (RI/SP 활용률), KPI-AI-2 (AI 비용/토큰) | 예산 대비 실적 관리, RI 구매 ROI 분석, AI 비용 ChargebackUnit별 배분 | 월간 |
| **엔지니어링팀** | KPI-CSP-1 (태깅 커버리지), KPI-CSP-3 (이상 탐지 응답), KPI-AI-1 (GPU 활용률), KPI-AI-3 (모델 효율) | 태그 정책 준수, 이상 비용 대응, GPU 스케줄링 최적화, 프롬프트 엔지니어링 | 주간 |
| **경영진** | 전체 6종 KPI + HBT LoB 단위경제 4종 | 전략 정렬(MNO·MVNO·IoT·B2B 비용 vs 매출), Crawl→Walk 전환 투자 승인 | 분기 |

### HBT LoB별 Ownership 매핑

| LoB | 단위경제 지표 | 비용 Ownership | 엔지니어링 Ownership |
|-----|------------|--------------|------------------|
| MNO | 가입자당 클라우드 비용 | 재무팀 + MNO 사업팀 | 인프라운영팀 (CC-100) |
| MVNO | MVNO 회선당 비용 | 재무팀 + MVNO 사업팀 | 인프라운영팀 (CC-100) |
| IoT | IoT 디바이스당 비용 | 재무팀 + B2B 사업팀 | 서비스개발팀 (CC-200) |
| B2B | API 호출 100만 건당 비용 | 재무팀 + B2B 사업팀 | 서비스개발팀 (CC-200) + 데이터/AI팀 (CC-300) |

---

## 5. KPI 6종 목표값 요약

| KPI ID | 지표명 | 목표값 | 게이트 기준 ID | 현재 판정 |
|--------|--------|--------|--------------|---------|
| KPI-CSP-1 | 태깅 커버리지 | ≥ 95% | TAGGING_COVERAGE | O 통과 (96.12%) |
| KPI-CSP-2 | RI/SP 활용률 | ≥ 80% | RI_UTILIZATION | — 측정 시작 |
| KPI-CSP-3 | 이상 탐지 응답 시간 | ≤ 24h | ANOMALY_DETECT_LATENCY | — 측정 시작 |
| KPI-AI-1 | GPU 활용률 | ≥ 60% | GPU_UTILIZATION | — 측정 시작 |
| KPI-AI-2 | AI 비용/토큰 | 전월 대비 ≥ 5% 감소 | (FORECAST_MAPE 연계) | — 측정 시작 |
| KPI-AI-3 | 모델 효율 (유효 출력률) | ≥ 70% | — | — 측정 시작 |
