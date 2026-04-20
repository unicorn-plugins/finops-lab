# 자동화 파이프라인 5단계 설계서

**작성일**: 2026-04-19  
**작성자**: 최운영/프랙티셔너 (FinOps Operate)  
**참조**: finops.md §4.11, gate-criteria.yaml  
**대상**: (주)하이브리지텔레콤 (HBT) 멀티클라우드(AWS·Azure·GCP) + AI(Anthropic·Vertex AI)

---

## 1. 파이프라인 개요

FinOps 자동화 파이프라인은 **데이터수집 → 정규화 → 분석 → 알림 → 액션** 5단계로 구성됨.  
각 단계는 독립적으로 실행 가능하며, 실패 시 하위 단계로 전파되지 않도록 격리 설계함.

```
[1단계: 데이터수집] → [2단계: 정규화] → [3단계: 분석] → [4단계: 알림] → [5단계: 액션]
     ↓실패                  ↓실패              ↓실패            ↓실패            ↓실패
  백업수집                수동큐              수동검토         백업채널         자동롤백
```

---

## 2. 5단계 파이프라인 상세 설계

### 1단계: 데이터수집 (Data Collection)

| 항목 | 내용 |
|------|------|
| **트리거** | 일별 자동 스케줄 (AWS: 매일 02:00 KST / Azure: 매일 03:00 KST / GCP: 준실시간) |
| **도구** | AWS CUR 2.0 → S3 버킷, Azure Cost Management Exports → Blob Storage, GCP Cloud Billing Export → BigQuery |
| **수집 대상** | CSP 청구 데이터(일별) + AI API 호출 로그(Anthropic API·Vertex AI) + GPU 사용률 데이터 |
| **출력** | 원시 청구 데이터 랜딩 존 적재 (S3·Blob·BigQuery) |
| **SLA** | 당일 데이터 T+6시간 이내 수집 완료 |

**실패 액션**
- 수집 실패 탐지: CloudWatch·Azure Monitor·GCP Alerting 으로 수집 지연 감지
- 즉시 조치: 백업 수집 경로(CSP 콘솔 수동 export) 전환 + 담당자(cost-analyst) Slack 알림
- 에스컬레이션: 24시간 이내 미복구 시 FinOps팀장 에스컬레이션 + Jira 인시던트 생성 (`finops-data-collection-fail`)

---

### 2단계: 정규화 (Normalization)

| 항목 | 내용 |
|------|------|
| **트리거** | 1단계 수집 완료 이벤트 (S3 PutObject·Blob Event·BigQuery 테이블 업데이트) |
| **도구** | FOCUS v1.3 정규화 파이프라인 (Python ETL), AI 확장 5종 스키마(LLMApiKey·ModelName·ChargebackUnit·TokenCount·GPUHours) 적용 |
| **처리 내용** | CSP별 상이한 컬럼 스키마 → FOCUS 통일 포맷 변환, 환율 적용(KRW 환산, ₩1,500/$1), AmortizedCost 계산 |
| **출력** | focus-normalized.csv 업데이트 (2,335행+ 증분 적재) |
| **SLA** | 수집 완료 후 2시간 이내 정규화 완료 |

**실패 액션**
- 정규화 오류 탐지: 스키마 검증 실패·행 수 이상 시 파이프라인 중단 + 오류 로그 생성
- 즉시 조치: 실패 데이터를 수동 검토 큐로 이동 + cost-analyst·tag-governor 알림
- 에스컬레이션: 2회 연속 실패 시 데이터 엔지니어링팀 에스컬레이션 + 파이프라인 코드 검토 태스크 생성

---

### 3단계: 분석 (Analysis)

| 항목 | 내용 |
|------|------|
| **트리거** | 2단계 정규화 완료 이벤트 + 주간/월간 스케줄 |
| **도구** | AWS Cost Anomaly Detection, Azure Cost Alerts, GCP Budget Alerts, rightsize-advisor 룰셋, KPI 계산 쿼리(SQL on BigQuery/Athena) |
| **분석 항목** | ① 이상 비용 탐지 (전주 동기간 대비 +20% 이상) — σ 기반 통계 탐지 포함 ② KPI-CSP-1~3·KPI-AI-1~3 현황 계산 ③ 유휴 리소스 스캔 (CPU < 5%, 7일 이상) ④ RI/SP 활용률 계산 |
| **출력** | 이상 이벤트 목록 + KPI 현황 데이터 + 최적화 권고 목록 |
| **SLA** | 정규화 완료 후 1시간 이내 분석 완료 |

**실패 액션**
- 분석 오류 탐지: KPI 계산 쿼리 실행 실패·분석 서비스 장애
- 즉시 조치: 전회 분석 결과 유지 + 수동 검토 큐로 이동 + finops-practitioner 알림
- 에스컬레이션: 분석 지연이 ANOMALY_DETECT_LATENCY 24h SLA 위협 시 FinOps팀장 즉시 보고

---

### 4단계: 알림 (Alert)

| 항목 | 내용 |
|------|------|
| **트리거** | 3단계 분석 결과에서 이상 이벤트·KPI 미달 탐지 |
| **도구** | Slack 알림 (#finops-review 채널), Jira/ServiceNow 티켓 자동 생성, 이메일 백업 알림 |
| **알림 유형** | ① 이상 비용 발생 알림 (즉시, Slack + Jira `finops-anomaly-sla`) ② KPI 미달 알림 (주간, 담당 에이전트별) ③ 게이트 미달 알림 (월간, 게이트별 책임 에이전트) ④ 예산 초과 경보 (임계값 도달 시 즉시) |
| **알림 수신자** | 이상 탐지: cost-analyst + FinOps팀장 / KPI 미달: 게이트별 책임 에이전트 / 예산 초과: FinOps팀장 + 재무팀 |
| **SLA** | 이벤트 발생 후 15분 이내 Slack 알림 발송 (ANOMALY_DETECT_LATENCY ≤24h 내 포함) |

**게이트별 알림 연계**

| 게이트 | 알림 수신자 | Jira 레이블 |
|--------|-----------|-----------|
| TAGGING_COVERAGE < 95% | tag-governor (태거) | `finops-tag-violation` |
| FORECAST_MAPE > 10% | finops-practitioner (프랙티셔너) | `finops-forecast-miss` |
| RI_UTILIZATION < 80% | commit-planner (커밋터) | `finops-ri-underutilized` |
| ANOMALY_DETECT_LATENCY > 24h | cost-analyst (FinOps팀장) | `finops-anomaly-sla` |
| IDLE_RESOURCE_RATE > 3% | rightsize-advisor (라이트사이저) | `finops-idle-resource` |
| GPU_UTILIZATION < 60% | finops-practitioner (프랙티셔너) | `finops-gpu-underutilized` |

**실패 액션**
- Slack 전송 실패: 이메일 백업 채널로 자동 전환 + Jira 티켓 상태 `Alert-Failed` 표시
- 에스컬레이션: 48시간 알림 미확인 시 FinOps팀장 → 임원 에스컬레이션 (팀장 → CTO/CFO)

---

### 5단계: 액션 (Action)

| 항목 | 내용 |
|------|------|
| **트리거** | 4단계 알림 확인 후 담당 에이전트의 승인 (Slack Approval Bot, ChatOps 워크플로우) |
| **도구** | Terraform (IaC 변경 적용), AWS CLI / Azure CLI / gcloud CLI (리소스 조정), tag-governor 스크립트 (태그 일괄 적용) |
| **액션 유형** | ① 태그 미적용 리소스 일괄 태깅 (tag-governor) ② 유휴 리소스 중지/삭제 (rightsize-advisor 승인 후) ③ Right-sizing 적용 (비운영 환경부터 순차) ④ RI 구매/판매 실행 (commit-planner 승인 후) |
| **승인 체계** | 비용 영향 < 500,000 KRW: 담당 에이전트 단독 승인 / 500,000~5,000,000 KRW: FinOps팀장 승인 / > 5,000,000 KRW: 재무팀 + 임원 승인 |
| **출력** | 변경 사항 적용 + 변경 로그 기록 (Jira 티켓 상태 `Applied`) + 검증 일정 등록 |
| **SLA** | 승인 완료 후 4시간 이내 적용 / 7일 후 KPI 개선 효과 검증 |

**실패 액션**
- 적용 실패: 자동 롤백 실행 (Terraform state 복원) + 인시던트 티켓 생성 (`finops-apply-fail`)
- 롤백 실패: 수동 복구 절차 실행 + post-mortem 일정 즉시 생성 (48시간 이내)
- 에스컬레이션: 적용 실패가 서비스 영향 시 SRE팀 + FinOps팀장 동시 알림

---

## 3. 파이프라인 SLA 요약

| 단계 | 주요 SLA | 실패 기준 |
|------|---------|---------|
| 1단계 데이터수집 | T+6시간 이내 수집 | 24시간 초과 미수집 |
| 2단계 정규화 | 수집 후 2시간 이내 | 스키마 검증 실패 2회 연속 |
| 3단계 분석 | 정규화 후 1시간 이내 | 이상 탐지 지연 24h SLA 위협 |
| 4단계 알림 | 이벤트 후 15분 이내 Slack | 48시간 미확인 → 에스컬레이션 |
| 5단계 액션 | 승인 후 4시간 이내 적용 | 적용 실패 → 자동 롤백 |
| 효과 검증 | 적용 후 7일 | KPI 미개선 → 재검토 큐 |

---

## 4. 파이프라인 운영 거버넌스

### 승인 체계 (ChatOps 기반)

```
Slack 알림 수신
  → [에이전트] /approve {티켓ID}  또는  /reject {티켓ID} {사유}
  → 승인 시: 5단계 액션 자동 트리거
  → 거부 시: 티켓 상태 'Rejected' + 재검토 큐 이동
  → 24시간 무응답: 에스컬레이션 자동 실행
```

### 변경 로그 보존

- 모든 변경 사항: Jira 티켓 + 변경 이전/이후 상태 기록
- Terraform state 백업: S3·Blob·GCS 버저닝 활성화 (90일 보존)
- 월간 변경 이력 보고서: review-runbook.md 월간 리뷰 아젠다 연계
