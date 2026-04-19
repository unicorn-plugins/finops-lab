# (주)하이브리지텔레콤 — 회사 프로파일

## 1. 회사 기본정보

| 항목 | 내용 |
|------|------|
| 회사명 | (주)하이브리지텔레콤 |
| 약어 | HBT |
| 설립 | 2008년 |
| 임직원 수 | 3,200명 |
| 연매출 | 약 ₩820,000,000,000 (8,200억 원) |
| 본사 | 서울특별시 |
| 사업자 유형 | 주식회사 (비상장) |

## 2. 사업 영역

| 사업 분야 | 설명 |
|-----------|------|
| MNO (Mobile Network Operator) | 자체 이동통신망 운영, LTE/5G 서비스 제공 |
| MVNO (Mobile Virtual Network Operator) | 알뜰폰 플랫폼 운영, B2C 및 기업 전용 알뜰폰 서비스 |
| 엔터프라이즈 IoT | 산업용 IoT 단말 관리, 원격 모니터링 솔루션 |
| 5G 기반 B2B 솔루션 | 스마트 팩토리, 커넥티드 캠퍼스, 공공 안전망 구축 |

## 3. 클라우드 현황

### 3.1 멀티클라우드 구성

| 클라우드 | 주요 용도 | 주 리전 | 비중 |
|---------|----------|---------|------|
| AWS | 주력 프로덕션 워크로드 (web, api, data 프로젝트) | ap-northeast-2 (서울) | 55% |
| Azure | 내부 업무 시스템(HR·ERP·협업툴) + web/api/data 일부 dev·stg·prod 미러 및 보조 워크로드 | koreacentral (한국 중부) | 25% |
| GCP | ML/AI 파이프라인, BigQuery 데이터 레이크 (일부 web/api 워크로드 포함) | asia-northeast3 (서울) | 20% |

### 3.2 AWS 주요 서비스 현황

- **Web 프로젝트**: ECS Fargate, CloudFront, S3, RDS Aurora
- **API 프로젝트**: ECS Fargate, API Gateway, Lambda, ElastiCache
- **Data 프로젝트**: EMR, Redshift, Glue, S3, Kinesis

### 3.3 Azure 주요 서비스 현황

- HR 시스템: Azure App Service, Azure SQL Database
- ERP: Azure Virtual Machines, Azure Blob Storage
- 협업툴: Microsoft 365 연동, Azure Active Directory
- 멀티클라우드 미러링: web/api 프로젝트의 dev/stg 환경과 일부 prod 보조 인스턴스(재난복구·버스트 용량)를 Azure에서 운영

### 3.4 GCP 주요 서비스 현황

- ML 파이프라인: Vertex AI, Cloud Run, Pub/Sub
- 데이터 레이크: BigQuery, Cloud Storage, Dataflow
- AI 모델 서빙: Vertex AI Endpoints, Cloud Functions

## 4. 월 클라우드 지출 규모

| 항목 | 월 지출 (KRW) | 비중 |
|------|--------------|------|
| AWS | ₩176,000,000 | 55% |
| Azure | ₩80,000,000 | 25% |
| GCP | ₩64,000,000 | 20% |
| **합계** | **₩320,000,000** | 100% |

> 환율 기준: $1 = ₩1,500 (빌링 통화: KRW)

## 5. 조직 구성

### 5.1 FinOps 팀 (2명)

| 이름 | 직책 | 주요 책임 |
|------|------|----------|
| 이지수 | FinOps팀 팀장 | FinOps 전략 수립, 경영진 보고, 예산 관리 |
| 박민준 | FinOps 엔지니어 | 비용 분석, 최적화 실행, 자동화 구현 |

### 5.2 클라우드아키텍처팀 (5명)

- 클라우드 아키텍처 설계 및 기술 표준 수립
- FinOps 팀과 협업하여 Well-Architected 리뷰 수행
- 신규 서비스 클라우드 도입 검토

### 5.3 관련 이해관계자

| 부서 | FinOps 관련 역할 |
|------|----------------|
| 서비스개발팀 | CostCenter CC-200 비용 오너, 워크로드 최적화 협업 |
| 데이터/AI팀 | CostCenter CC-300 비용 오너, ML 비용 최적화 협업 |
| 인프라운영팀 | CostCenter CC-100 비용 오너, 예약 인스턴스 관리 |
| 재무팀 | 예산 승인, 청구 검토, 연간 클라우드 예산 편성 |

## 6. CostCenter 구성

| CostCenter ID | 명칭 | 담당 부서 | 대상 서비스 |
|--------------|------|----------|------------|
| CC-100 | 인프라/운영 | 인프라운영팀 | 공통 인프라, 네트워킹, 보안 |
| CC-200 | 서비스개발 | 서비스개발팀 | Web, API 프로덕션 서비스 |
| CC-300 | 데이터/AI | 데이터/AI팀 | Data 파이프라인, ML 워크로드 |

## 7. 핵심 태그 규칙

모든 클라우드 리소스에는 아래 4종의 태그가 필수 적용됩니다.

| 태그 키 | 허용값 | 예시 | 설명 |
|---------|--------|------|------|
| Project | web, api, data, ml | `Project=api` | 귀속 프로젝트 |
| Environment | prod, stg, dev | `Environment=prod` | 운영 환경 구분 |
| Owner | 담당자 이메일 | `Owner=minjun.park@hbt.co.kr` | 리소스 오너 |
| CostCenter | CC-100, CC-200, CC-300 | `CostCenter=CC-200` | 비용 센터 |

### 태그 미적용 시 처리

1. tag-governor 에이전트가 위반 리소스 자동 탐지
2. 오너에게 Slack 알림 발송
3. 72시간 이내 미수정 시 FinOps팀 에스컬레이션

## 8. 비즈니스 KPI 후보

| KPI | 계산식 | 현재 측정 여부 | 목표 방향 |
|-----|--------|--------------|----------|
| 가입자 1인당 클라우드 비용 | 월 총 클라우드 비용 ÷ 월간 활성 사용자(MAU) | 미측정 | 감소 |
| API 호출 100만 건당 비용 | 월 API 관련 클라우드 비용 ÷ (API 호출 건수 / 1,000,000) | 미측정 | 감소 |
| ML 모델 학습 1회당 비용 | 월 학습 관련 GCP 비용 ÷ 학습 실행 횟수 | 미측정 | 감소 |

## 9. FinOps 성숙도

### 현재 상태: Crawl 단계

| 지표 | 현재 | 목표 (1년) |
|------|------|-----------|
| 태깅 커버리지 | ~85% | 95% 이상 |
| 비용 리뷰 빈도 | 분기 1회 | 월 1회 |
| RI 활용률 | 미집계 | 80% 이상 |
| 단위경제 KPI 측정 | 미시작 | 3종 측정 |
| 예산 경보 자동화 | 부분 적용 | 전 프로젝트 |

### 목표 상태: Walk 단계 (1년 내 달성)

- 태깅 커버리지 95% 이상 달성
- 월별 정기 FinOps 리뷰 운영
- 예약 인스턴스(RI) 활용률 80% 이상
- 단위경제 KPI 3종 정기 측정 및 보고
- 이상 비용 자동 탐지 및 알림 체계 구축

## 10. 참고

- **플러그인**: finops-lab (DMAP FinOps 학습 플러그인)
- **FOCUS 버전**: v1.1 (FinOps Open Cost and Usage Specification)
- **빌링 통화**: KRW (원화), 환율 ₩1,500/$1 적용
