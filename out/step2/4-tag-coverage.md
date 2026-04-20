# 태그 커버리지 분석 보고서

**분석 일시**: 2026-04-19  
**분석 범위**: out/focus-normalized.csv (2,335행)  
**조직**: (주)하이브리지텔레콤 (HBT)

---

## 1. 필수 4종 태그 커버리지 요약

### 1.1 전체 커버리지 현황

| 태그 키 | 태그 존재 | 전체 리소스 | 커버리지 % | 미태깅 비용(KRW) | 비용 기준 누락률 |
|--------|---------|-----------|----------|-----------------|-----------------|
| Project | 2,252 | 2,335 | 96.45% | 207,431 | 0.49% |
| Environment | 2,335 | 2,335 | 100.00% | 0 | 0.00% |
| Owner | 2,271 | 2,335 | 97.26% | 108,254 | 0.26% |
| CostCenter | 2,236 | 2,335 | 95.76% | 735,271 | 1.74% |

**종합 평가**: 필수 4종 태그 커버리지 96.12% (행 기준). 목표 95% 달성 상태.

---

## 2. CSP별 태그 커버리지 분포

### 2.1 AWS (784행, 33.6%)

| 태그 키 | 존재 수 | 커버리지 % | 미태깅 리소스 | 주요 누락 사유 |
|--------|--------|----------|------------|--------------|
| Project | 720 | 91.84% | 64 | 레거시 리소스 미태깅 |
| Environment | 784 | 100.00% | 0 | - |
| Owner | 720 | 91.84% | 64 | 레거시 리소스 미태깅 |
| CostCenter | 753 | 96.05% | 31 | 개발/테스트 리소스 미귀속 |

**AWS 커버리지 평가**: Project, Owner 91.84%로 상대적 약점. 레거시 인스턴스(i-legacy-001, vol-legacy-001) 기반.

### 2.2 Azure (및 기타 — "Other", 1,551행, 66.4%)

| 태그 키 | 존재 수 | 커버리지 % | 미태깅 리소스 | 주요 누락 사유 |
|--------|--------|----------|------------|--------------|
| Project | 1,532 | 98.77% | 19 | Azure DevOps 통합 리소스 미태깅 |
| Environment | 1,551 | 100.00% | 0 | - |
| Owner | 1,551 | 100.00% | 0 | - |
| CostCenter | 1,483 | 95.62% | 68 | 개발/스테이징 환경 미귀속 |

**Azure 커버리지 평가**: Owner 100%, CostCenter 95.62%. 전반적으로 높은 수준.

---

## 3. 미태깅 리소스 Top 20 (비용 순)

| 순위 | 리소스 ID | CSP | 서비스 | 누락 태그 | 비용(KRW) | 누적 비용(KRW) |
|------|----------|-----|--------|---------|---------|-------------|
| 1 | /subscriptions/.../vm-dev-001 | Azure | Virtual Machines | CostCenter | 15,000 | 15,000 |
| 2 | /subscriptions/.../appservice-dev-001 | Azure | App Service | CostCenter | 12,000 | 27,000 |
| 3 | /subscriptions/.../sqldb-dev | Azure | SQL Database | CostCenter | 9,375 | 36,375 |
| 4 | N/A | Anthropic | Anthropic API | Project | 9,344 | 45,719 |
| 5 | i-legacy-001 | AWS | EC2 | Project, Owner | 2,994 | 48,713 |
| 6 | arn:aws:s3:::hbt-logs | AWS | S3 | Project, Owner | 2,700 | 51,413 |
| 7 | vol-legacy-001 | AWS | EC2 | Project, Owner, CostCenter | 400 | 51,813 |

**Top 7 미태깅 비용 합계**: 51,813 KRW (전체 미태깅 비용의 약 6.5%)

**주요 발견사항**:
- Azure 개발/스테이징 리소스(vm-dev-001, appservice-dev-001, sqldb-dev)가 CostCenter 태그 누락
- AWS 레거시 리소스(i-legacy-001, vol-legacy-001)가 Project/Owner/CostCenter 태그 누락
- Anthropic API 리소스가 Project 태그 누락 (AI 특화 리소스)

---

## 4. AI 특화 태깅 준수 현황

### 4.1 AI 리소스 현황

| 항목 | 값 |
|------|-----|
| AI 리소스 수(고유) | 2개 |
| AI 리소스 비용 | 843,695 KRW (2.0%) |
| ServiceName 포함 키워드 | Anthropic API, Vertex AI |

### 4.2 AI 특화 태그 3종 준수도

| AI 태그 키 | 필수 여부 | 현황 | 미준수 리소스 |
|-----------|---------|------|------------|
| LLMApiKey | 필수(신규) | 미적용 | 2개 (Anthropic API) |
| ModelName | 필수(신규) | 미적용 | 2개 (Anthropic API, Vertex AI) |
| ChargebackUnit | 필수(신규) | 미적용 | 2개 (Anthropic API, Vertex AI) |

**AI 태그 평가**: 현재 AI 리소스에 LLMApiKey, ModelName, ChargebackUnit 태그 미적용. 신규 정책 도입 시 즉시 적용 필요.

**추가 태깅 규칙(권고)**:
- **LLMApiKey**: API Key 식별자 마스킹(마지막 4자리만 표시). 예: `sk-...abcd`
- **ModelName**: 사용 모델명 명시. 예: `anthropic-claude-3-5-sonnet`, `google-vertex-ai-gemini`
- **ChargebackUnit**: 청구 단위 지정. 예: `CC-300` (데이터/AI팀)

---

## 5. 환경별 태그 준수 분포

| 환경 | 리소스 수 | Project | Environment | Owner | CostCenter | 문제점 |
|-----|---------|---------|-------------|-------|-----------|--------|
| prod | 800 | 792 (99.0%) | 800 (100.0%) | 800 (100.0%) | 795 (99.4%) | CostCenter 5개 누락 |
| stg | 300 | 298 (99.3%) | 300 (100.0%) | 300 (100.0%) | 285 (95.0%) | CostCenter 15개 누락 |
| dev | 1,235 | 1,162 (94.1%) | 1,235 (100.0%) | 1,171 (94.8%) | 1,156 (93.6%) | Project 73개, Owner 64개, CostCenter 79개 누락 |

**환경별 평가**:
- **prod**: 가장 높은 준수율(99.6% 평균). CostCenter 5개만 미귀속.
- **stg**: 중간 준수율(98.6%). CostCenter 누락 15개.
- **dev**: 가장 낮은 준수율(94.1%). Project, Owner, CostCenter 각각 70~80개 미태깅.

---

## 6. 개선 권고 사항

### 6.1 즉시 조치 (1주일 내)

1. **AWS 레거시 리소스 태깅**
   - 대상: i-legacy-001, vol-legacy-001 등 64개 미태깅 리소스
   - 조치: Project, Owner, CostCenter 3종 태그 추가
   - 담당: 인프라운영팀 (CC-100)
   - 영향 비용: ~3,000 KRW

2. **Azure 개발/스테이징 리소스 CostCenter 귀속**
   - 대상: vm-dev-001, appservice-dev-001 등 68개 리소스
   - 조치: CostCenter 태그 추가 (CC-100 또는 CC-200)
   - 담당: 서비스개발팀 (CC-200)
   - 영향 비용: ~36,000 KRW

3. **AI 리소스 신규 태그 적용**
   - 대상: Anthropic API (Project 누락), Vertex AI 리소스
   - 조치: LLMApiKey, ModelName, ChargebackUnit 3종 태그 추가
   - 담당: 데이터/AI팀 (CC-300)
   - 영향 비용: 843,695 KRW (비용 정확도 향상)

### 6.2 단계적 개선 (2~4주)

4. **개발 환경 환경정보 점검**
   - 현황: dev 환경 Project 미태깅 73개, Owner 미태깅 64개
   - 조치: 자동화 스크립트로 dev 환경 리소스 대량 태깅
   - 목표: Project/Owner 커버리지 98% 이상

5. **tag-policy.yaml 기반 자동 검증 강화**
   - 현황: 수동 탐지 기반의 태그 관리
   - 조치: tag-policy.yaml 런타임 적용으로 배포 시 자동 검증
   - 목표: 신규 리소스 100% 태깅 강제

### 6.3 체계화 (1개월)

6. **월간 태깅 커버리지 리뷰 프로세스 수립**
   - COVERS-R-02 규칙 연계: CostCenter별 태깅 준수율 월간 공개
   - COVERS-O-01 규칙 연계: Owner 태그 형식 검증 및 알림
   - 목표: Crawl → Walk 단계 전환 시 태깅 95%+ 달성

---

## 7. COVERS 규칙 연계

| 원칙 | 규칙 ID | 관련 태그 | 상태 |
|-----|--------|---------|------|
| **O**wnership | COVERS-O-01 | Owner | 97.26% (양호) |
| **O**wnership | COVERS-O-02 | CostCenter | 95.76% (개선 필요) |
| **R**ight-time Report | COVERS-R-02 | Project, Environment, Owner, CostCenter | 96.12% (양호) |
| **S**teering | COVERS-S-02 | tag-policy.yaml 정책 | 신규 정책 적용 필요 |

**COVERS 정렬도**: 필수 4종 태그 커버리지 96%로 Ownership(O) 및 Right-time Report(R) 원칙 부분 달성.  
CostCenter 95.76% 개선으로 완전 달성 가능.

---

## 8. 참고사항

- **빌링 통화**: KRW (₩1,500/$1)
- **분석 기준**: AmortizedCost_KRW (분할상환 비용)
- **Tags 형식**: JSON (예: `{"Project": "web", "Environment": "prod", ...}`)
- **레거시 리소스**: AWS 레거시 EC2 인스턴스(i-legacy-001 등)는 2026년 2월 중 마이그레이션 계획 중
- **AI 리소스 확장**: Vertex AI 추가 도입 예정(2026년 3분기), LLM 태깅 정책 선제 적용 권고
