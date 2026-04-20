# Crawl → Walk → Run 전환 로드맵 (12개월)

**작성일**: 2026-04-19  
**작성자**: 최운영/프랙티셔너 (FinOps Operate)  
**참조**: finops.md §4.14, gate-criteria.yaml §walk_stage_criteria, State of FinOps 2026  
**대상**: (주)하이브리지텔레콤 (HBT) | 목표: Crawl → Walk (1년 내 달성)

---

## 1. 전환 로드맵 개요

HBT는 현재 **Crawl 단계** 진입 상태임.  
태깅 커버리지 96.12%로 게이트 1개 통과, 나머지 게이트(FORECAST_MAPE·RI_UTILIZATION·ANOMALY_DETECT_LATENCY·IDLE_RESOURCE_RATE·GPU_UTILIZATION)는 측정 시작 단계임.

**12개월 목표**: gate-criteria.yaml의 walk_stage_criteria 5개 게이트 모두 통과 → Crawl→Walk 전환 인정

```
2026년 4월          2026년 7월          2026년 10월         2027년 4월
     │                   │                   │                   │
  [Crawl 기초]       [Crawl 완성]         [Walk 진입]         [Walk 완성]
  기반 체계 구축      자동화 파이프라인     최적화 실행          거버넌스 내재화
  KPI 측정 시작       전 게이트 측정       게이트 달성 시작      Run 준비
```

---

## 2. Crawl 단계 (0~3개월: 2026년 4월~6월)

### 단계 목표

비용 가시성 확보 완성 + 자동화 파이프라인 구축 + KPI 측정 체계 수립

### 분기별 마일스톤

| 월 | 마일스톤 | 완료 기준 |
|----|---------|---------|
| 4월 (현재) | 태깅 커버리지 96.12% 유지·개선 | TAGGING_COVERAGE ≥ 95% 3주 연속 |
| 4월 | AI 리소스 태그 적용 | Anthropic API·Vertex AI LLMApiKey·ModelName·ChargebackUnit 3종 100% 적용 |
| 5월 | 자동화 파이프라인 1~4단계 구축 | 데이터수집→정규화→분석→알림 일 1회 자동 실행 |
| 5월 | KPI 측정 시작 | KPI-CSP-1~3·KPI-AI-1~3 전종 측정값 최초 생성 |
| 5월 | 예산 경보 자동화 전 프로젝트 적용 | 전 프로젝트 Budget Alert 100% 설정 |
| 6월 | 월간 FinOps 리뷰 3개월 연속 운영 시작 | review-runbook.md 월간 리뷰 2회 완료 |
| 6월 | ANOMALY_DETECT_LATENCY 측정 시작 | 이상 이벤트 5건 이상 측정·기록 |

### Crawl 단계 Ownership

| 역할 | 담당 에이전트 | 책임 |
|------|------------|------|
| **재무** | finops-practitioner (프랙티셔너) | KPI 측정 체계 수립, 예산 경보 설정 |
| **엔지니어링** | tag-governor (태거) + cost-analyst | AI 태그 적용, 파이프라인 구축 |
| **경영진** | CTO 스폰서십 | 파이프라인 구축 리소스 승인 |

### Crawl 단계 성공 지표

- TAGGING_COVERAGE ≥ 95% 지속 유지
- KPI 6종 전종 측정값 최초 생성 (베이스라인 확정)
- 자동화 파이프라인 1~4단계 일 1회 정상 실행 30일 연속
- 예산 경보 자동화 전 프로젝트 적용 완료
- 월간 FinOps 리뷰 2회 완료

---

## 3. Walk 단계 전환 준비 (4~8개월: 2026년 7월~11월)

### 단계 목표

게이트 6종 목표값 달성 + 최적화 실행 + 단위경제 KPI 개선 추이 확보

### 분기별 마일스톤

| 월 | 마일스톤 | 완료 기준 |
|----|---------|---------|
| 7월 | ANOMALY_DETECT_LATENCY ≤ 24h 달성 | 연속 3개월 이상 이벤트 평균 탐지 시간 ≤ 24h |
| 7월 | IDLE_RESOURCE_RATE 측정 및 10% 미만 달성 | 전체 유휴 리소스 비율 10% 이하로 감소 |
| 8월 | rightsize-plan.md 대안A 실행 완료 | 월 9,724,250 KRW 절감 실현(비운영→운영 환경 순차) |
| 8월 | commit-strategy.md Base 시나리오 RI 구매 시작 | RI 구매 완료 + RI_UTILIZATION 측정 시작 |
| 9월 | FORECAST_MAPE ≤ 10% 달성 | 월간 비용 예측 MAPE 10% 이내 2개월 연속 |
| 9월 | IDLE_RESOURCE_RATE ≤ 3% 달성 | 유휴 리소스 비율 3% 이하 달성 |
| 10월 | RI_UTILIZATION ≥ 80% 달성 | RI/SP 활용률 80% 이상 2개월 연속 |
| 10월 | GPU_UTILIZATION ≥ 60% 달성 | GPU 활용률 60% 이상 4주 연속 |
| 11월 | HBT LoB 단위경제 4종 개선 추이 확보 | MNO·MVNO·IoT·B2B 단위당 비용 3개월 연속 감소 또는 유지 |

### Walk 단계 전환 준비 Ownership

| 역할 | 담당 에이전트 | 책임 |
|------|------------|------|
| **재무** | commit-planner (커밋터) + finops-practitioner | RI 구매 의사결정, 예측 모델 정확도 관리 |
| **엔지니어링** | rightsize-advisor (라이트사이저) + cost-analyst | 유휴 리소스 제거, Right-sizing 실행, 이상 탐지 SLA 준수 |
| **경영진** | CTO/CFO | RI 구매 시나리오 승인 (commit-strategy.md Base 시나리오), 절감 성과 확인 |

### Walk 단계 전환 준비 성공 지표

- 자동화 파이프라인 5단계(액션) 포함 전체 운영 안정화
- FORECAST_MAPE ≤ 10% 달성 후 2개월 연속 유지
- IDLE_RESOURCE_RATE ≤ 3% 달성
- ANOMALY_DETECT_LATENCY ≤ 24h 달성 후 3개월 연속 유지
- 월간 절감 실적 ≥ 5,000,000 KRW (3개월 누적 ≥ 15,000,000 KRW)

---

## 4. Walk 단계 완성 (9~12개월: 2026년 12월~2027년 3월)

### 단계 목표

gate-criteria.yaml §walk_stage_criteria 5개 게이트 전체 통과 → Walk 전환 공식 인정  
Run 단계 진입 기반 구축 (엔지니어 셀프서비스, 예측 기반 의사결정 체계 준비)

### 분기별 마일스톤

| 월 | 마일스톤 | 완료 기준 |
|----|---------|---------|
| 12월 | Walk 전환 공식 판정 | walk_stage_criteria 5개 게이트 전체 통과 + 월간 리뷰 3개월 연속 운영 |
| 12월 | RI_UTILIZATION ≥ 80% Walk 완성 | RI 구매 후 활용률 80% 이상 3개월 연속 유지 |
| 1월 | 팀별 비용 책임 체계(Chargeback) 도입 | CC-100/200/300별 Chargeback 모델 운영 시작 |
| 2월 | 엔지니어 셀프서비스 대시보드 구축 | 서비스별 비용 대시보드 팀별 접근 권한 부여 |
| 2월 | KPI-AI-2·AI-3 목표값 달성 | AI 비용/토큰 전월 대비 5% 감소·모델 효율 ≥ 70% |
| 3월 | Run 단계 진입 준비 완료 | 실시간 비용 거버넌스 프로토타입 + 예측 기반 의사결정 첫 사례 |

### Walk 완성 단계 Ownership

| 역할 | 담당 에이전트 | 책임 |
|------|------------|------|
| **재무** | finops-practitioner (프랙티셔너) + 재무팀 | Chargeback 모델 운영, Walk 전환 공식 보고 |
| **엔지니어링** | 전 에이전트 팀 | 셀프서비스 대시보드 구축, 자동화 고도화 |
| **경영진** | CTO/CFO | Walk 전환 공식 인정, Run 단계 투자 결정 |

### Walk 단계 완성 성공 지표 (walk_stage_criteria 전체)

- TAGGING_COVERAGE ≥ 95% — 12개월 연속 유지 (**필수**)
- FORECAST_MAPE ≤ 10% — 6개월 이상 유지 (**필수**)
- ANOMALY_DETECT_LATENCY ≤ 24h — 6개월 이상 유지 (**필수**)
- RI_UTILIZATION ≥ 80% — Walk 달성 후 3개월 내 달성 (**권장**)
- IDLE_RESOURCE_RATE ≤ 3% — 달성 후 유지 (**권장**)
- 월간 FinOps 리뷰 3개월 연속 운영 (**추가 요건**)
- 단위경제 KPI 3종 측정 시작 (**추가 요건**)
- 전 프로젝트 예산 경보 자동화 적용 (**추가 요건**)

---

## 5. 12개월 전환 마일스톤 요약

| 분기 | 단계 | 핵심 마일스톤 | 게이트 달성 목표 | Ownership |
|------|------|------------|--------------|---------|
| Q2 2026 (4~6월) | Crawl 기반 구축 | 파이프라인 1~4단계 구축, AI 태그 적용, KPI 측정 시작 | TAGGING_COVERAGE 유지 | 엔지니어링 주도 |
| Q3 2026 (7~9월) | Crawl→Walk 전환 시작 | ANOMALY·IDLE·FORECAST 게이트 달성, 절감 실현 | +3개 게이트 달성 | 재무·엔지니어링 협업 |
| Q4 2026 (10~12월) | Walk 진입 완성 | RI·GPU 게이트 달성, Walk 공식 판정 | 전 게이트 통과 | 경영진 승인 |
| Q1 2027 (1~3월) | Walk 거버넌스 내재화 | Chargeback 도입, 셀프서비스 구축, Run 준비 | 유지 + Run 기반 | 전사 내재화 |

---

## 6. 성숙도 전환 리스크 및 대응

| 리스크 | 발생 가능성 | 영향도 | 대응 방안 |
|--------|-----------|--------|---------|
| FORECAST_MAPE 달성 지연 | 중 | 중 | Walk 전환 조건 중 권장으로 조정 검토 후 필수 유지 원칙 재확인, 데이터 품질 선행 개선 |
| RI_UTILIZATION 저하 | 중 | 높음 | commit-strategy.md Conservative 시나리오로 하향 조정, 소규모 RI 선구매 후 활용률 모니터링 |
| AI 비용 급증 | 높음 | 중 | KPI-AI-2·AI-3 조기 측정 시작, 모델 다운그레이드 대안 즉시 실행, GPU 예산 Cap 설정 |
| 조직 저항 (Chargeback 도입) | 중 | 중 | Showback 선행 → 3개월 후 Chargeback 전환, 팀별 인센티브 설계 병행 |
| 경영진 관심 약화 | 낮음 | 높음 | 분기 리뷰에 ROI 수치(절감 실적 누적) 전면 배치, 단위경제 사업 연결 스토리 강화 |

---

## 7. Run 단계 진입 조건 (참고, 12개월 이후 목표)

Run 단계는 본 로드맵 범위 외이나 방향성 참조용으로 기술함.

- 실시간 비용 거버넌스 (준실시간 대시보드, 자동 최적화 파이프라인 완전 자동화)
- 예측 기반 의사결정 (MAPE ≤ 5%, 30일 선행 예측 신뢰도 확보)
- 엔지니어 셀프서비스 (팀별 비용 대시보드 + 자동 권고 수신 체계)
- FinOps 문화 내재화 (전사 FinOps 교육 이수율 ≥ 80%, 팀별 KPI 책임 체계 완성)
- AI/SaaS Scope 확장 (AI 비용 관리 98% 수준 달성, SaaS 라이선스 포함 통합 관리)
