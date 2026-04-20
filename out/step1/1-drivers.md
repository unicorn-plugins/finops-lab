# FinOps 도입 드라이버 — HBT (주)하이브리지텔레콤

> 작성: 전략기획 태희 / 근거: `references/am/finops.md` §4.1~4.4, `references/finops/state-of-finops-2026-lab-guide.md` §1~3, `resources/basic-info/company-profile.md`

## 1. 비즈니스 이슈 목록

월 ₩320M(연 약 ₩3.84B) 멀티클라우드 지출 대비 단위경제 KPI 미측정, 태깅 커버리지 85%, RI 활용률 미집계 등  
기본 가시성·최적화 체계가 부재함. 이슈를 영향도(H/M/L) 및 우선순위로 정리함.

| # | 비즈니스 이슈 | 근거/수치 | 영향도 | 우선순위 |
|---|--------------|----------|--------|----------|
| B1 | 멀티클라우드 비용 불투명 — AWS 55%/Azure 25%/GCP 20% 간 단일 뷰 부재 | FOCUS 미적용, CSP별 이질 스키마 | H | P0 |
| B2 | 단위경제 KPI 미측정 — MAU/API/ML당 비용 산출 불가 | company-profile §8 (3종 모두 미측정) | H | P0 |
| B3 | 태깅 커버리지 부족 — 필수 4태그 15% 미적용 → 비용 귀속 불가 | 현재 ~85%, 목표 95% | H | P0 |
| B4 | RI/SP 활용률 미집계 — On-Demand 과다 지출 추정 | company-profile §9, 목표 80% | H | P0 |
| B5 | 이상 비용 탐지 부재 — 급증 사전 차단 불가 | 예산 경보 부분 적용 | M | P1 |
| B6 | FinOps for AI 미대응 — GCP Vertex AI·BigQuery 비용 추적 공백 | State of FinOps 2026 §2, AI 관리율 98% | H | P0 |
| B7 | 분기 1회 리뷰 → 의사결정 지연 | 목표 월 1회 | M | P1 |
| B8 | 재무-엔지니어링 협업 체계 미성숙 — 오너십 분산 | FinOps팀 단 2명, 18개 CSP 서비스 커버 | H | P0 |
| B9 | 예측 정확도(MAPE) 기준선 없음 → 예산 편성 괴리 | COVERS-R-03 목표 ≤10% | M | P1 |
| B10 | SaaS/LLM 지출 가시성 공백 — Cloud+ 범주 미관리 | State of FinOps 2026 §2, SaaS 관리율 90% | M | P1 |

## 2. FinOps 3대 가치 매핑

FinOps 3대 가치(Inform·Optimize·Operate)에 이슈를 매핑함. ●=핵심, ○=보조.  
매핑 근거는 `references/am/finops.md` §4.1~4.4 및 State of FinOps 2026 §1~3 Top 스킬셋을 참조함.

| 이슈 | Inform | Optimize | Operate | 매핑 근거 |
|------|:------:|:--------:|:-------:|----------|
| B1 멀티클라우드 불투명 | ● | ○ | ○ | §4.4 보이기 — FOCUS 표준 정규화 (COVERS-S-01) |
| B2 단위경제 KPI 미측정 | ○ | ○ | ● | §4.2 WHY 투자가치 증명, §4.12 KPI (COVERS-V-01) |
| B3 태깅 커버리지 부족 | ● | ○ | ○ | §4.4 태그 기반 비용 할당 (COVERS-O-01, O-02) |
| B4 RI/SP 미집계 | ○ | ● | ○ | §4.4 줄이기 — 약정 할인 (COVERS-E-04) |
| B5 이상 비용 탐지 부재 | ● | ○ | ○ | §4.2 WHAT#1 이상 비용 탐지 (COVERS-R-01) |
| B6 FinOps for AI 공백 | ● | ● | ○ | §4.16 FinOps for AI, SoF 2026 AI Cost Mgmt 58% |
| B7 분기→월 리뷰 | ○ | ○ | ● | §4.4 체계화 — 정기 리뷰 (COVERS-C-01) |
| B8 협업 체계 미성숙 | ○ | ○ | ● | §4.3 Collaboration + Ownership (COVERS-C-02) |
| B9 예측 MAPE 기준선 | ● | ○ | ○ | §4.12 예측 정확도 (COVERS-R-03) |
| B10 SaaS/LLM 공백 | ● | ○ | ○ | §4.15 Cloud+ Scope 확장 |

## 3. State of FinOps 2026 Top 스킬셋 정합성

HBT의 이슈 매핑이 업계 Top 스킬셋과 정렬되는지 검증함.

| Top 스킬셋 (SoF 2026 응답률) | HBT 관련 이슈 | 정합성 |
|------------------------------|--------------|--------|
| AI Cost Management (58%) | B6 (FinOps for AI 공백) | 최우선 — GCP Vertex AI·ML 학습 비용 관리 |
| FinOps Tooling (43%) | B1, B3, B5 | FOCUS 정규화·태그 거버너·이상 탐지 도구 필요 |
| Engineering/Automation (40%) | B4, B8 | RI/SP 자동 분석·오너십 자동 알림 파이프라인 |
| Capacity Planning (39%) | B9, B4 | MAPE 관리·약정 커버리지 계획 |

## 4. 결론

HBT의 10개 비즈니스 이슈 중 P0 6개(B1·B2·B3·B4·B6·B8)는 Inform·Operate 가치에 집중되어 있으며,  
Crawl→Walk 1년 전환 목표 달성을 위해 FOCUS 정규화·태깅 커버리지·단위경제 KPI·FinOps for AI  
4개 축을 최우선 과제로 설정함.
