# Ownership × Capability 성숙도 진단 — HBT

> 작성: 전략기획 태희 / 근거: `references/am/finops.md` §4.14~4.16, State of FinOps 2026 Lab Guide §1~3  
> 평가 기준: Crawl / Walk / Run 3단계 성숙도 모델

## 1. Ownership 현황

현재 HBT의 클라우드 비용 Ownership은 재무팀·엔지니어링(인프라/서비스개발/데이터AI)·경영진 간 분산되어 있으나  
명시적 책임 분담(RACI)이 미정립되어 있음. FinOps팀 2명(이지수·박민준)이 사실상 모든 책임을 겸함.

| 주체 | 현재 책임 범위 | Capability 최하위 항목 | 갭 (Crawl → Walk) |
|------|---------------|----------------------|-------------------|
| **경영진** (CTO/CFO) | 연간 예산 승인 / 분기 보고 수령 | **Executive Alignment** — 단위경제 KPI·ROI 보고 프레임 부재 | WHY 공감대·월간 1-Pager 정례화 필요 (COVERS-S-04) |
| **재무팀** | 청구서 검토, 연 1회 예산 편성 | **Governance** — FOCUS 기반 청구 검증 프로세스 없음 | 월간 공동 리뷰 참여·MAPE 관리 참여 (COVERS-R-03, R-04) |
| **FinOps팀** (2명) | 전략·분석·최적화·보고 전 영역 겸임 | **Capacity** — 2명이 3 CSP 18개 서비스 커버 | 연합 거버넌스 체계로 엔지니어링에 일상 책임 이관 (COVERS-S-02, S-03) |
| **인프라운영팀** (CC-100) | RI/공통 인프라 운영 | **Optimization** — RI 활용률 미집계 | 약정 커버리지 자가 측정·권고 실행 (COVERS-E-04) |
| **서비스개발팀** (CC-200) | Web·API 프로덕션 운영 | **Ownership 자가 인식** — 비용 가시성 없음 | 월간 리뷰 사전 셀프체크 의무화 (COVERS-O-03) |
| **데이터/AI팀** (CC-300) | ML/BigQuery 운영 | **AI Cost Management** — Vertex AI 학습 단위비용 미측정 | 모델 학습당 비용 KPI 측정 (COVERS-V-01, SoF 2026 AI 58%) |

## 2. Capability 수준 매트릭스

`references/am/finops.md` §4.14~4.16 성숙도 모델 기준. 평가 항목 4종 × Crawl(1) / Walk(2) / Run(3) 스케일.

| Capability | 현재 수준 | 목표(1년) | 증거/수치 | 우선순위 | COVERS 규칙 |
|-----------|-----------|-----------|----------|----------|-------------|
| **Visibility (가시성)** | Crawl (1.3) | Walk (2.0) | 태깅 85%, FOCUS 미적용, 이상 탐지 없음 | P0 | COVERS-S-01, R-01, R-02 |
| **Optimization (최적화)** | Crawl (1.0) | Walk (2.0) | RI 활용률 미집계, 유휴 탐지 수동 | P0 | COVERS-E-01, E-02, E-04 |
| **Operations (운영)** | Crawl (1.1) | Walk (2.0) | 분기 1회 리뷰, 단위경제 KPI 0종 | P0 | COVERS-C-01, V-01, R-04 |
| **Governance (거버넌스)** | Crawl (1.2) | Walk (2.2) | 태그 정책은 존재, 자동 집행 부분 | P1 | COVERS-O-01, S-02, S-03 |
| **AI Cost Mgmt (확장)** | Pre-Crawl (0.5) | Crawl (1.5) | Vertex AI 학습당 비용 미측정 | P0 | COVERS-V-01 + SoF 2026 §2 |

### 수준 판정 근거

- **Visibility 1.3**: CSP 콘솔 개별 조회는 가능하나 단일 뷰·실시간성 부재 (COVERS-R-01 미달).
- **Optimization 1.0**: 권고는 있으나 실행·ROI 추적 체계 없음 (COVERS-V-03 미달).
- **Operations 1.1**: 리뷰 빈도 분기 1회로 Walk(월 1회) 기준 미달 (COVERS-C-01 미달).
- **Governance 1.2**: 태그 정책은 수립(COVERS-S-02 부분)되었으나 자동 에스컬레이션 부재.
- **AI Cost Mgmt 0.5**: FinOps Foundation 2026 AI 관리율 98% 대비 HBT는 가시성 자체가 부재.

## 3. 우선순위 갭 목록 (Top 8)

Crawl→Walk 12개월 전환을 위해 우선순위 기반으로 갭을 정의함.

| # | 갭 | Ownership 주체 | 현재 → 목표 | COVERS 규칙 | 분기 타겟 |
|---|-----|---------------|-------------|-------------|----------|
| G1 | FOCUS 표준 정규화 부재 | FinOps팀 | 0% → 3 CSP 100% | COVERS-S-01 | Q1 |
| G2 | 태깅 커버리지 85% | 전 개발팀 + FinOps | 85% → 95% | COVERS-O-01, O-02, S-02 | Q1~Q2 |
| G3 | 이상 비용 탐지 파이프라인 | FinOps팀 | 수동 → 24h 자동 | COVERS-R-01 | Q2 |
| G4 | RI/SP 활용률 미집계 | 인프라운영팀 | 미집계 → 80% | COVERS-E-04 | Q2~Q3 |
| G5 | 단위경제 KPI 0종 | 서비스개발/데이터AI | 0 → 3종 | COVERS-V-01 | Q3 |
| G6 | 월간 공동 리뷰 미정착 | 경영진 + 전 팀 | 분기 → 월 | COVERS-C-01, R-04 | Q2 |
| G7 | FinOps for AI 공백 | 데이터/AI팀 | 0 → ML 학습당 비용 측정 | COVERS-V-01 (AI확장) | Q3~Q4 |
| G8 | 예측 MAPE 기준선 없음 | FinOps팀 | 미측정 → ≤10% | COVERS-R-03 | Q4 |

## 4. 진단 요약

HBT는 **Visibility·Operations·AI Cost Mgmt 3개 축이 가장 취약**하며,  
Ownership 측면에서는 **FinOps팀 2명 단독 부담 구조**가 Capability 확장을 가로막는 병목임.  
연합 거버넌스(중앙 정책·분산 실행)로의 전환이 Walk 단계 진입의 전제 조건이 됨 (COVERS-S-02, S-03).
