# FinOps KPI 대시보드 템플릿

> (주)하이브리지텔레콤 (HBT) — FinOps Operate Phase KPI 대시보드  
> 기준일: 2026-04-19 | 측정 주기: 주간·월간  
> 참조: finops.md §4.12, gate-criteria.yaml

---

## CSP KPI (클라우드 인프라 효율성 3종)

| KPI ID | 지표명 | 계산식 | 기준값(Baseline) | 목표값(Target) | 측정 주기 | 데이터 소스 | 담당 에이전트 |
|--------|--------|--------|----------------|--------------|---------|-----------|-------------|
| KPI-CSP-1 | 태깅 커버리지 | (태그 4종 완비 리소스 수 / 전체 리소스 수) × 100 | 96.12% | ≥ 95% | 주간 | focus-normalized.csv (Tags 컬럼) | tag-governor |
| KPI-CSP-2 | RI/SP 활용률 | (CommitmentDiscountStatus=Used EffectiveCost 합) / (Used+Unused EffectiveCost 합) × 100 | 측정 시작 | ≥ 80% | 월간 | focus-normalized.csv (CommitmentDiscountStatus) | commit-planner |
| KPI-CSP-3 | 이상 탐지 응답 시간 | 이상 비용 알림 발송 시각 − 이상 비용 발생 시각 (시간 단위) | 측정 시작 | ≤ 24h | 이벤트별 | CSP 청구 데이터 + Slack #finops-review 타임스탬프 | cost-analyst |

---

## AI KPI (AI/LLM 비용 효율성 3종)

| KPI ID | 지표명 | 계산식 | 기준값(Baseline) | 목표값(Target) | 측정 주기 | 데이터 소스 | 담당 에이전트 |
|--------|--------|--------|----------------|--------------|---------|-----------|-------------|
| KPI-AI-1 | GPU 활용률 | (실제 GPU 사용 시간 / 프로비저닝 GPU 시간) × 100 | 측정 시작 | ≥ 60% | 주간 | GCP Billing + Vertex AI 사용 로그 (utilization-sample.csv) | rightsize-advisor |
| KPI-AI-2 | AI 비용/토큰 | AI 총 비용(KRW) / 총 토큰 수(입력+출력, 백만 단위) | 843,695 KRW / 측정 시작 | 전월 대비 ≥ 5% 감소 | 월간 | focus-normalized.csv (ServiceName=Anthropic API·Vertex AI) + API 호출 로그 | finops-practitioner |
| KPI-AI-3 | 모델 효율 (유효 출력률) | 유효 출력 토큰 수 / (입력 + 출력) 총 토큰 수 × 100 | 측정 시작 | ≥ 70% | 월간 | LLM API 응답 로그 (ModelName 태그 연계) | finops-practitioner |

---

## HBT 사업 포트폴리오 단위경제 KPI (LoB별)

| LoB | 단위경제 지표 | 계산식 | 목표 | 데이터 소스 |
|-----|------------|--------|------|-----------|
| MNO | 가입자당 클라우드 비용 | 월 클라우드 비용(KRW) / MNO 활성 가입자 수 | 전월 대비 감소 | AWS CUR + 가입자 DB |
| MVNO | MVNO 회선당 비용 | CC-100 월 비용(KRW) / MVNO 활성 회선 수 | 전월 대비 감소 | Azure Cost Mgmt + MVNO 시스템 |
| IoT | IoT 디바이스당 비용 | IoT 관련 월 비용(KRW) / 활성 디바이스 수 | 전월 대비 감소 | GCP Billing + IoT 플랫폼 |
| B2B | API 호출 100만 건당 비용 | CC-200 월 비용(KRW) / (API 호출 수 ÷ 1,000,000) | 전월 대비 감소 | API Gateway CloudWatch + 비용 데이터 |

---

## 게이트 기준 현황 (gate-criteria.yaml 기준)

| 게이트 ID | 지표명 | 기준 | 현재값 | 판정 |
|---------|--------|------|--------|------|
| TAGGING_COVERAGE | 태깅 커버리지 | ≥ 95% | 96.12% | O 통과 |
| FORECAST_MAPE | 비용 예측 MAPE | ≤ 10% | 측정 시작 | — 미측정 |
| RI_UTILIZATION | RI/SP 활용률 | ≥ 80% | 측정 시작 | — 미측정 |
| ANOMALY_DETECT_LATENCY | 이상 탐지 지연 | ≤ 24h | 측정 시작 | — 미측정 |
| IDLE_RESOURCE_RATE | 유휴 리소스 비율 | ≤ 3% | 측정 시작 | — 미측정 |
| GPU_UTILIZATION | GPU 활용률 | ≥ 60% | 측정 시작 | — 미측정 |

> 상태 표시: O 통과 / X 미달 / — 미측정 / ~ 개선 중
