"""
FOCUS v1.3 정규화 스크립트
소스: AWS CUR 2.0, Azure Cost Export, GCP Billing, SaaS LLM
출력: out/focus-normalized.csv
"""
import csv
import json
import os
import math
import re
from datetime import datetime, timedelta

# Vertex AI 모델명 추출 패턴 — sku_description에서 알려진 모델명 탐지
VERTEX_MODEL_PATTERNS = [
    r"gemini-[0-9a-z.\-]+(?:-[a-z]+)?",
    r"text-bison(?:-[0-9a-z]+)?",
    r"chat-bison(?:-[0-9a-z]+)?",
    r"code-bison(?:-[0-9a-z]+)?",
    r"codechat-bison(?:-[0-9a-z]+)?",
    r"textembedding-gecko(?:-[0-9a-z]+)?",
    r"imagen-[0-9a-z.\-]+",
    r"palm-[0-9a-z.\-]+",
]

def extract_vertex_model(sku_description):
    if not sku_description:
        return None
    for pat in VERTEX_MODEL_PATTERNS:
        m = re.search(pat, sku_description, re.IGNORECASE)
        if m:
            return m.group(0).lower()
    return None

# ── 상수 ──────────────────────────────────────────────────────────────────────
EXCHANGE_RATE = 1500
BASE_DIR = r"C:\Users\hiond\workshop\finops-lab"
BILLING_DIR = os.path.join(BASE_DIR, "resources", "sample-billing")
OUT_DIR = os.path.join(BASE_DIR, "out")

# ── FOCUS v1.3 Mandatory 15 + Recommended 2 + Conditional 주요 + AI 확장 5 + AmortizedCost_KRW
FOCUS_COLUMNS = [
    # Mandatory 15
    "BilledCost", "EffectiveCost", "BillingAccountId", "BillingAccountName",
    "BillingCurrency", "BillingPeriodStart", "BillingPeriodEnd",
    "ChargePeriodStart", "ChargePeriodEnd",
    "ChargeCategory", "ChargeClass", "ChargeDescription",
    "ServiceCategory", "ServiceName", "ServiceProviderName",
    # Recommended 2
    "ChargeFrequency", "ServiceSubcategory",
    # Conditional (주요)
    "SubAccountId", "SubAccountName", "RegionId", "RegionName",
    "ResourceId", "ResourceName", "ResourceType",
    "ConsumedQuantity", "ConsumedUnit",
    "PricingCategory",
    "CommitmentDiscountId", "CommitmentDiscountType", "CommitmentDiscountStatus",
    "Tags",
    # AI 확장 5종
    "TokenCountInput", "TokenCountOutput", "ModelName", "GpuHours", "GpuUtilization",
    # 파생 컬럼
    "AmortizedCost_KRW",
]

def round2(v):
    if v is None:
        return None
    return round(float(v), 2)

def to_krw(usd_val):
    if usd_val is None or usd_val == "" or usd_val == "0":
        return 0.0
    return round2(float(usd_val) * EXCHANGE_RATE)

def empty_row():
    return {c: None for c in FOCUS_COLUMNS}

# ── 유틸리티: utilization 조인맵 구축 ─────────────────────────────────────────
def load_utilization():
    """resource_id + date → avg_cpu_percent (GpuUtilization은 null)"""
    util_map = {}
    path = os.path.join(BILLING_DIR, "utilization-sample.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["resource_id"], row["date"])
            util_map[key] = {
                "avg_cpu_percent": row.get("avg_cpu_percent"),
                # GPU 컬럼 없음 → null
                "gpu_utilization": None,
            }
    return util_map

# ── AWS 서비스명 매핑 ─────────────────────────────────────────────────────────
AWS_SERVICE_MAP = {
    "AmazonEC2": ("Amazon EC2", "Compute", "Virtual Machines"),
    "AmazonRDS": ("Amazon RDS", "Databases", "Relational Databases"),
    "AmazonS3": ("Amazon S3", "Storage", "Object Storage"),
    "AWSLambda": ("AWS Lambda", "Compute", "Serverless Compute"),
    "AmazonCloudWatch": ("Amazon CloudWatch", "Management and Governance", "Observability"),
    "AmazonBedrock": ("Amazon Bedrock", "AI and Machine Learning", "Generative AI"),
    "AWSBedrockRuntime": ("Amazon Bedrock", "AI and Machine Learning", "Generative AI"),
}

AZURE_SERVICE_MAP = {
    "Virtual Machines": ("Virtual Machines", "Compute", "Virtual Machines"),
    "SQL Database": ("Azure SQL Database", "Databases", "Relational Databases"),
    "Storage": ("Azure Blob Storage", "Storage", "Object Storage"),
    "App Service": ("Azure App Service", "Web", "Other (Web)"),
    "Azure Monitor": ("Azure Monitor", "Management and Governance", "Observability"),
    "Azure OpenAI": ("Azure OpenAI", "AI and Machine Learning", "Generative AI"),
}

GCP_SERVICE_MAP = {
    "Compute Engine": ("Compute Engine", "Compute", "Virtual Machines"),
    "Cloud SQL": ("Cloud SQL", "Databases", "Relational Databases"),
    "Cloud Storage": ("Cloud Storage", "Storage", "Object Storage"),
    "BigQuery": ("BigQuery", "Analytics", "Data Processing"),
    "Vertex AI": ("Vertex AI", "AI and Machine Learning", "Machine Learning"),
    "Cloud Run": ("Cloud Run", "Compute", "Containers"),
    "Cloud Functions": ("Cloud Functions", "Compute", "Serverless Compute"),
}

# ── AWS CUR 정규화 ────────────────────────────────────────────────────────────
def normalize_aws(util_map):
    rows = []
    path = os.path.join(BILLING_DIR, "aws-cur-sample.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for src in reader:
            r = empty_row()
            # 비용
            unblended = float(src.get("line_item_unblended_cost") or 0)
            blended = float(src.get("line_item_blended_cost") or 0)
            r["BilledCost"] = round2(unblended * EXCHANGE_RATE)
            r["EffectiveCost"] = round2(blended * EXCHANGE_RATE)

            # 계정
            r["BillingAccountId"] = src.get("bill_payer_account_id", "")
            r["BillingAccountName"] = "hbt-prod-aws"
            r["BillingCurrency"] = "KRW"

            # 기간
            period_start = src.get("bill_billing_period_start_date", "2026-03-01")
            if "T" not in period_start:
                period_start = period_start + "T00:00:00Z"
            r["BillingPeriodStart"] = period_start
            r["BillingPeriodEnd"] = "2026-04-01T00:00:00Z"

            charge_start = src.get("line_item_usage_start_date", "")
            charge_end = src.get("line_item_usage_end_date", "")
            # 24:00:00 → 다음날 00:00:00 변환
            if charge_end and "T24:" in charge_end:
                charge_end = charge_end.replace("T24:00:00Z", "")
                dt = datetime.strptime(charge_end, "%Y-%m-%d") + timedelta(days=1)
                charge_end = dt.strftime("%Y-%m-%dT00:00:00Z")
            r["ChargePeriodStart"] = charge_start
            r["ChargePeriodEnd"] = charge_end

            # 청구 분류
            pricing_term = src.get("pricing_term", "OnDemand")
            if pricing_term == "Reserved":
                r["ChargeCategory"] = "Purchase"
                r["PricingCategory"] = "Committed"
                r["ChargeFrequency"] = "One-Time"
            else:
                r["ChargeCategory"] = "Usage"
                r["PricingCategory"] = "Standard"
                r["ChargeFrequency"] = "Usage-Based"
            r["ChargeClass"] = None

            # 서비스
            product_code = src.get("line_item_product_code", "")
            svc = AWS_SERVICE_MAP.get(product_code, (product_code, "Other", "Other"))
            r["ServiceName"] = svc[0]
            r["ServiceCategory"] = svc[1]
            r["ServiceSubcategory"] = svc[2]
            r["ServiceProviderName"] = "Amazon Web Services"
            r["ChargeDescription"] = src.get("line_item_usage_type", "")

            # 리전/리소스
            r["RegionId"] = src.get("product_region", "")
            r["RegionName"] = "Asia Pacific (Seoul)" if src.get("product_region") == "ap-northeast-2" else src.get("product_region", "")
            resource_id = src.get("line_item_resource_id", "")
            r["ResourceId"] = resource_id if resource_id else None
            r["ResourceName"] = resource_id if resource_id else None
            r["ResourceType"] = f"AWS::{product_code.replace('Amazon','').replace('AWS','')}::Instance" if resource_id else None

            # 사용량
            r["ConsumedQuantity"] = src.get("line_item_usage_amount", "")
            r["ConsumedUnit"] = src.get("pricing_unit", "")

            # 약정 할인
            ri_arn = src.get("reservation_reservation_a_r_n", "")
            if ri_arn:
                r["CommitmentDiscountId"] = ri_arn
                r["CommitmentDiscountType"] = "Reserved"
                r["CommitmentDiscountStatus"] = "Used"
            else:
                r["CommitmentDiscountId"] = None
                r["CommitmentDiscountType"] = None
                r["CommitmentDiscountStatus"] = None

            # 태그
            tags = {}
            for k, fk in [("resource_tags_user_project", "Project"),
                          ("resource_tags_user_environment", "Environment"),
                          ("resource_tags_user_owner", "Owner"),
                          ("resource_tags_user_cost_center", "CostCenter")]:
                v = src.get(k, "")
                if v:
                    tags[fk] = v
            r["Tags"] = json.dumps(tags, ensure_ascii=False) if tags else None

            # AI 확장 — AWS는 Bedrock 없으므로 null
            r["TokenCountInput"] = None
            r["TokenCountOutput"] = None
            r["ModelName"] = None
            r["GpuHours"] = None

            # Utilization 조인 — charge_start 날짜 부분
            charge_date = charge_start[:10] if charge_start else ""
            util_key = (resource_id, charge_date)
            util_row = util_map.get(util_key)
            r["GpuUtilization"] = util_row["gpu_utilization"] if util_row else None

            # AmortizedCost — OnDemand는 EffectiveCost와 동일 (UpfrontFee=0)
            r["AmortizedCost_KRW"] = r["EffectiveCost"]

            rows.append(r)
    return rows

# ── Azure Cost Export 정규화 ──────────────────────────────────────────────────
def normalize_azure(util_map):
    rows = []
    path = os.path.join(BILLING_DIR, "azure-export-sample.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for src in reader:
            r = empty_row()
            # Azure는 이미 KRW
            cost_val = float(src.get("CostInBillingCurrency") or 0)
            r["BilledCost"] = round2(cost_val)
            r["EffectiveCost"] = round2(cost_val)

            # 계정
            r["BillingAccountId"] = src.get("SubscriptionId", "")
            r["BillingAccountName"] = src.get("SubscriptionName", "")
            r["BillingCurrency"] = src.get("BillingCurrency", "KRW")

            # 기간
            billing_start = src.get("BillingPeriodStartDate", "2026-03-01")
            if "T" not in billing_start:
                billing_start = billing_start + "T00:00:00Z"
            r["BillingPeriodStart"] = billing_start
            r["BillingPeriodEnd"] = "2026-04-01T00:00:00Z"

            date_val = src.get("Date", "")
            if "T" not in date_val and date_val:
                charge_start = date_val + "T00:00:00Z"
                # 다음날
                dt = datetime.strptime(date_val, "%Y-%m-%d") + timedelta(days=1)
                charge_end = dt.strftime("%Y-%m-%dT00:00:00Z")
            else:
                charge_start = date_val
                charge_end = ""
            r["ChargePeriodStart"] = charge_start
            r["ChargePeriodEnd"] = charge_end

            # 청구 분류
            charge_type = src.get("ChargeType", "Usage")
            if charge_type == "Purchase":
                r["ChargeCategory"] = "Purchase"
                r["ChargeFrequency"] = "One-Time"
                r["PricingCategory"] = "Committed"
            else:
                r["ChargeCategory"] = "Usage"
                r["ChargeFrequency"] = "Usage-Based"
                r["PricingCategory"] = "Standard"
            r["ChargeClass"] = None

            # 서비스
            meter_cat = src.get("MeterCategory", "")
            svc = AZURE_SERVICE_MAP.get(meter_cat, (meter_cat, "Other", "Other"))
            r["ServiceName"] = svc[0]
            r["ServiceCategory"] = svc[1]
            r["ServiceSubcategory"] = svc[2]
            r["ServiceProviderName"] = "Microsoft Azure"
            meter_sub = src.get("MeterSubCategory", "")
            meter_name = src.get("MeterName", "")
            r["ChargeDescription"] = f"{meter_cat} - {meter_sub} - {meter_name}" if meter_sub else f"{meter_cat} - {meter_name}"

            # 리전/리소스
            loc = src.get("ResourceLocation", "")
            r["RegionId"] = loc
            r["RegionName"] = "Korea Central" if loc == "koreacentral" else loc
            resource_id = src.get("ResourceId", "")
            r["ResourceId"] = resource_id if resource_id else None
            r["ResourceName"] = resource_id.split("/")[-1] if resource_id else None
            r["ResourceType"] = None
            r["SubAccountId"] = src.get("ResourceGroup", "")
            r["SubAccountName"] = src.get("ResourceGroup", "")

            # 사용량
            r["ConsumedQuantity"] = src.get("UsageQuantity", "")
            r["ConsumedUnit"] = src.get("UnitOfMeasure", "")

            # 약정 할인
            ri_id = src.get("ReservationId", "")
            if ri_id:
                r["CommitmentDiscountId"] = ri_id
                r["CommitmentDiscountType"] = "Reserved"
                r["CommitmentDiscountStatus"] = "Used"
            else:
                r["CommitmentDiscountId"] = None
                r["CommitmentDiscountType"] = None
                r["CommitmentDiscountStatus"] = None

            # 태그
            raw_tags = src.get("Tags", "")
            if raw_tags and raw_tags.strip():
                try:
                    r["Tags"] = json.dumps(json.loads(raw_tags), ensure_ascii=False)
                except Exception:
                    r["Tags"] = raw_tags
            else:
                r["Tags"] = None

            # AI 확장
            r["TokenCountInput"] = None
            r["TokenCountOutput"] = None
            r["ModelName"] = None
            r["GpuHours"] = None

            # Utilization 조인
            charge_date = date_val[:10] if date_val else ""
            res_name_short = resource_id.split("/")[-1] if resource_id else ""
            util_key = (res_name_short, charge_date)
            util_row = util_map.get(util_key)
            r["GpuUtilization"] = util_row["gpu_utilization"] if util_row else None

            r["AmortizedCost_KRW"] = r["EffectiveCost"]
            rows.append(r)
    return rows

# ── GCP Billing 정규화 ────────────────────────────────────────────────────────
def normalize_gcp(util_map):
    rows = []
    path = os.path.join(BILLING_DIR, "gcp-billing-sample.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for src in reader:
            r = empty_row()
            cost_usd = float(src.get("cost") or 0)
            credits = float(src.get("credits_amount") or 0)
            r["BilledCost"] = round2(cost_usd * EXCHANGE_RATE)
            r["EffectiveCost"] = round2((cost_usd + credits) * EXCHANGE_RATE)

            r["BillingAccountId"] = src.get("billing_account_id", "")
            r["BillingAccountName"] = src.get("project_name", "")
            r["BillingCurrency"] = "KRW"

            invoice_month = src.get("invoice_month", "2026-03")
            billing_start = invoice_month + "-01T00:00:00Z"
            r["BillingPeriodStart"] = billing_start
            r["BillingPeriodEnd"] = "2026-04-01T00:00:00Z"

            charge_start = src.get("usage_start_time", "")
            charge_end = src.get("usage_end_time", "")
            # T24: 처리
            for field_val in [charge_end]:
                if field_val and "T24:" in field_val:
                    charge_end = field_val.replace("T24:00:00Z", "")
                    dt = datetime.strptime(charge_end, "%Y-%m-%d") + timedelta(days=1)
                    charge_end = dt.strftime("%Y-%m-%dT00:00:00Z")
            r["ChargePeriodStart"] = charge_start
            r["ChargePeriodEnd"] = charge_end

            r["ChargeCategory"] = "Usage"
            r["ChargeFrequency"] = "Usage-Based"
            r["PricingCategory"] = "Standard"
            r["ChargeClass"] = None

            svc_desc = src.get("service_description", "")
            svc = GCP_SERVICE_MAP.get(svc_desc, (svc_desc, "Other", "Other"))
            r["ServiceName"] = svc[0]
            r["ServiceCategory"] = svc[1]
            r["ServiceSubcategory"] = svc[2]
            r["ServiceProviderName"] = "Google Cloud Platform"
            r["ChargeDescription"] = src.get("sku_description", "")

            loc = src.get("location_region", "")
            r["RegionId"] = loc
            r["RegionName"] = "Seoul" if loc == "asia-northeast3" else loc
            resource_global = src.get("resource_global_name", "")
            resource_name = src.get("resource_name", "")
            r["ResourceId"] = resource_global if resource_global else None
            r["ResourceName"] = resource_name if resource_name else None
            r["ResourceType"] = None
            r["SubAccountId"] = src.get("project_id", "")
            r["SubAccountName"] = src.get("project_name", "")

            r["ConsumedQuantity"] = src.get("usage_amount", "")
            r["ConsumedUnit"] = src.get("usage_unit", "")

            credits_type = src.get("credits_type", "")
            if credits_type == "COMMITTED_USAGE_DISCOUNT":
                r["CommitmentDiscountType"] = "Committed Use"
                r["CommitmentDiscountStatus"] = "Used"
            else:
                r["CommitmentDiscountId"] = None
                r["CommitmentDiscountType"] = None
                r["CommitmentDiscountStatus"] = None

            raw_labels = src.get("labels", "")
            if raw_labels and raw_labels.strip():
                try:
                    r["Tags"] = json.dumps(json.loads(raw_labels), ensure_ascii=False)
                except Exception:
                    r["Tags"] = raw_labels
            else:
                r["Tags"] = None

            # AI 확장 — Vertex AI 행
            is_ai = svc_desc == "Vertex AI"
            r["TokenCountInput"] = None
            r["TokenCountOutput"] = None
            r["ModelName"] = extract_vertex_model(src.get("sku_description", "")) if is_ai else None
            r["GpuHours"] = None

            # Utilization 조인
            charge_date = charge_start[:10] if charge_start else ""
            res_short = resource_name if resource_name else ""
            util_key = (res_short, charge_date)
            util_row = util_map.get(util_key)
            r["GpuUtilization"] = util_row["gpu_utilization"] if util_row else None

            r["AmortizedCost_KRW"] = r["EffectiveCost"]
            rows.append(r)
    return rows

# ── SaaS LLM 정규화 ──────────────────────────────────────────────────────────
def normalize_saas_llm():
    rows = []
    path = os.path.join(BILLING_DIR, "saas-llm-sample.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for src in reader:
            r = empty_row()
            cost_usd = float(src.get("cost_usd") or 0)
            cost_krw = round2(cost_usd * EXCHANGE_RATE)
            r["BilledCost"] = cost_krw
            r["EffectiveCost"] = cost_krw

            provider = src.get("provider", "")
            if provider == "anthropic":
                r["BillingAccountId"] = src.get("api_key_hash", "")
                r["BillingAccountName"] = "hbt-anthropic"
                r["ServiceProviderName"] = "Anthropic"
                r["ServiceName"] = "Anthropic API"
                r["ServiceCategory"] = "AI and Machine Learning"
                r["ServiceSubcategory"] = "Generative AI"
            elif provider == "openai":
                r["BillingAccountId"] = src.get("api_key_hash", "")
                r["BillingAccountName"] = "hbt-openai"
                r["ServiceProviderName"] = "OpenAI"
                r["ServiceName"] = "OpenAI API"
                r["ServiceCategory"] = "AI and Machine Learning"
                r["ServiceSubcategory"] = "Generative AI"
            else:
                r["BillingAccountId"] = src.get("api_key_hash", "")
                r["BillingAccountName"] = f"hbt-{provider}"
                r["ServiceProviderName"] = provider
                r["ServiceName"] = f"{provider} API"
                r["ServiceCategory"] = "AI and Machine Learning"
                r["ServiceSubcategory"] = "Generative AI"

            r["BillingCurrency"] = "KRW"

            date_val = src.get("date", "")
            r["BillingPeriodStart"] = "2026-03-01T00:00:00Z"
            r["BillingPeriodEnd"] = "2026-04-01T00:00:00Z"
            if date_val:
                r["ChargePeriodStart"] = date_val + "T00:00:00Z"
                dt = datetime.strptime(date_val, "%Y-%m-%d") + timedelta(days=1)
                r["ChargePeriodEnd"] = dt.strftime("%Y-%m-%dT00:00:00Z")
            else:
                r["ChargePeriodStart"] = None
                r["ChargePeriodEnd"] = None

            r["ChargeCategory"] = "Usage"
            r["ChargeFrequency"] = "Usage-Based"
            r["PricingCategory"] = "Standard"
            r["ChargeClass"] = None

            model = src.get("model", "")
            r["ChargeDescription"] = f"{provider} {model} API usage"
            r["ModelName"] = model

            r["RegionId"] = None
            r["RegionName"] = None
            r["ResourceId"] = None
            r["ResourceName"] = None
            r["ResourceType"] = None

            project = src.get("project", "")
            r["SubAccountId"] = project if project else None
            r["SubAccountName"] = project if project else None

            # 토큰 사용량
            tokens_in = src.get("tokens_input", "")
            tokens_out = src.get("tokens_output", "")
            r["TokenCountInput"] = int(tokens_in) if tokens_in else None
            r["TokenCountOutput"] = int(tokens_out) if tokens_out else None
            r["ConsumedQuantity"] = None
            r["ConsumedUnit"] = None

            # GPU 없음
            r["GpuHours"] = None
            r["GpuUtilization"] = None

            # 태그
            raw_tags = src.get("tags", "")
            if raw_tags and raw_tags.strip():
                try:
                    r["Tags"] = json.dumps(json.loads(raw_tags), ensure_ascii=False)
                except Exception:
                    r["Tags"] = raw_tags
            else:
                r["Tags"] = None

            # AmortizedCost — SaaS는 EffectiveCost와 동일
            r["AmortizedCost_KRW"] = cost_krw

            rows.append(r)
    return rows

# ── 메인 ─────────────────────────────────────────────────────────────────────
def main():
    print("utilization 데이터 로드 중...")
    util_map = load_utilization()
    print(f"  utilization 레코드: {len(util_map)}")

    print("AWS CUR 정규화 중...")
    aws_rows = normalize_aws(util_map)
    print(f"  AWS 행: {len(aws_rows)}")

    print("Azure Cost Export 정규화 중...")
    azure_rows = normalize_azure(util_map)
    print(f"  Azure 행: {len(azure_rows)}")

    print("GCP Billing 정규화 중...")
    gcp_rows = normalize_gcp(util_map)
    print(f"  GCP 행: {len(gcp_rows)}")

    print("SaaS LLM 정규화 중...")
    saas_rows = normalize_saas_llm()
    print(f"  SaaS LLM 행: {len(saas_rows)}")

    all_rows = aws_rows + azure_rows + gcp_rows + saas_rows
    total = len(all_rows)
    print(f"\n총 정규화 행: {total}")

    # 출력 CSV 저장
    out_path = os.path.join(OUT_DIR, "focus-normalized.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FOCUS_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"저장 완료: {out_path}")

    # ── 검증 ──────────────────────────────────────────────────────────────────
    print("\n=== 검증 ===")

    # 1) FOCUS Mandatory 15종 전체 존재 여부
    mandatory = ["BilledCost", "EffectiveCost", "BillingAccountId", "BillingAccountName",
                 "BillingCurrency", "BillingPeriodStart", "BillingPeriodEnd",
                 "ChargePeriodStart", "ChargePeriodEnd",
                 "ChargeCategory", "ChargeClass", "ChargeDescription",
                 "ServiceCategory", "ServiceName", "ServiceProviderName"]
    print(f"Mandatory 15종 컬럼 존재: {all(c in FOCUS_COLUMNS for c in mandatory)}")

    # 2) AI 행 수 (GCP Vertex AI + SaaS LLM 전체)
    ai_rows = [r for r in all_rows if r.get("ServiceCategory") == "AI and Machine Learning"]
    print(f"AI 관련 행 수: {len(ai_rows)}")

    # AI 확장 컬럼 채워진 행 (TokenCountInput or ModelName)
    ai_ext_filled = [r for r in ai_rows if r.get("TokenCountInput") is not None or r.get("ModelName") is not None]
    print(f"AI 확장 컬럼 채워진 행: {len(ai_ext_filled)}")

    # 3) KRW 환산 검증 (5행 샘플)
    print("\n=== KRW 샘플 검증 (AWS 5행) ===")
    with open(os.path.join(BILLING_DIR, "aws-cur-sample.csv"), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        src_rows = list(reader)[:5]
    for i, (src, norm) in enumerate(zip(src_rows, aws_rows[:5])):
        expected = round(float(src["line_item_unblended_cost"]) * 1500, 2)
        actual = norm["BilledCost"]
        match = abs(expected - float(actual or 0)) < 0.01
        print(f"  AWS 행{i+1}: USD={src['line_item_unblended_cost']} × 1500 = {expected} KRW → 정규화={actual} → {'OK' if match else 'NG'}")

    # 4) 월 총합 검증
    print("\n=== 월 총합 KRW 검증 ===")
    # 원본 합산
    aws_total_usd = sum(float(r.get("line_item_unblended_cost") or 0) for r in src_rows)
    with open(os.path.join(BILLING_DIR, "aws-cur-sample.csv"), newline="", encoding="utf-8") as f:
        aws_total_usd = sum(float(r.get("line_item_unblended_cost") or 0) for r in csv.DictReader(f))
    with open(os.path.join(BILLING_DIR, "azure-export-sample.csv"), newline="", encoding="utf-8") as f:
        azure_total_krw = sum(float(r.get("CostInBillingCurrency") or 0) for r in csv.DictReader(f))
    with open(os.path.join(BILLING_DIR, "gcp-billing-sample.csv"), newline="", encoding="utf-8") as f:
        gcp_total_usd = sum(float(r.get("cost") or 0) for r in csv.DictReader(f))
    with open(os.path.join(BILLING_DIR, "saas-llm-sample.csv"), newline="", encoding="utf-8") as f:
        saas_total_usd = sum(float(r.get("cost_usd") or 0) for r in csv.DictReader(f))

    orig_total_krw = round(aws_total_usd * 1500 + azure_total_krw + gcp_total_usd * 1500 + saas_total_usd * 1500, 2)
    norm_total_krw = round(sum(float(r.get("BilledCost") or 0) for r in all_rows), 2)
    diff = abs(orig_total_krw - norm_total_krw)
    print(f"  원본 합산 KRW: {orig_total_krw:,.2f}")
    print(f"  정규화 합산 KRW: {norm_total_krw:,.2f}")
    print(f"  차이: {diff:.2f} KRW → {'OK (±0.01 이내)' if diff <= 0.01 else f'NG (차이={diff})'}")

    print("\n=== AmortizedCost 검증 (OnDemand = EffectiveCost) ===")
    for r in aws_rows[:5]:
        match = abs(float(r["AmortizedCost_KRW"] or 0) - float(r["EffectiveCost"] or 0)) < 0.01
        print(f"  EffectiveCost={r['EffectiveCost']} AmortizedCost={r['AmortizedCost_KRW']} → {'OK' if match else 'NG'}")

    # 소스별 행 수 요약
    print("\n=== 소스별 행 수 ===")
    print(f"  AWS:      {len(aws_rows)}")
    print(f"  Azure:    {len(azure_rows)}")
    print(f"  GCP:      {len(gcp_rows)}")
    print(f"  SaaS LLM: {len(saas_rows)}")
    print(f"  합계:     {total}")

    return {
        "total_rows": total,
        "aws_rows": len(aws_rows),
        "azure_rows": len(azure_rows),
        "gcp_rows": len(gcp_rows),
        "saas_rows": len(saas_rows),
        "ai_rows": len(ai_rows),
        "orig_total_krw": orig_total_krw,
        "norm_total_krw": norm_total_krw,
        "diff": diff,
    }

if __name__ == "__main__":
    main()
