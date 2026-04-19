# finops-lab 플러그인 개발 계획서

> 작성일: 2026-04-18  
> 작성 팀: am-strategy  
> 대상 저장소: `~/workshop/finops` (= `C:\Users\hiond\workshop\finops`)  
> 교재: [references/am/04-finops.md](../references/am/04-finops.md)  
> 빌더: [DMAP 빌더](C:\Users\hiond\workspace\dmap)

---

## 1. 목적 (WHY)

FinOps 교재(`references/am/finops.md`)의 **3단계 순환(Inform → Optimize → Operate)** 과  
**2025-2026 프레임워크 업데이트(FOCUS · Ownership×Capability · Cloud+)** 를  
**손으로 돌려보며** 체득 가능한 DMAP 플러그인을 제작함.

### 핵심 학습 목표

- 교재 §4.4 HOW 3단계 순환을 스킬 단위로 체험
- 교재 §4.5·§4.11·§4.16의 **FOCUS 표준** 을 실제 변환·통합까지 실습
- 교재 §4.6·§4.8·§4.10 의 태그 거버넌스·Right-sizing·약정 할인 의사결정을 샘플 데이터로 수행
- 교재 §4.12·§4.14 의 단위경제 KPI 와 성숙도 진단을 템플릿화

---

## 2. 범위 (Scope)

### 2.1 포함 (In-Scope)

| 구분 | 내용 |
|------|------|
| 스킬 | `@why-finops` · `@inform` · `@optimize` · `@operate` 4종 |
| 샘플 데이터 | AWS CUR · Azure Cost Export · GCP Billing Export 3종 (가상·익명) |
| FOCUS 변환 | 3종 CSV → FOCUS v1.x 통합 스키마 정규화 데모 |
| 대시보드 | Markdown + Mermaid 기반 비용 추이·Top 서비스·이상 비용·태깅 갭 리포트 |
| 템플릿 | 태그 정책 YAML · RI/SP/Spot 의사결정 매트릭스 · 월간 리뷰 아젠다 · KPI 대시보드 |
| 룰북 | COVERS 6원칙 + 게이트 기준(태깅 95% · MAPE 10% · RI 활용률 80% 등) 규칙 ID화 |

### 2.2 제외 (Out-of-Scope, 추후 이터레이션)

- 실 CSP 계정 연동 (AWS/Azure/GCP API 호출)
- Infracost 기반 IaC Shift-Left 실습
- HTML/Chart.js 인터랙티브 대시보드 (MVP 이후 2차)
- Jupyter Notebook 기반 심화 분석
- AI 비용 관리(§4.16) 심화 시나리오

---

## 3. 설계 개요 (A3-c 최종안)

### 3.1 플러그인 정보

| 항목 | 값 |
|------|-----|
| 이름 | `finops-lab` |
| 타입 | DMAP 선언형 멀티에이전트 플러그인 |
| 런타임 | Claude Code (1차), Codex CLI (Gateway 호환) |
| 저장소 | `~/workshop/finops` |

### 3.2 스킬 구성

| 스킬 | 역할 | 교재 연결 | 주요 산출물 |
|------|------|---------|-----------|
| `@why-finops` | WHY 정의 · Ownership×Capability 자가진단 · 성숙도(Crawl/Walk/Run) 판정 | §4.2, §4.14~15 | WHY 캔버스, 성숙도 리포트 |
| `@inform` | 3 CSP CSV 로드 → **FOCUS 정규화** → 통합 대시보드 · 이상 비용 탐지 · 태깅 갭 리포트 | §4.5~6, §4.11, §4.16 | focus-normalized.csv, dashboard.md |
| `@optimize` | 유휴 리소스 탐지 · Right-sizing 권고 · **RI/SP/Spot 혼합 추천기**(Conservative/Base/Optimistic 3시나리오) | §4.8~10 | rightsize-plan.md, commit-strategy.md |
| `@operate` | 단위경제 KPI 설정 · 자동화 파이프라인 설계 · 주간/월간/분기 비용 리뷰 템플릿 | §4.11~13 | kpi-dashboard.md, review-runbook.md |

### 3.3 에이전트 구성

| 에이전트 | Tier | 담당 |
|---------|------|------|
| `strategy-director` | HIGH | WHY 정의, 성숙도 진단 |
| `focus-normalizer` | MEDIUM | 3 CSP CSV → FOCUS 스키마 변환·병합 |
| `cost-analyst` | MEDIUM | 통합 데이터 분석, 이상 비용 탐지 |
| `tag-governor` | LOW | 태깅 커버리지 점검, 정책 위반 리포트 |
| `rightsize-advisor` | MEDIUM | 사용률 데이터 기반 다운사이징 3대안 제시 |
| `commit-planner` | HIGH | RI/SP/Spot 혼합 전략 시뮬레이션 (3시나리오) |
| `finops-practitioner` | MEDIUM | KPI 정의, 리뷰 운영 설계 |
| `reviewer` | HIGH | 산출물 독립 검증, 게이트 체크리스트 판정 |

### 3.4 리소스 구성

```
~/workshop/finops/
├── skills/
│   ├── why-finops/SKILL.md
│   ├── inform/SKILL.md
│   ├── optimize/SKILL.md
│   └── operate/SKILL.md
├── agents/
│   ├── strategy-director.md
│   ├── focus-normalizer.md
│   ├── cost-analyst.md
│   ├── tag-governor.md
│   ├── rightsize-advisor.md
│   ├── commit-planner.md
│   ├── finops-practitioner.md
│   └── reviewer.md
├── resources/
│   ├── sample-billing/
│   │   ├── aws-cur-sample.csv
│   │   ├── azure-export-sample.csv
│   │   └── gcp-billing-sample.csv
│   ├── schema/
│   │   └── focus-v1.yaml
│   ├── mapping/
│   │   ├── aws-cur-to-focus.yaml
│   │   ├── azure-export-to-focus.yaml
│   │   └── gcp-billing-to-focus.yaml
│   ├── templates/
│   │   ├── tag-policy.yaml
│   │   ├── ri-sp-decision-matrix.md
│   │   ├── monthly-review-agenda.md
│   │   └── kpi-dashboard.md
│   └── rulebook/
│       ├── covers-principles.yaml
│       └── gate-criteria.yaml
├── gateway/
│   └── runtime-mapping.yaml
├── install.yaml
├── plugin.yaml
├── CLAUDE.md
└── README.md
```

---

## 4. 학습 여정 (사용자 관점)

```
Step 1. @why-finops
        └ 우리 팀의 FinOps WHY 정의 + 현재 성숙도 자가진단

Step 2. @inform
        ├ 2-1. 3 CSP 샘플 CSV 로드
        ├ 2-2. FOCUS v1.x 통합 스키마로 정규화·병합
        └ 2-3. 통합 대시보드 생성 (비용 추이 · Top 서비스 · 이상 비용 · 태깅 갭)

Step 3. @optimize
        ├ 3-1. 유휴/과잉 리소스 탐지 (CPU<40%, 2주 이상 등 지표 기반)
        ├ 3-2. Right-sizing 3대안 제시
        └ 3-3. RI/SP/Spot 혼합 추천 (Conservative/Base/Optimistic)

Step 4. @operate
        ├ 4-1. 단위경제 KPI 정의 (트래픽 1건당 비용 등)
        ├ 4-2. 자동화 파이프라인 설계 (탐지→권고→승인→적용→검증)
        └ 4-3. 주간/월간/분기 리뷰 루틴 템플릿화
```

---

## 5. 샘플 데이터 설계

### 5.1 공통 시나리오

각 CSV에 **의도적으로 심는 학습 이벤트**:

| 시나리오 | AWS CUR | Azure Export | GCP Billing |
|---------|---------|-------------|------------|
| 비용 급증(Anomaly) | 3/15 EC2 비용 3배↑ | 3/20 VM 비용 급증 | 3/25 Compute Engine 급증 |
| 태깅 누락 | `Project` 태그 미지정 리소스 8% | `CostCenter` 미지정 5% | `Environment` 미지정 10% |
| 유휴 리소스 | 미연결 EBS 3개, 유휴 EC2 2개 | 미사용 Disk 2개 | 유휴 GCE 1개 |
| 과잉 프로비저닝 | CPU 평균 15% EC2 5대 | 메모리 30% VM 3대 | CPU 20% GCE 4대 |
| 약정 기회 | 24/7 상시 DB 3대 | 상시 App Service 2대 | 상시 SQL 2대 |

### 5.2 FOCUS 정규화 컬럼 (최소 세트)

FOCUS v1.x 기반:
`BilledCost, EffectiveCost, BillingAccountId, ServiceName, ServiceCategory,
RegionId, ResourceId, ResourceType, ChargeCategory, UsageQuantity, UsageUnit,
Tags, BillingPeriodStart, BillingPeriodEnd, CommitmentDiscountType, CommitmentDiscountStatus`

### 5.3 대시보드 구성 (Markdown + Mermaid)

- 월별 비용 추이 (라인 차트)
- 서비스별 Top 10 (바 차트)
- 이상 비용 알림 (표)
- 태깅 커버리지 (도넛)
- CSP별 분포 (파이)
- 단위경제 KPI (표)

---

## 6. 개발 로드맵 (4-Phase)

DMAP `dmap:develop-plugin` 워크플로우 기준:

| Phase | 기간 | 산출물 |
|-------|------|-------|
| **P1. 기획·설계** | 1일 | plugin.yaml, install.yaml, 스킬 4종 SKILL.md 초안 |
| **P2. 샘플 자산 제작** | 1~2일 | 3 CSP CSV 샘플, FOCUS 스키마 YAML, 매핑 YAML, 템플릿 4종 |
| **P3. 에이전트 구현** | 1~2일 | 8종 에이전트 프롬프트, 룰북 |
| **P4. 통합 테스트·README** | 1일 | End-to-End 학습 여정 실행 검증, README, CLAUDE.md |

### MVP vs 2차 이터레이션

| 구분 | MVP (1차) | 2차 |
|------|-----------|-----|
| 스킬 | `@why-finops` + `@inform` | `@optimize` + `@operate` |
| 대시보드 | Markdown + Mermaid | HTML + Chart.js |
| 데이터 | 정적 CSV | 실 CSP API 연동 옵션 |
| AI 비용 | 미포함 | §4.16 시나리오 추가 |

---

## 7. 검증 기준 (Exit Criteria)

지환(감사) 기준. 모든 항목 정량화.

| 항목 | 기준 |
|------|------|
| 교재 커버리지 | §4.4~§4.15 전 섹션이 스킬/자산에 1:1 매핑됨 |
| FOCUS 변환 완전성 | 3 CSP CSV 모두 FOCUS 필수 컬럼 15종 이상 채워 출력 |
| 대시보드 생성 | `@inform` 실행 결과로 대시보드 Markdown 1본 자동 생성 |
| 약정 추천 시나리오 | RI/SP/Spot 혼합 전략이 Conservative/Base/Optimistic 3안으로 제시됨 |
| 룰북 추적성 | 모든 권고에 COVERS 규칙 ID 역추적 가능 |
| DMAP 표준 준수 | `dmap:develop-plugin` 린트/검증 통과 |

---

## 8. 리스크·대응 (하늘)

| 리스크 | 영향 | 대응 |
|-------|------|------|
| FOCUS v1.x 스펙 변경 가능성 | 매핑 YAML 재작성 필요 | 공식 링크(focus.finops.org)만 참조, 버전 고정 명시 |
| 샘플 데이터 비현실성 | 학습 효과 저하 | 실제 CUR 컬럼명 그대로 사용, 월 단위 30일 데이터 심기 |
| Mermaid 차트 가독성 한계 | 시각 체감 약함 | 2차에서 HTML 대시보드 추가 |
| DMAP 학습 곡선 | 첫 플러그인 제작 부담 | `dmap:help` + 기존 플러그인(`am-strategy`, `npd`) 구조 레퍼런스 |

---

## 9. 다음 액션

1. 이 계획서 승인 확인
2. `~/workshop/finops`에서 `dmap:develop-plugin` 실행
3. P1(기획·설계) 산출물 먼저 리뷰 후 P2 진행
4. MVP 완성 후 팀 내부 시연 → 피드백 → 2차 이터레이션 착수

---

## 10. 참고 자료

- 교재: [references/am/04-finops.md](../references/am/04-finops.md)
- State of FinOps 2026: [references/finops/State of FinOps 2026 Report.pdf](../references/finops/)
- FOCUS 공식: https://focus.finops.org/
- FinOps Framework: https://finops.org/framework
- DMAP 빌더: `C:\Users\hiond\workspace\dmap`
- 참고 플러그인: `C:\Users\hiond\workshop\am-strategy`
