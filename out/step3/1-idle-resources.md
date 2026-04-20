# 유휴 리소스 목록

## 식별 기준

- CPU: 2주 평균 < 40% | Memory: 2주 평균 < 60% | GPU: 2주 평균 < 60%  
- 관찰 기간: 2026-03-01 ~ 2026-03-31 (31일, 14일 이상 연속 데이터 보유 리소스만 판정)  
- 조건 중 하나 이상 충족 시 최적화 후보 분류  
- 이용률 데이터 누락(null) 처리 방침: 해당 날짜 제외 후 유효 측정치만으로 평균 산정; 14일 미만 데이터 보유 리소스는 판정 제외

## 유휴 리소스 목록 (28건)

| 리소스 ID | CSP | 서비스 | 인스턴스 유형 | CPU% | Memory% | GPU% | 일일비용(KRW) | 유휴유형 |
|-----------|-----|--------|--------------|------|---------|------|--------------|---------|
| vm-overprov-001 | Azure | Virtual Machines | Standard_D8s_v3 | 23.9 | 28.5 | N/A | 87,097 | CPU유휴·MEM유휴 |
| vm-overprov-002 | Azure | Virtual Machines | Standard_D8s_v3 | 21.0 | 28.6 | N/A | 87,097 | CPU유휴·MEM유휴 |
| vm-overprov-003 | Azure | Virtual Machines | Standard_D8s_v3 | 19.2 | 28.3 | N/A | 87,097 | CPU유휴·MEM유휴 |
| vm-spike-azure | Azure | Virtual Machines | Standard_D4s_v3 | 43.2 | 58.5 | N/A | 46,452 | MEM유휴 |
| vm-api-001 | Azure | Virtual Machines | Standard_D4s_v3 | 56.2 | 56.4 | N/A | 43,548 | MEM유휴 |
| i-overprov-001 | AWS | Amazon EC2 | m5.4xlarge | 12.6 | 20.2 | N/A | 27,648 | CPU유휴·MEM유휴 |
| i-overprov-002 | AWS | Amazon EC2 | m5.4xlarge | 13.0 | 20.1 | N/A | 27,648 | CPU유휴·MEM유휴 |
| i-overprov-003 | AWS | Amazon EC2 | m5.4xlarge | 12.7 | 19.7 | N/A | 27,648 | CPU유휴·MEM유휴 |
| i-overprov-004 | AWS | Amazon EC2 | m5.4xlarge | 13.3 | 20.1 | N/A | 27,648 | CPU유휴·MEM유휴 |
| i-overprov-005 | AWS | Amazon EC2 | m5.4xlarge | 12.4 | 19.9 | N/A | 27,648 | CPU유휴·MEM유휴 |
| vm-web-001 | Azure | Virtual Machines | Standard_D2s_v3 | 58.9 | 58.1 | N/A | 21,774 | MEM유휴 |
| vm-web-002 | Azure | Virtual Machines | Standard_D2s_v3 | 64.5 | 57.1 | N/A | 21,774 | MEM유휴 |
| i-spike-001 | AWS | Amazon EC2 | c5.2xlarge | 45.6 | 50.0 | N/A | 19,161 | MEM유휴 |
| i-web-001 | AWS | Amazon EC2 | m5.2xlarge | 62.6 | 56.3 | N/A | 13,824 | MEM유휴 |
| i-web-002 | AWS | Amazon EC2 | m5.2xlarge | 63.1 | 57.4 | N/A | 13,824 | MEM유휴 |
| i-web-003 | AWS | Amazon EC2 | m5.2xlarge | 61.5 | 57.4 | N/A | 13,824 | MEM유휴 |
| gce-spike-1 | GCP | Compute Engine | n2-standard-4 | 39.3 | 45.0 | N/A | 12,774 | CPU유휴·MEM유휴 |
| gce-overprov-002 | GCP | Compute Engine | n2-standard-8 | 18.7 | 27.5 | N/A | 10,368 | CPU유휴·MEM유휴 |
| gce-overprov-003 | GCP | Compute Engine | n2-standard-8 | 19.3 | 27.4 | N/A | 10,368 | CPU유휴·MEM유휴 |
| gce-overprov-004 | GCP | Compute Engine | n2-standard-8 | 18.9 | 26.9 | N/A | 10,368 | CPU유휴·MEM유휴 |
| gce-overprov-005 | GCP | Compute Engine | n2-standard-8 | 19.2 | 27.9 | N/A | 10,368 | CPU유휴·MEM유휴 |
| gce-web-001 | GCP | Compute Engine | n2-standard-4 | 62.9 | 53.6 | N/A | 6,969 | MEM유휴 |
| gce-web-002 | GCP | Compute Engine | n2-standard-4 | 60.2 | 52.4 | N/A | 6,969 | MEM유휴 |
| gce-api-001 | GCP | Compute Engine | n2-standard-4 | 56.8 | 54.1 | N/A | 6,969 | MEM유휴 |
| gce-api-002 | GCP | Compute Engine | n2-standard-4 | 54.5 | 51.8 | N/A | 6,969 | MEM유휴 |
| gce-idle-1 | GCP | Compute Engine | n2-standard-4 | 19.1 | 25.9 | N/A | 6,969 | CPU유휴·MEM유휴 |
| i-idle-001 | AWS | Amazon EC2 | m5.large | 0.0 | 0.0 | N/A | 0 | CPU유휴·MEM유휴 |
| i-idle-002 | AWS | Amazon EC2 | m5.large | 0.0 | 0.0 | N/A | 0 | CPU유휴·MEM유휴 |

## 판정 근거 요약

| 유형 | 건수 | 판정 기준 |
|------|------|---------|
| CPU유휴 | 16건 | 2주 평균 CPU < 40% |
| MEM유휴 | 28건 | 2주 평균 Memory < 60% |
| CPU+MEM 복합 | 16건 | 두 조건 동시 충족 |
| GPU저활용 | 0건 | 2주 평균 GPU < 60% (해당 리소스 GPU 이용률 측정값 없음) |

## 주요 유휴 리소스 상세

### 완전 유휴 리소스 (Terminate 우선순위)

- **i-idle-001** (m5.large): CPU 0% · Memory 0% · 31일 연속 — 즉시 종료 권고  
- **i-idle-002** (m5.large): CPU 0% · Memory 0% · 31일 연속 — 즉시 종료 권고  

### 과잉 프로비저닝 리소스 (Downsize 우선순위)

- **vm-overprov-001** (Standard_D8s_v3): CPU 23.9% · Memory 28.5% · 월 2,612,903KRW  
- **vm-overprov-002** (Standard_D8s_v3): CPU 21.0% · Memory 28.6% · 월 2,612,903KRW  
- **vm-overprov-003** (Standard_D8s_v3): CPU 19.2% · Memory 28.3% · 월 2,612,903KRW  
- **i-overprov-001** (m5.4xlarge): CPU 12.6% · Memory 20.2% · 월 829,440KRW  
- **i-overprov-002** (m5.4xlarge): CPU 13.0% · Memory 20.1% · 월 829,440KRW  
- **i-overprov-003** (m5.4xlarge): CPU 12.7% · Memory 19.7% · 월 829,440KRW  
- **i-overprov-004** (m5.4xlarge): CPU 13.3% · Memory 20.1% · 월 829,440KRW  
- **i-overprov-005** (m5.4xlarge): CPU 12.4% · Memory 19.9% · 월 829,440KRW  