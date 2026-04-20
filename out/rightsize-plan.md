# Right-sizing 권고 계획서

- 분석 기준일: 2026-04-19  
- 데이터 기간: 2026-03-01 ~ 2026-03-31 (31일)  
- 대상 리소스: 컴퓨트 유휴 28건 + AI 모델 2건  
- 리스크 분류 기준: CPU >= 50% 리소스는 Downsize 시 High/Very High로 상향 적용; MEM유휴 단독 시 MEM 최적화 타입 교체 권고

## 총 예상 절감액 요약

| 대안 | 컴퓨트 절감(KRW/월) | AI 모델 절감(KRW/월) | 합계(KRW/월) | 주요 리스크 |
|------|---------------------|---------------------|-------------|-----------|
| Downsize-1단+MEM최적화 + AI대안A | 8,964,691 | 759,559 | **9,724,250** | Low~High (리소스별 상이) |
| Downsize-2단 + AI대안B | 13,183,127 | 727,933 | **13,911,060** | Medium~Very High |
| Terminate + AI대안C | 18,435,686 | 777,269 | **19,212,955** | Low(완전유휴)/High(과잉) |

---

## 컴퓨트 Right-sizing

### 판정 기준 및 리스크 분류

- CPU 2주 평균 < 40% AND/OR Memory 2주 평균 < 60%로 유휴 판정  
- **CPU >= 50% + MEM유휴 단독**: Downsize 금지 — 메모리 최적화 인스턴스 타입 교체 권고  
  (Downsize 시 CPU 포화 위험; r5/B-시리즈/n2d 등 동급 CPU 저비용 타입으로 교체)  
- **CPU 30~50%**: Downsize-1단 리스크 Medium  
- **CPU < 30%**: Downsize-1단 리스크 Low  
- Terminate: 완전유휴(CPU=0%·MEM=0%) Low, 과잉프로비전 High

### 3대안 비교표

| 리소스 ID | CSP | 현재 유형 | CPU% | MEM% | 대안A | 대안B | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(Terminate,KRW/월) | 리스크A | 리스크B | 리스크C |
|-----------|-----|----------|------|------|-------|-------|--------------|--------------|------------------------|--------|--------|--------|
| vm-overprov-001 | Azure | Standard_D8s_v3 | 23.9 | 28.5 | Standard_D4s_v3 | Standard_D2s_v3 | 1,306,452 | 1,959,677 | 2,351,613 | Low | High | High |
| vm-overprov-002 | Azure | Standard_D8s_v3 | 21.0 | 28.6 | Standard_D4s_v3 | Standard_D2s_v3 | 1,306,452 | 1,959,677 | 2,351,613 | Low | High | High |
| vm-overprov-003 | Azure | Standard_D8s_v3 | 19.2 | 28.3 | Standard_D4s_v3 | Standard_D2s_v3 | 1,306,452 | 1,959,677 | 2,351,613 | Low | Medium | High |
| vm-spike-azure | Azure | Standard_D4s_v3 | 43.2 | 58.5 | Standard_D2s_v3 | Standard_B2ms | 696,774 | 905,806 | 1,254,193 | Medium | High | High |
| vm-api-001 | Azure | Standard_D4s_v3 | 56.2 | 56.4 | [MEM최적화] Standard_B4ms | Standard_B4ms | 326,613 | 457,258 | 1,175,807 | Medium | Medium | High |
| i-overprov-001 | AWS | m5.4xlarge | 12.6 | 20.2 | m5.2xlarge | m5.xlarge | 414,720 | 622,080 | 746,496 | Low | Medium | High |
| i-overprov-002 | AWS | m5.4xlarge | 13.0 | 20.1 | m5.2xlarge | m5.xlarge | 414,720 | 622,080 | 746,496 | Low | Medium | High |
| i-overprov-003 | AWS | m5.4xlarge | 12.7 | 19.7 | m5.2xlarge | m5.xlarge | 414,720 | 622,080 | 746,496 | Low | Medium | High |
| i-overprov-004 | AWS | m5.4xlarge | 13.3 | 20.1 | m5.2xlarge | m5.xlarge | 414,720 | 622,080 | 746,496 | Low | Medium | High |
| i-overprov-005 | AWS | m5.4xlarge | 12.4 | 19.9 | m5.2xlarge | m5.xlarge | 414,720 | 622,080 | 746,496 | Low | Medium | High |
| vm-web-001 | Azure | Standard_D2s_v3 | 58.9 | 58.1 | [MEM최적화] Standard_B2s | Standard_B2s | 163,306 | 228,629 | 587,903 | Medium | Medium | High |
| vm-web-002 | Azure | Standard_D2s_v3 | 64.5 | 57.1 | [MEM최적화] Standard_B2s | Standard_B2s | 163,306 | 228,629 | 587,903 | Medium | Medium | High |
| i-spike-001 | AWS | c5.2xlarge | 45.6 | 50.0 | c5.xlarge | c5.large | 287,420 | 431,129 | 517,355 | Medium | High | High |
| i-web-001 | AWS | m5.2xlarge | 62.6 | 56.3 | [MEM최적화] r5.xlarge | r5.xlarge | 82,944 | 124,416 | 373,248 | Medium | Medium | High |
| i-web-002 | AWS | m5.2xlarge | 63.1 | 57.4 | [MEM최적화] r5.xlarge | r5.xlarge | 82,944 | 124,416 | 373,248 | Medium | Medium | High |
| i-web-003 | AWS | m5.2xlarge | 61.5 | 57.4 | [MEM최적화] r5.xlarge | r5.xlarge | 82,944 | 124,416 | 373,248 | Medium | Medium | High |
| gce-spike-1 | GCP | n2-standard-4 | 39.3 | 45.0 | n2-standard-2 | e2-medium | 191,613 | 249,097 | 344,903 | Medium | High | High |
| gce-overprov-002 | GCP | n2-standard-8 | 18.7 | 27.5 | n2-standard-4 | n2-standard-2 | 155,520 | 233,280 | 279,936 | Low | Medium | High |
| gce-overprov-003 | GCP | n2-standard-8 | 19.3 | 27.4 | n2-standard-4 | n2-standard-2 | 155,520 | 233,280 | 279,936 | Low | Medium | High |
| gce-overprov-004 | GCP | n2-standard-8 | 18.9 | 26.9 | n2-standard-4 | n2-standard-2 | 155,520 | 233,280 | 279,936 | Low | Medium | High |
| gce-overprov-005 | GCP | n2-standard-8 | 19.2 | 27.9 | n2-standard-4 | n2-standard-2 | 155,520 | 233,280 | 279,936 | Low | Medium | High |
| gce-web-001 | GCP | n2-standard-4 | 62.9 | 53.6 | [MEM최적화] n2d-standard-4 | n2d-standard-4 | 41,814 | 62,721 | 188,163 | Medium | Medium | High |
| gce-web-002 | GCP | n2-standard-4 | 60.2 | 52.4 | [MEM최적화] n2d-standard-4 | n2d-standard-4 | 41,814 | 62,721 | 188,163 | Medium | Medium | High |
| gce-api-001 | GCP | n2-standard-4 | 56.8 | 54.1 | [MEM최적화] n2d-standard-4 | n2d-standard-4 | 41,814 | 62,721 | 188,163 | Medium | Medium | High |
| gce-api-002 | GCP | n2-standard-4 | 54.5 | 51.8 | [MEM최적화] n2d-standard-4 | n2d-standard-4 | 41,814 | 62,721 | 188,163 | Medium | Medium | High |
| gce-idle-1 | GCP | n2-standard-4 | 19.1 | 25.9 | n2-standard-2 | e2-medium | 104,535 | 135,896 | 188,163 | Low | Medium | High |
| i-idle-001 | AWS | m5.large | 0.0 | 0.0 | m5.medium | m5.small | 0 | 0 | 0 | Low | Medium | Low |
| i-idle-002 | AWS | m5.large | 0.0 | 0.0 | m5.medium | m5.small | 0 | 0 | 0 | Low | Medium | Low |

**컴퓨트 소계**: 대안A 8,964,691KRW/월 | 대안B 13,183,127KRW/월 | 대안C(Terminate) 18,435,686KRW/월

### 대안 상세 설명

#### 대안A — Downsize-1단 / MEM 최적화 타입 교체

- CPU < 50%: 인스턴스 한 단계 축소 (예: m5.4xlarge → m5.2xlarge, D8s_v3 → D4s_v3)  
- CPU >= 50% MEM유휴 단독: 메모리 최적화 타입 교체  
  - AWS: r5 계열 (메모리 집약형, CPU 동일 수준 유지)  
  - Azure: Standard_B 계열 (Burstable, 유휴 시 크레딧 축적으로 스파이크 대응)  
  - GCP: n2d 계열 (AMD EPYC, 동급 CPU 약 20% 저렴)  
- SLA 리스크: Low(CPU<30%) / Medium(CPU 30~50%) / High(CPU>=50% Downsize 시도 금지)  
- 구현 복잡도: Low — 인스턴스 중지 후 유형 변경 (10~30분 다운타임)  
- 적용 기간: 1~2주 내

#### 대안B — Downsize-2단

- CPU < 30% 리소스에 한해 권고 (CPU >= 30%는 Very High 리스크, 적용 비권고)  
- 절감률: 약 65~75%  
- SLA 리스크: High~Very High (피크 트래픽 대응 능력 현저 감소)  
- 구현 복잡도: Medium — Auto Scaling 정책 동시 조정 필수  
- 적용 기간: 2~4주 (성능 테스트 선행 필수)

#### 대안C — Terminate

- 완전 유휴(CPU=0%·MEM=0%, 31일 연속): i-idle-001, i-idle-002 즉시 종료 권고  
- 과잉 프로비저닝: 14일 추가 모니터링 + 담당팀 승인 후 진행  
- SLA 리스크: Low(완전유휴) / High(과잉프로비전)  
- 적용 기간: 완전유휴 즉시 / 과잉프로비전 4~8주

---

## AI 모델 최적화

### 모델 다운그레이드 3종 대안

| 현재 모델 | 제공사 | 월비용(KRW) | 대안A(보수적) | 대안B(균형) | 대안C(최적화) | 절감A(KRW/월) | 절감B(KRW/월) | 절감C(KRW/월) | 품질리스크A | 품질리스크B | 품질리스크C | 적용기간 |
|----------|--------|------------|---------------|-------------|---------------|--------------|--------------|--------------|-----------|-----------|-----------|---------|
| Vertex AI | GCP | 45,987 | Vertex AI gemini-1.5-flash | Vertex AI gemini-1.5-flash-8b | Vertex AI 배치 예측 API | 27,592 | 34,490 | 29,892 | Medium | Low | Low | 2~4주 (파이프라인 수정 필요) |
| claude-3-5-sonnet | Anthropic | 770,492 | claude-3-haiku | gpt-4o-mini | claude-3-haiku + 프롬프트 캐싱 | 731,967 | 693,443 | 747,377 | Low | Low | Low | 즉시 (1~2주 A/B 테스트 권고) |

**AI 모델 소계**: 대안A 759,559KRW/월 | 대안B 727,933KRW/월 | 대안C 777,269KRW/월

### AI 대안 상세 설명

#### 대안A — 보수적 (동일 제공사 소형 모델)

- claude-3-5-sonnet → claude-3-haiku: API 호환 100%, 입력 토큰 단가 약 95% 절감  
- Vertex AI → gemini-1.5-flash: 동일 GCP 인프라, 마이그레이션 공수 최소  
- 품질 리스크: Low — 일반 텍스트 처리 태스크 품질 차이 미미  
- 적용 기간: 즉시 (1~2주 A/B 테스트 권고)

#### 대안B — 균형 (타사 동급 경량 모델)

- claude-3-5-sonnet → gpt-4o-mini: 프롬프트 일부 수정 필요  
- Vertex AI → gemini-1.5-flash-8b: 단순 분류/요약 태스크 적합  
- 품질 리스크: Low~Medium — 복잡한 추론 태스크 품질 차이 가능  
- 적용 기간: 2~4주

#### 대안C — 최적화 (경량 모델 + 캐싱/배치)

- claude-3-haiku + 프롬프트 캐싱: 캐시 히트 시 입력 토큰 90% 절감  
- Vertex AI 배치 예측 API: 비동기 처리로 실시간 API 대비 최대 50% 절감  
- 품질 리스크: Low — 동일 모델, 캐싱 추가만  
- 적용 기간: 즉시

---

## 실행 우선순위 로드맵

### 즉시 실행 (0~2주) — Low 리스크, 빠른 절감 효과

| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |
|---------|--------|------|-----------------|-------|
| P1 | i-idle-001, i-idle-002 | Terminate | 0 (연결 리소스 정리 효과) | Low |
| P2 | claude-3-5-sonnet | 대안C (캐싱 활성화) | 29,892 | Low |
| P3 | vm-overprov-001,002,003 (D8s->D4s) | Downsize-1단 | 3,919,354 | Low |
| P4 | i-overprov-001~005 (m5.4xl->m5.2xl) | Downsize-1단 | 2,073,600 | Low |
| P5 | gce-overprov-002~005 (n2-std-8->4) | Downsize-1단 | 622,080 | Low |

### 단기 실행 (2~4주) — 테스트 선행 필요

| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |
|---------|--------|------|-----------------|-------|
| P6 | claude-3-5-sonnet | 대안A (claude-3-haiku) | 27,592 | Low |
| P7 | vm-spike-azure (D4s->B4ms) | MEM 최적화 타입 교체 | 348,387 | Medium |
| P8 | vm-api-001 (D4s->B4ms) | MEM 최적화 타입 교체 | 326,613 | Medium |

### 중기 실행 (4~8주) — 의존성 분석 선행 필요

| 우선순위 | 리소스 | 대안 | 예상 절감(KRW/월) | 리스크 |
|---------|--------|------|-----------------|-------|
| P9 | Vertex AI trainingPipelines | 대안B (gemini-1.5-flash-8b) | 693,443 | Low |
| P10 | gce-web/api 시리즈 (n2d-standard-4) | MEM 최적화 타입 교체 | 167,256 | Medium |
| P11 | i-web-001~003, i-spike-001 | MEM 최적화 타입 교체 | 363,800 | Medium |

## 전체 예상 절감 합계

- **대안A 시나리오 (Downsize-1단+MEM최적화+AI대안A)**: 9,724,250KRW/월 (116,691,000KRW/년)  
- **대안B 시나리오 (Downsize-2단+AI대안B)**: 13,911,060KRW/월 (166,932,720KRW/년)  
- **대안C 시나리오 (Terminate+AI대안C)**: 19,212,955KRW/월 (230,555,460KRW/년)  

> 권고 최적안: **대안A** — 9,724,250KRW/월, CPU>=50% 리소스 장애 위험 배제, P1~P5 실행 시 4주 내 효과 가시화  