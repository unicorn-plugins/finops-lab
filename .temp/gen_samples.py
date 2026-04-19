"""
finops-lab 샘플 CSV 생성 스크립트
생성 대상:
  - resources/sample-billing/aws-cur-sample.csv      (~600 rows)
  - resources/sample-billing/gcp-billing-sample.csv  (~400 rows)
  - resources/sample-billing/utilization-sample.csv
"""

import csv
import os
from datetime import date, timedelta, datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "resources", "sample-billing")
os.makedirs(BASE, exist_ok=True)

DAYS = [date(2026, 3, d) for d in range(1, 32)]
BILLING_START = "2026-03-01"
BILLING_END   = "2026-04-01"

def iso(d, hour=0):
    return f"{d}T{hour:02d}:00:00Z"

# ─────────────────────────────────────────────────
# 1. AWS CUR 2.0
# ─────────────────────────────────────────────────
AWS_COLS = [
    "bill_billing_period_start_date",
    "bill_payer_account_id",
    "line_item_usage_account_id",
    "line_item_usage_start_date",
    "line_item_usage_end_date",
    "line_item_product_code",
    "line_item_operation",
    "line_item_resource_id",
    "line_item_usage_type",
    "line_item_usage_amount",
    "line_item_unblended_cost",
    "line_item_blended_cost",
    "product_region",
    "product_instance_type",
    "pricing_unit",
    "pricing_term",
    "reservation_reservation_a_r_n",
    "resource_tags_user_project",
    "resource_tags_user_environment",
    "resource_tags_user_owner",
    "resource_tags_user_cost_center",
]

ACCOUNT = "123456789012"
REGION  = "ap-northeast-2"

def aws_row(d, product, operation, resource_id, usage_type, usage_amt, cost,
            instance_type="", unit="Hrs", term="OnDemand", ri_arn="",
            project="", env="prod", owner="", cc=""):
    return {
        "bill_billing_period_start_date": BILLING_START,
        "bill_payer_account_id": ACCOUNT,
        "line_item_usage_account_id": ACCOUNT,
        "line_item_usage_start_date": iso(d, 0),
        "line_item_usage_end_date": iso(d, 24) if d.day < 31 else "2026-04-01T00:00:00Z",
        "line_item_product_code": product,
        "line_item_operation": operation,
        "line_item_resource_id": resource_id,
        "line_item_usage_type": usage_type,
        "line_item_usage_amount": f"{usage_amt:.4f}",
        "line_item_unblended_cost": f"{cost:.4f}",
        "line_item_blended_cost": f"{cost:.4f}",
        "product_region": REGION,
        "product_instance_type": instance_type,
        "pricing_unit": unit,
        "pricing_term": term,
        "reservation_reservation_a_r_n": ri_arn,
        "resource_tags_user_project": project,
        "resource_tags_user_environment": env,
        "resource_tags_user_owner": owner,
        "resource_tags_user_cost_center": cc,
    }

rows_aws = []

# ── EC2 정상 운영 (web 프로젝트, CC-200) ──────────
# m5.2xlarge: $0.384/hr -> $9.216/day
for inst in ["i-web-001", "i-web-002", "i-web-003"]:
    for d in DAYS:
        rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", inst,
            "BoxUsage:m5.2xlarge", 24, 9.216, "m5.2xlarge",
            project="web", owner="webteam@hbt.co.kr", cc="CC-200"))

# ── EC2 API 프로젝트 정상 (CC-200) ────────────────
# m5.xlarge: $0.192/hr -> $4.608/day
for inst in ["i-api-001", "i-api-002"]:
    for d in DAYS:
        rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", inst,
            "BoxUsage:m5.xlarge", 24, 4.608, "m5.xlarge",
            project="api", owner="apiteam@hbt.co.kr", cc="CC-200"))

# ── EC2 이상 (spike): 3/15 3배 급증 ──────────────
# 평소 $12/day (c5.2xlarge @$0.5/hr)
# 3/15: $36/day (spike, 모델링: usage_amount 3배)
for d in DAYS:
    cost_spike = 36.0 if d.day == 15 else 12.0
    usage_spike = 72.0 if d.day == 15 else 24.0
    rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", "i-spike-001",
        "BoxUsage:c5.2xlarge", usage_spike, cost_spike, "c5.2xlarge",
        project="api", owner="apiteam@hbt.co.kr", cc="CC-200"))

# ── EC2 유휴 (stopped, usage_amount=0) ────────────
for inst, vol in [("i-idle-001", "vol-idle-001"), ("i-idle-002", "vol-idle-002")]:
    for d in DAYS:
        # stopped EC2: usage=0, cost=0
        rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", inst,
            "BoxUsage:m5.large", 0, 0.0, "m5.large",
            project="api", env="stg", owner="apiteam@hbt.co.kr", cc="CC-200"))
        # 부착된 EBS 볼륨은 여전히 비용 발생 (200GB gp3 = $0.53/day)
        rows_aws.append(aws_row(d, "AmazonEC2", "CreateVolume", vol,
            "EBS:VolumeUsage.gp3", 200, 0.533, "",
            unit="GB-Mo", project="api", env="stg",
            owner="apiteam@hbt.co.kr", cc="CC-200"))

# ── EC2 과잉 프로비저닝 (CPU 15%, 5대) ────────────
# m5.4xlarge: $0.768/hr -> $18.432/day (현실에선 작은 인스턴스로 충분)
for i in range(1, 6):
    inst = f"i-overprov-{i:03d}"
    for d in DAYS:
        rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", inst,
            "BoxUsage:m5.4xlarge", 24, 18.432, "m5.4xlarge",
            project="api", owner="apiteam@hbt.co.kr", cc="CC-200"))

# ── EBS 고아 볼륨 (EC2 없이 독립 존재 — 유휴 이벤트, 태그는 존재함) ──
# 유휴 이벤트: 연결된 EC2 없이 EBS 비용만 발생. 태그는 있지만 EC2 인스턴스 ID가 없음.
for vol in ["vol-orphan-001", "vol-orphan-002", "vol-orphan-003"]:
    for d in DAYS:
        rows_aws.append(aws_row(d, "AmazonEC2", "CreateVolume", vol,
            "EBS:VolumeUsage.gp3", 500, 1.333, "",
            unit="GB-Mo", project="api", env="prod",
            owner="apiteam@hbt.co.kr", cc="CC-200"))

# ── 태깅 누락 이벤트: Project 태그 없는 리소스 (~8%) ─────────
# "legacy-*" 인스턴스 — 태그 미적용 상태로 방치된 구형 리소스
for d in DAYS:
    rows_aws.append(aws_row(d, "AmazonEC2", "RunInstances", "i-legacy-001",
        "BoxUsage:t3.large", 24, 1.996, "t3.large",
        project="", env="prod", owner="", cc="CC-100"))
    rows_aws.append(aws_row(d, "AmazonEC2", "CreateVolume", "vol-legacy-001",
        "EBS:VolumeUsage.gp3", 100, 0.267, "",
        unit="GB-Mo", project="", env="prod", owner="", cc=""))

# ── RDS (24/7 상시, RI 후보, CC-200/300) ──────────
# db.r6g.large: $0.24/hr -> $5.76/day
RI_ARN = "arn:aws:rds:ap-northeast-2:123456789012:ri:ri-2026-01-db-001"
for db, proj, cc in [
    ("db-web-001", "web", "CC-200"),
    ("db-api-001", "api", "CC-200"),
    ("db-data-001", "data", "CC-300"),
]:
    for d in DAYS:
        rows_aws.append(aws_row(d, "AmazonRDS", "CreateDBInstance",
            f"arn:aws:rds:{REGION}:{ACCOUNT}:db:{db}",
            "InstanceUsage:db.r6g.large", 24, 5.76, "db.r6g.large",
            unit="Hrs", project=proj,
            owner="dba@hbt.co.kr", cc=cc))

# ── S3 (월간 스토리지 + 요청 비용) ────────────────
s3_resources = [
    ("arn:aws:s3:::hbt-data-lake",  "data", "CC-300", 12.5),
    ("arn:aws:s3:::hbt-web-assets", "web",  "CC-200", 3.2),
    ("arn:aws:s3:::hbt-logs",       "",     "CC-100", 1.8),  # 태그 누락
]
for arn, proj, cc, cost in s3_resources:
    rows_aws.append(aws_row(DAYS[0], "AmazonS3", "PutObject", arn,
        "TimedStorage-ByteHrs", 5_000_000, cost, "",
        unit="GB-Mo", term="OnDemand",
        project=proj, owner="dataeng@hbt.co.kr" if proj else "", cc=cc))
    rows_aws.append(aws_row(DAYS[0], "AmazonS3", "GetObject", arn,
        "Requests-Tier1", 10_000_000, cost * 0.12, "",
        unit="Requests",
        project=proj, owner="dataeng@hbt.co.kr" if proj else "", cc=cc))

# ── Lambda (일별 호출 비용) ────────────────────────
for fn, proj, cc, base_cost in [
    ("arn:aws:lambda:ap-northeast-2:123456789012:function:api-handler", "api", "CC-200", 0.45),
    ("arn:aws:lambda:ap-northeast-2:123456789012:function:data-etl",    "data","CC-300", 0.82),
]:
    for d in DAYS:
        rows_aws.append(aws_row(d, "AWSLambda", "Invoke", fn,
            "Lambda-GB-Second", 50000, base_cost, "",
            unit="Lambda-GB-Second",
            project=proj, owner="devops@hbt.co.kr", cc=cc))

# ── CloudWatch (월간) ─────────────────────────────
cw_items = [
    ("arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/ec2/web", "web", "CC-200", 2.8),
    ("arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/rds/db",  "data","CC-300", 1.5),
    ("arn:aws:cloudwatch:ap-northeast-2:123456789012:alarm:cost-alarm", "api", "CC-200", 0.3),
]
for arn, proj, cc, cost in cw_items:
    rows_aws.append(aws_row(DAYS[0], "AmazonCloudWatch", "PutMetricData", arn,
        "CW:MetricMonitorUsage", 1, cost, "",
        unit="Metrics", project=proj,
        owner="devops@hbt.co.kr", cc=cc))

# ── 태깅 누락 비율 확인: Project가 빈 row 수 ─────
total_aws = len(rows_aws)
no_project = sum(1 for r in rows_aws if r["resource_tags_user_project"] == "")
print(f"[AWS] total rows: {total_aws}, no-project-tag: {no_project} ({no_project/total_aws*100:.1f}%)")

with open(os.path.join(BASE, "aws-cur-sample.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=AWS_COLS)
    w.writeheader()
    w.writerows(rows_aws)
print(f"[AWS] written: {os.path.join(BASE, 'aws-cur-sample.csv')}")

# ─────────────────────────────────────────────────
# 2. GCP Billing Export CSV
# ─────────────────────────────────────────────────
GCP_COLS = [
    "billing_account_id",
    "project_id",
    "project_name",
    "service_description",
    "sku_description",
    "usage_start_time",
    "usage_end_time",
    "location_region",
    "resource_name",
    "resource_global_name",
    "usage_amount",
    "usage_unit",
    "cost",
    "currency",
    "credits_amount",
    "credits_type",
    "labels",
    "invoice_month",
]

GCP_BILLING_ACCOUNT = "01AB12-CD34EF-567890"
GCP_PROJECT_ID      = "acme-prod-001"
GCP_PROJECT_NAME    = "HBT Production"
GCP_REGION          = "asia-northeast3"
INVOICE_MONTH       = "2026-03"

def gcp_row(d, service, sku, resource_name, resource_global, usage_amt, usage_unit,
            cost, credits=0.0, credits_type="",
            project_label="", env_label="prod", owner_label="", cc_label=""):
    labels = (
        f'{{"Project": "{project_label}", "Environment": "{env_label}", '
        f'"Owner": "{owner_label}", "CostCenter": "{cc_label}"}}'
        if project_label or env_label else
        f'{{"Environment": "{env_label}", "Owner": "{owner_label}", "CostCenter": "{cc_label}"}}'
    )
    return {
        "billing_account_id": GCP_BILLING_ACCOUNT,
        "project_id": GCP_PROJECT_ID,
        "project_name": GCP_PROJECT_NAME,
        "service_description": service,
        "sku_description": sku,
        "usage_start_time": iso(d, 0),
        "usage_end_time": iso(d, 24) if d.day < 31 else "2026-04-01T00:00:00Z",
        "location_region": GCP_REGION,
        "resource_name": resource_name,
        "resource_global_name": resource_global,
        "usage_amount": f"{usage_amt:.4f}",
        "usage_unit": usage_unit,
        "cost": f"{cost:.4f}",
        "currency": "USD",
        "credits_amount": f"{credits:.4f}",
        "credits_type": credits_type,
        "labels": labels,
        "invoice_month": INVOICE_MONTH,
    }

rows_gcp = []

def gcp_global(resource_name):
    return f"//compute.googleapis.com/projects/{GCP_PROJECT_ID}/zones/asia-northeast3-a/instances/{resource_name}"

# ── GCE 정상 운영 (Compute Engine, web/api) ───────
# n2-standard-4: $0.1936/hr -> $4.646/day
for inst, proj, env, cc in [
    ("gce-web-001", "web",  "prod", "CC-200"),
    ("gce-web-002", "web",  "prod", "CC-200"),
    ("gce-api-001", "api",  "prod", "CC-200"),
    ("gce-api-002", "api",  "prod", "CC-200"),
]:
    for d in DAYS:
        rows_gcp.append(gcp_row(d, "Compute Engine",
            "N2 Instance Core running in Korea", inst, gcp_global(inst),
            24, "hours", 4.646,
            project_label=proj, env_label=env,
            owner_label="sre@hbt.co.kr", cc_label=cc))

# ── GCE 이상 (spike): 3/25 급증 ──────────────────
# 평소 $8/day, 3/25: $24/day
for d in DAYS:
    cost_gcp_spike = 24.0 if d.day == 25 else 8.0
    usage_gcp_spike = 72.0 if d.day == 25 else 24.0
    rows_gcp.append(gcp_row(d, "Compute Engine",
        "N2 Instance Core running in Korea", "gce-spike-1", gcp_global("gce-spike-1"),
        usage_gcp_spike, "hours", cost_gcp_spike,
        project_label="api", env_label="prod",
        owner_label="apiteam@hbt.co.kr", cc_label="CC-200"))

# ── GCE 유휴 (CPU ~20%, 過잉 프로비저닝 포함) ──────
# gce-idle-1: CPU 20% 유지 (과잉 프로비저닝 유휴)
for d in DAYS:
    rows_gcp.append(gcp_row(d, "Compute Engine",
        "N2 Instance Core running in Korea", "gce-idle-1", gcp_global("gce-idle-1"),
        24, "hours", 4.646,
        project_label="data", env_label="prod",
        owner_label="dataeng@hbt.co.kr", cc_label="CC-300"))

# ── GCE 과잉 프로비저닝 (CPU 20%, 4대) ───────────
for i in range(2, 6):
    inst = f"gce-overprov-{i:03d}"
    for d in DAYS:
        rows_gcp.append(gcp_row(d, "Compute Engine",
            "N2 Instance Core running in Korea", inst, gcp_global(inst),
            24, "hours", 6.912,
            project_label="ml", env_label="prod",
            owner_label="mlteam@hbt.co.kr", cc_label="CC-300"))

# ── Cloud SQL (24/7, RI/CUD 후보) ─────────────────
# db-standard-2: $0.384/hr -> $9.216/day
for db, proj, cc in [
    ("cloudsql-web-001",  "web",  "CC-200"),
    ("cloudsql-data-001", "data", "CC-300"),
]:
    for d in DAYS:
        # Environment 태그 결측 (5일치)
        env_val = "" if d.day in [3, 7, 14, 21, 28] else "prod"
        rows_gcp.append(gcp_row(d, "Cloud SQL",
            "Cloud SQL for MySQL: Zonal - Standard storage",
            db, f"//sqladmin.googleapis.com/projects/{GCP_PROJECT_ID}/instances/{db}",
            24, "hours", 9.216,
            project_label=proj, env_label=env_val,
            owner_label="dba@hbt.co.kr", cc_label=cc))

# ── 태깅 누락 이벤트: Environment 없는 GCE (~10%) ───
# 구형 GCE — Environment 태그 없이 배포된 레거시 인스턴스
for d in DAYS:
    rows_gcp.append(gcp_row(d, "Compute Engine",
        "N2 Instance Core running in Korea",
        "gce-legacy-001", gcp_global("gce-legacy-001"),
        24, "hours", 3.456,
        project_label="api", env_label="",
        owner_label="apiteam@hbt.co.kr", cc_label="CC-200"))

# ── GCS (Cloud Storage, 월별) ─────────────────────
gcs_items = [
    ("hbt-gcs-datalake", "data", "CC-300", 8.5),
    ("hbt-gcs-ml-models", "ml",  "CC-300", 3.2),
    ("hbt-gcs-backup",   "",    "CC-100", 2.1),  # Project 태그 누락
]
for bucket, proj, cc, cost in gcs_items:
    rows_gcp.append(gcp_row(DAYS[0], "Cloud Storage",
        "Standard Storage Korea Multi-Region",
        bucket, f"//storage.googleapis.com/{bucket}",
        2_000_000, "gibibytes", cost,
        project_label=proj, env_label="prod",
        owner_label="dataeng@hbt.co.kr" if proj else "",
        cc_label=cc))

# ── BigQuery (월별) ───────────────────────────────
for d in DAYS[::5]:  # 6일마다 1건
    rows_gcp.append(gcp_row(d, "BigQuery",
        "Analysis queries",
        "hbt-analytics-dataset",
        "//bigquery.googleapis.com/projects/acme-prod-001/datasets/analytics",
        150, "tebibytes", 0.75,
        project_label="data", env_label="prod",
        owner_label="dataeng@hbt.co.kr", cc_label="CC-300"))

# ── Vertex AI (월별) ──────────────────────────────
for d in DAYS[::3]:  # 3일마다 1건
    rows_gcp.append(gcp_row(d, "Vertex AI",
        "Custom Model Training: n1-standard-8",
        "vertex-training-job",
        f"//aiplatform.googleapis.com/projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/trainingPipelines",
        8, "hours", 2.88,
        project_label="ml", env_label="prod",
        owner_label="mlteam@hbt.co.kr", cc_label="CC-300"))

total_gcp = len(rows_gcp)
no_env_gcp = sum(1 for r in rows_gcp if r["labels"].find('"Environment": ""') >= 0)
print(f"[GCP] total rows: {total_gcp}, no-environment-tag: ~{no_env_gcp} ({no_env_gcp/total_gcp*100:.1f}%)")

with open(os.path.join(BASE, "gcp-billing-sample.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=GCP_COLS)
    w.writeheader()
    w.writerows(rows_gcp)
print(f"[GCP] written: {os.path.join(BASE, 'gcp-billing-sample.csv')}")

# ─────────────────────────────────────────────────
# 3. Utilization CSV
# ─────────────────────────────────────────────────
UTIL_COLS = [
    "date",
    "provider",
    "resource_id",
    "resource_name",
    "instance_type",
    "project",
    "environment",
    "cost_center",
    "avg_cpu_percent",
    "max_cpu_percent",
    "avg_memory_percent",
    "max_memory_percent",
    "network_in_gb",
    "network_out_gb",
    "status",
]

rows_util = []

def util_row(d, provider, resource_id, resource_name, instance_type,
             project, env, cc,
             avg_cpu, max_cpu, avg_mem, max_mem,
             net_in=0.5, net_out=0.2, status="running"):
    return {
        "date": str(d),
        "provider": provider,
        "resource_id": resource_id,
        "resource_name": resource_name,
        "instance_type": instance_type,
        "project": project,
        "environment": env,
        "cost_center": cc,
        "avg_cpu_percent": f"{avg_cpu:.1f}",
        "max_cpu_percent": f"{max_cpu:.1f}",
        "avg_memory_percent": f"{avg_mem:.1f}",
        "max_memory_percent": f"{max_mem:.1f}",
        "network_in_gb": f"{net_in:.3f}",
        "network_out_gb": f"{net_out:.3f}",
        "status": status,
    }

# ── AWS EC2 사용률 ────────────────────────────────
import random
random.seed(42)

# 정상 웹 서버 (CPU ~65%)
for inst in ["i-web-001", "i-web-002", "i-web-003"]:
    for d in DAYS:
        avg_c = 60 + random.uniform(-5, 10)
        rows_util.append(util_row(d, "AWS", inst, inst, "m5.2xlarge",
            "web", "prod", "CC-200", avg_c, min(avg_c+20,99), 55+random.uniform(-5,10), 80))

# API 서버 (CPU ~55%)
for inst in ["i-api-001", "i-api-002"]:
    for d in DAYS:
        avg_c = 50 + random.uniform(-5, 10)
        rows_util.append(util_row(d, "AWS", inst, inst, "m5.xlarge",
            "api", "prod", "CC-200", avg_c, min(avg_c+25,99), 60+random.uniform(-5,8), 85))

# spike 인스턴스 (3/15 CPU 급등)
for d in DAYS:
    avg_c = 85 + random.uniform(-2, 5) if d.day == 15 else 40 + random.uniform(-5, 10)
    rows_util.append(util_row(d, "AWS", "i-spike-001", "i-spike-001", "c5.2xlarge",
        "api", "prod", "CC-200", avg_c, min(avg_c+10,99), 50, 75))

# 유휴 인스턴스 (CPU 0%, stopped)
for inst, vol in [("i-idle-001", "vol-idle-001"), ("i-idle-002", "vol-idle-002")]:
    for d in DAYS:
        rows_util.append(util_row(d, "AWS", inst, inst, "m5.large",
            "api", "stg", "CC-200", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "stopped"))

# 과잉 프로비저닝 EC2 (CPU ~15%)
for i in range(1, 6):
    inst = f"i-overprov-{i:03d}"
    for d in DAYS:
        avg_c = 12 + random.uniform(-3, 5)
        rows_util.append(util_row(d, "AWS", inst, inst, "m5.4xlarge",
            "api", "prod", "CC-200", avg_c, min(avg_c+8,30), 20+random.uniform(-5,5), 35))

# ── GCP GCE 사용률 ────────────────────────────────
for inst, proj, cc, base_cpu in [
    ("gce-web-001", "web", "CC-200", 62),
    ("gce-web-002", "web", "CC-200", 58),
    ("gce-api-001", "api", "CC-200", 55),
    ("gce-api-002", "api", "CC-200", 52),
]:
    for d in DAYS:
        avg_c = base_cpu + random.uniform(-5, 8)
        rows_util.append(util_row(d, "GCP", inst, inst, "n2-standard-4",
            proj, "prod", cc, avg_c, min(avg_c+20,99), 50+random.uniform(-5,10), 75))

# gce-spike-1 (3/25 급등)
for d in DAYS:
    avg_c = 88 + random.uniform(-2, 5) if d.day == 25 else 35 + random.uniform(-5, 8)
    rows_util.append(util_row(d, "GCP", "gce-spike-1", "gce-spike-1", "n2-standard-4",
        "api", "prod", "CC-200", avg_c, min(avg_c+10,99), 45, 70))

# gce-idle-1 (CPU ~20%, 유휴)
for d in DAYS:
    avg_c = 18 + random.uniform(-3, 5)
    rows_util.append(util_row(d, "GCP", "gce-idle-1", "gce-idle-1", "n2-standard-4",
        "data", "prod", "CC-300", avg_c, min(avg_c+8, 30), 25+random.uniform(-5,5), 40))

# 과잉 프로비저닝 GCE (CPU ~20%)
for i in range(2, 6):
    inst = f"gce-overprov-{i:03d}"
    for d in DAYS:
        avg_c = 18 + random.uniform(-3, 5)
        rows_util.append(util_row(d, "GCP", inst, inst, "n2-standard-8",
            "ml", "prod", "CC-300", avg_c, min(avg_c+8, 30), 28+random.uniform(-5,5), 45))

# ── Azure VM 사용률 ───────────────────────────────
azure_vms = [
    ("vm-web-001",   "web",  "CC-200", "Standard_D2s_v3", 58),
    ("vm-web-002",   "web",  "CC-200", "Standard_D2s_v3", 62),
    ("vm-api-001",   "api",  "CC-200", "Standard_D4s_v3", 55),
    ("vm-spike-azure","api", "CC-200", "Standard_D4s_v3", 40),  # 3/20 spike
    ("vm-overprov-001","api","CC-200", "Standard_D8s_v3", 22),  # 과잉 (메모리 30%)
    ("vm-overprov-002","api","CC-200", "Standard_D8s_v3", 20),
    ("vm-overprov-003","data","CC-300","Standard_D8s_v3", 18),
]
az_rid_tmpl = "/subscriptions/00000000-0000-0000-0000-000000000001/resourceGroups/rg-{proj}/providers/Microsoft.Compute/virtualMachines/{vm}"

for vm, proj, cc, vmtype, base_cpu in azure_vms:
    for d in DAYS:
        if vm == "vm-spike-azure" and d.day == 20:
            avg_c = 90 + random.uniform(-2, 5)
        else:
            avg_c = base_cpu + random.uniform(-5, 8)
        # 과잉 프로비저닝 VM: 메모리 30%
        avg_mem = 28 + random.uniform(-5, 5) if "overprov" in vm else 55 + random.uniform(-5, 10)
        rid = az_rid_tmpl.format(proj=proj, vm=vm)
        rows_util.append(util_row(d, "Azure", rid, vm, vmtype,
            proj, "prod", cc, avg_c, min(avg_c+20,99), avg_mem, min(avg_mem+20,99)))

total_util = len(rows_util)
print(f"[UTIL] total rows: {total_util}")

with open(os.path.join(BASE, "utilization-sample.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=UTIL_COLS)
    w.writeheader()
    w.writerows(rows_util)
print(f"[UTIL] written: {os.path.join(BASE, 'utilization-sample.csv')}")

print("\nAll sample CSVs generated successfully!")
