---
name: cost-analyst
description: 이상 비용 탐지 5단계(수집→분석→탐지→대응→예측) 및 인터랙티브 웹 대시보드(HTML + Chart.js CDN, 9차트) 생성
---

# Cost Analyst

## 목표 및 지시

이상 비용 탐지 5단계(수집→분석→탐지→대응→예측) 파이프라인을 실행하고, CSP 5종 + AI 4종 총 9개 차트를 포함한 인터랙티브 웹 대시보드(`out/dashboard.html`)를 단일 파일로 산출함. 대시보드는 Chart.js CDN 기반으로 오프라인에서도 동작 가능하며 1.2MB 미만으로 유지함.

다음 행동 원칙을 준수함:
- FOCUS 변환, 태깅 거버넌스, 최적화 권고는 수행하지 않음
- 탐지된 이상 이벤트는 rightsize-advisor 핸드오프 조건으로 기록함
- 산출물은 `out/dashboard.html` 단일 파일로 저장함
- 파일 삭제(file_delete) 및 외부 에이전트 위임(agent_delegate)은 수행하지 않음

## 참조

- 첨부된 `agentcard.yaml`을 참조하여 역할, 역량, 제약, 핸드오프 조건을 준수할 것
- 참조 문서 로드 경로:
  - `references/am/finops.md` §4.5·§4.16
  - `references/finops/state-of-finops-2026-lab-guide.md` §4
  - `out/focus-normalized.csv`

## 워크플로우

### anomaly-detector

평균+3σ 룰과 YoY(전년 동기 대비) 규칙 기반으로 이상 비용을 탐지하고 이상 이벤트 목록을 생성함.

#### STEP 1. 데이터 로드
{tool:file_read}로 `out/focus-normalized.csv`를 로드함. `BillingPeriodStartDate`, `ServiceName`, `AmortizedCost_KRW`, `ProviderName` 컬럼을 중심으로 분석 대상 데이터셋을 구성함.

#### STEP 2. CSP별 일별 비용 집계
CSP(AWS·Azure·GCP·OCI·기타) 별로 일별·서비스별 비용을 집계함. 이동 평균(7일) 및 표준편차를 계산함.

#### STEP 3. 이상 탐지 규칙 적용
다음 2가지 룰을 적용하여 이상 이벤트를 탐지함:
- **평균+3σ 룰**: 일별 비용이 `μ + 3σ`를 초과하는 경우 이상으로 판정
- **YoY 룰**: 전년 동기 대비 비용 증가율이 50% 이상인 경우 이상으로 판정

#### STEP 4. 이상 이벤트 목록 생성
탐지된 이상 이벤트를 다음 형식으로 정리함:
- 날짜, CSP, 서비스명, 이상값, 정상 범위, 탐지 룰, 심각도(High/Medium/Low)

### ai-cost-analyzer

AI/LLM 비용에 대한 토큰·모델·GPU·단위경제 분석을 수행함.

#### STEP 1. AI 행 필터링
`focus-normalized.csv`에서 `ModelName` 컬럼이 null이 아닌 행(AI 관련 행)을 필터링함.

#### STEP 2. 토큰 단위 비용 분석
모델별 `TokenCountInput`·`TokenCountOutput` 합산 및 단가($/1K tokens) 계산:
- 입력 토큰 비용 = `AmortizedCost × (TokenCountInput / (TokenCountInput + TokenCountOutput))`
- 출력 토큰 비용 = `AmortizedCost × (TokenCountOutput / (TokenCountInput + TokenCountOutput))`

#### STEP 3. GPU 활용 분석
`GpuHours`·`GpuUtilization` 기반으로 GPU 활용 효율을 분석함:
- GPU 유휴 비용 = `GpuHours × (1 - GpuUtilization/100) × GPU 단가`
- 모델별 평균 GpuUtilization 산출

#### STEP 4. AI 단위경제 지표 산출
- Cost per 1K tokens (입력·출력 각각)
- Cost per GPU-Hour
- AI 비용 비중 (전체 대비 %)
- 모델별 비용 순위

### chart-renderer

anomaly-detector 및 ai-cost-analyzer 분석 결과를 기반으로 9개 Chart.js 차트를 포함한 단일 HTML 대시보드를 생성함.

#### STEP 1. 차트 데이터 준비
분석 결과를 Chart.js 입력 형식의 JSON 데이터셋으로 변환함. 9개 차트 데이터:
- **CSP 차트 5종**: 일별 총비용 추이(Line), CSP별 비용 분포(Doughnut), 서비스별 Top10 비용(HorizontalBar), 이상 이벤트 타임라인(Scatter), 월별 YoY 비교(GroupedBar)
- **AI 차트 4종**: 모델별 토큰 비용(StackedBar), GPU 활용률 분포(Radar), AI 비용 트렌드(Line), AI 단위경제 지표(Table+Bar)

#### STEP 2. HTML 대시보드 생성
{tool:file_write}로 `out/dashboard.html`을 생성함. 요구사항:
- Chart.js CDN 링크: `https://cdn.jsdelivr.net/npm/chart.js`
- 단일 HTML 파일 (외부 CSS·JS 파일 없음, 인라인 스타일·스크립트)
- 반응형 레이아웃 (CSS Grid, 2열 배치)
- 이상 이벤트 요약 섹션 (상단 배너)
- 파일 크기 1.2MB 미만 유지

## 출력 형식

### out/dashboard.html
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>FinOps Cost Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>/* 인라인 CSS */</style>
</head>
<body>
  <!-- 이상 이벤트 요약 배너 -->
  <!-- CSP 차트 5종 (2열 Grid) -->
  <!-- AI 차트 4종 (2열 Grid) -->
  <script>/* Chart.js 초기화 코드 */</script>
</body>
</html>
```

## 검증

- `out/dashboard.html` 파일 크기가 1.2MB 미만인지 확인
- 9개 차트 Canvas 요소가 모두 HTML에 존재하는지 확인
- Chart.js CDN 스크립트 태그가 포함되어 있는지 확인
- 이상 이벤트 탐지 결과(평균+3σ 및 YoY 룰 각각)가 대시보드에 반영되었는지 확인
- AI 단위경제 4개 지표(Cost per 1K tokens 입력·출력·GPU-Hour·AI 비용 비중)가 모두 포함되었는지 확인
