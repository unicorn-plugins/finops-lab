---
name: commit-planner
description: 워크로드 분류(상시/변동/배치/예측불가) 및 RI/SP/Spot 혼합 Conservative/Base/Optimistic 3시나리오 약정 전략 산출
---

# Commit Planner

## 목표 및 지시

상시·변동·배치·예측불가 4범주로 워크로드를 분류하고, RI/SP/Spot 혼합 Conservative·Base·Optimistic 3시나리오를 모델링함. 각 시나리오의 절감액·Break-Even Point(BEP)·리스크를 계산하여 `out/commit-strategy.md`를 산출함.

다음 행동 원칙을 준수함:
- 데이터 정규화, PPT 제작, 실행 자동화는 수행하지 않음
- 의사결정 모델링 결과는 수치 근거와 함께 제시함
- 3시나리오 각각의 BEP 계산 수식을 명시함
- 파일 삭제(file_delete) 및 외부 에이전트 위임(agent_delegate)은 수행하지 않음

## 참조

- 첨부된 `agentcard.yaml`을 참조하여 역할, 역량, 제약, 핸드오프 조건을 준수할 것
- 참조 문서 로드 경로:
  - `references/am/finops.md` §4.10
  - `resources/templates/ri-sp-decision-matrix.md`
  - `out/focus-normalized.csv`

## 워크플로우

### workload-classifier

빌링 데이터 기반으로 워크로드를 4범주로 분류하고 각 범주별 비용 비중을 산출함.

#### STEP 1. 참조 문서 로드
{tool:file_read}로 `references/am/finops.md`(§4.10)와 `resources/templates/ri-sp-decision-matrix.md`를 로드함. 워크로드 분류 기준 및 RI/SP 의사결정 매트릭스를 파악함.

#### STEP 2. 빌링 데이터 로드 및 사용 패턴 분석
{tool:file_read}로 `out/focus-normalized.csv`를 로드함. 리소스별 일별 사용 패턴을 분석함:
- 사용 시간 분포 (24/7·업무시간·배치 시간대·불규칙)
- 사용량 변동성 (표준편차/평균 = CV 계수)
- 예측 가능성 (과거 30일 패턴의 반복성)

#### STEP 3. 워크로드 4범주 분류
다음 기준으로 리소스를 분류함:
- **상시(24/7)**: 가동률 95% 이상, CV < 0.15 → RI 적합
- **변동**: 가동률 40~94%, CV 0.15~0.5 → SP 혼합 적합
- **배치**: 정해진 시간대에만 사용, CV > 0.5 → Spot 적합
- **예측불가**: 패턴 없음, CV > 0.8 → On-Demand 유지

#### STEP 4. 분류 결과 집계
범주별 리소스 수·비용 비중·CSP별 분포를 집계함.

### scenario-modeler

워크로드 분류 결과를 기반으로 Conservative·Base·Optimistic 3시나리오를 계산함.

#### STEP 1. 시나리오 파라미터 정의
3시나리오의 RI/SP/Spot 혼합 비율을 정의함:

| 시나리오 | RI 비율 | SP 비율 | Spot 비율 | On-Demand |
|----------|---------|---------|-----------|-----------|
| Conservative | 20% | 10% | 0% | 70% |
| Base | 40% | 25% | 15% | 20% |
| Optimistic | 60% | 25% | 10% | 5% |

#### STEP 2. 절감액 계산
각 시나리오별 절감액을 계산함:
- RI 절감율: 온디맨드 대비 40% (1년 선납 기준)
- SP 절감율: 온디맨드 대비 25% (Compute SP 기준)
- Spot 절감율: 온디맨드 대비 70% (인터럽트 리스크 고려)
- `절감액(KRW) = Σ(해당 유형 리소스 비용 × 해당 할인율)`

#### STEP 3. Break-Even Point(BEP) 계산
각 시나리오별 BEP를 계산함:
- `BEP(개월) = 선납 비용 / 월간 절감액`
- RI 1년 선납: BEP 계산 후 회수 기간 명시
- RI 3년 선납: BEP 계산 후 회수 기간 명시

#### STEP 4. 리스크 평가
각 시나리오별 리스크를 평가함:
- **Conservative**: 리스크 낮음, 유연성 높음, 절감액 낮음
- **Base**: 리스크 중간, 균형 잡힌 포트폴리오
- **Optimistic**: 리스크 높음(Spot 인터럽트·워크로드 변동), 절감액 높음

#### STEP 5. 약정 전략 산출물 저장
{tool:file_write}로 `out/commit-strategy.md`를 저장함.

## 출력 형식

### out/commit-strategy.md
```
# 약정 전략 보고서

## 워크로드 분류 결과
| 범주 | 리소스 수 | 비용 비중% | CSP 분포 | 권고 약정 유형 |

## 3시나리오 비교
| 구분 | Conservative | Base | Optimistic |
|------|-------------|------|-----------|
| RI 비율 | 20% | 40% | 60% |
| SP 비율 | 10% | 25% | 25% |
| Spot 비율 | 0% | 15% | 10% |
| 월간 절감액(KRW) | | | |
| BEP(1년 RI) | | | |
| BEP(3년 RI) | | | |
| 리스크 | 낮음 | 중간 | 높음 |

## 시나리오별 상세 분석
### Conservative 시나리오
...

## 권고 시나리오
{권고 이유 및 적용 우선순위}

## 실행 로드맵
| 단계 | 기간 | 약정 유형 | 적용 리소스 | 예상 절감액 |
```

## 검증

- 워크로드 4범주(상시·변동·배치·예측불가) 분류 기준이 데이터 기반으로 적용되었는지 확인
- 3시나리오 각각의 RI/SP/Spot 혼합 비율이 명시되었는지 확인
- BEP 계산식과 결과값(1년·3년 RI 각각)이 포함되었는지 확인
- 절감액 계산에 KRW 단위가 적용되었는지 확인
- 권고 시나리오에 선택 근거가 데이터 기반으로 명시되었는지 확인
