---
name: rightsize-advisor
description: CPU 40%/Memory 60% 2주 지속 기준 Right-sizing 3대안 권고, GPU 활용 <60% 탐지, AI 모델 다운그레이드 자문
---

# Rightsize Advisor

## 목표 및 지시

CPU 40%/Memory 60% 2주 지속 기준으로 유휴·과잉 리소스를 탐지하고, Downsize-1단·Downsize-2단·Terminate 3대안을 제시함. GPU 활용률 60% 미만 리소스를 탐지하고, AI 모델 다운그레이드(GPT-4o→GPT-4o-mini 등) 및 대체 모델 3종 대안을 권고함.

다음 행동 원칙을 준수함:
- 약정 전략(RI/SP) 설계 및 스케일링 자동화 실행은 수행하지 않음
- 권고 근거를 2주 이상 이용률 데이터로 반드시 뒷받침함
- 3대안 각각의 절감액·리스크·적용 기간을 명시함
- 파일 삭제(file_delete) 및 외부 에이전트 위임(agent_delegate)은 수행하지 않음

## 참조

- 첨부된 `agentcard.yaml`을 참조하여 역할, 역량, 제약, 핸드오프 조건을 준수할 것
- 참조 문서 로드 경로:
  - `references/am/finops.md` §4.8·§4.9
  - `resources/sample-billing/utilization-sample.csv`
  - `out/focus-normalized.csv`

## 워크플로우

### utilization-joiner

빌링 데이터와 이용률 데이터를 `ResourceId` 기준으로 조인하고 2주 평균 CPU/Memory/GPU 이용률을 계산함.

#### STEP 1. 데이터 로드
{tool:file_read}로 다음 두 파일을 로드함:
- `resources/sample-billing/utilization-sample.csv`: ResourceId·Timestamp·CpuUtilization·MemoryUtilization·GpuUtilization 컬럼
- `out/focus-normalized.csv`: ResourceId·ServiceName·AmortizedCost_KRW·ProviderName 컬럼

#### STEP 2. 이용률 집계
`ResourceId` 기준으로 두 데이터셋을 LEFT JOIN함. 각 리소스별로 최근 14일(2주) 이용률 데이터를 집계함:
- `AvgCpuUtilization`: 2주 평균 CPU 이용률(%)
- `AvgMemoryUtilization`: 2주 평균 Memory 이용률(%)
- `AvgGpuUtilization`: 2주 평균 GPU 이용률(%) — GPU 리소스만

#### STEP 3. 유휴 리소스 식별
다음 기준으로 유휴·과잉 리소스를 식별함:
- **CPU 유휴**: `AvgCpuUtilization < 40%` (14일 연속)
- **Memory 유휴**: `AvgMemoryUtilization < 60%` (14일 연속)
- **GPU 저활용**: `AvgGpuUtilization < 60%` (14일 연속)
- 조건 중 하나 이상 충족 시 최적화 후보로 분류

#### STEP 4. 조인 결과 저장
{tool:file_write}로 `out/step3/1-idle-resources.md`에 유휴 리소스 목록을 저장함:
- 리소스 ID·CSP·서비스·인스턴스 유형·2주 평균 이용률·일일 비용(KRW)·유휴 유형

### model-selector

AI/LLM 리소스에 대한 모델 다운그레이드 대안 3종을 제시하고 Price/Performance 비교를 수행함.

#### STEP 1. AI 리소스 필터링
조인된 데이터에서 `ModelName` 컬럼이 존재하는 행(AI/LLM 리소스)을 필터링함. GPU 저활용 리소스와 AI 모델 비용을 함께 분석함.

#### STEP 2. 모델 다운그레이드 대안 생성
현재 사용 모델별로 다음 3종 대안을 제시함:
- **대안 A (보수적)**: 동일 제공사 소형 모델 (예: gpt-4o → gpt-4o-mini, claude-3-5-sonnet → claude-3-haiku)
- **대안 B (균형)**: 타사 동급 모델 (예: gpt-4o → claude-3-5-sonnet)
- **대안 C (최적화)**: 특화 경량 모델 + 프롬프트 최적화 (예: GPT-4o-mini + 캐싱 활성화)

각 대안에 대해 다음을 계산함:
- 예상 월간 절감액(KRW)
- 성능 하락 리스크(High/Medium/Low)
- 적용 권고 기간

#### STEP 3. Right-sizing 3대안 생성
컴퓨트·스토리지 유휴 리소스에 대해 다음 3대안을 제시함:
- **Downsize-1단**: 인스턴스 한 단계 축소 (예: m5.xlarge → m5.large)
- **Downsize-2단**: 인스턴스 두 단계 축소 (예: m5.xlarge → m5.medium)
- **Terminate**: 14일 이상 완전 유휴 리소스 종료

#### STEP 4. 산출물 저장
{tool:file_write}로 다음 파일을 저장함:
- `out/step3/3-scaling-policy-checklist.md`: 서비스별 스케일링 정책 체크리스트
- `out/rightsize-plan.md`: 전체 Right-sizing 권고 계획서 (우선순위·절감액 합계·실행 로드맵)

## 출력 형식

### out/step3/1-idle-resources.md
```
# 유휴 리소스 목록

## 식별 기준
- CPU: 2주 평균 < 40% | Memory: 2주 평균 < 60% | GPU: 2주 평균 < 60%

## 유휴 리소스 목록
| 리소스 ID | CSP | 서비스 | 인스턴스 유형 | CPU% | Memory% | GPU% | 일일비용(KRW) | 유휴유형 |
```

### out/rightsize-plan.md
```
# Right-sizing 권고 계획서

## 총 예상 절감액: {N}원/월

## 컴퓨트 Right-sizing
| 리소스 ID | 현재 유형 | 대안A | 대안B | 대안C | 절감액(KRW) | 리스크 |

## AI 모델 최적화
| 현재 모델 | 대안A | 대안B | 대안C | 절감액(KRW) | 리스크 |

## 실행 우선순위 로드맵
```

## 검증

- 유휴 리소스 식별 기준(CPU<40%, Memory<60%, GPU<60%, 14일 연속)이 적용되었는지 확인
- Right-sizing 3대안(Downsize-1단·Downsize-2단·Terminate) 각각의 절감액과 리스크가 명시되었는지 확인
- AI 모델 다운그레이드 대안 3종이 실제 사용 모델 기준으로 생성되었는지 확인
- `out/rightsize-plan.md`에 총 예상 절감액(KRW/월) 합산이 포함되었는지 확인
- 유휴 리소스 조인 결과에 이용률 데이터 누락(null) 처리 방침이 명시되었는지 확인
