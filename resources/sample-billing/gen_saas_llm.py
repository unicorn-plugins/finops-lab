"""
Generate resources/sample-billing/saas-llm-sample.csv

Deterministic (seed=finops-lab-2026) generator for SaaS LLM usage sample.
Period: 2026-03-01 ~ 2026-03-31 (30 days, UTC).
Providers: OpenAI (gpt-4o, gpt-4o-mini, o1) + Anthropic (claude-3-5-sonnet, claude-3-haiku).
Rationale: CSP 빌링(CUR/Export)에 안 잡히는 SaaS LLM API 독립 지출만 수록.

Embedded learning events (references team-planner.md #3-2):
  E1. 3/18 token spike 5x (api project: gpt-4o-mini → gpt-4o for customer-chat feature)
  E2. Oversized-model pattern (data project: using gpt-4o for classification task, should be mini)
  E3. AI tag coverage gap ~12% (missing Project or CostCenter in JSON tags)
  E4. Weekend reduction + weekday peak to mimic real chatbot traffic
"""
from __future__ import annotations
import csv
import hashlib
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = "finops-lab-2026"
random.seed(SEED)

OUT = Path(__file__).parent / "saas-llm-sample.csv"

# Model catalog — per-1M-token USD list price (approximate 2026 rates).
MODELS = {
    "gpt-4o":            {"provider": "openai",    "in":  2.50, "out": 10.00},
    "gpt-4o-mini":       {"provider": "openai",    "in":  0.15, "out":  0.60},
    "o1":                {"provider": "openai",    "in": 15.00, "out": 60.00},
    "claude-3-5-sonnet": {"provider": "anthropic", "in":  3.00, "out": 15.00},
    "claude-3-haiku":    {"provider": "anthropic", "in":  0.25, "out":  1.25},
}

FIELDS = [
    "date", "provider", "model", "project", "cost_center",
    "tokens_input", "tokens_output", "request_count",
    "cost_usd", "api_key_hash", "tags",
]

def hash_key(key_label: str) -> str:
    return "sk-" + hashlib.sha256((SEED + key_label).encode()).hexdigest()[:16]

def fmt_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")

def cost_of(model: str, tin: int, tout: int) -> float:
    m = MODELS[model]
    return round((tin / 1_000_000.0) * m["in"] + (tout / 1_000_000.0) * m["out"], 4)

def jitter(base: int, pct: float = 0.20) -> int:
    """Multiplicative jitter ±pct."""
    lo = int(base * (1.0 - pct))
    hi = int(base * (1.0 + pct))
    return random.randint(max(1, lo), max(lo + 1, hi))

def weekday_weight(d: date, peak: float = 1.0, trough: float = 0.55) -> float:
    # Mon(0)~Fri(4) peak, Sat/Sun trough.
    return peak if d.weekday() < 5 else trough

def make_tags(project: str | None, env: str, owner: str, cost_center: str | None) -> str:
    """Return JSON-encoded tags. E3: drop Project or CostCenter for ~12% of rows."""
    tags: dict[str, str] = {"Environment": env, "Owner": owner}
    if project is not None:
        tags["Project"] = project
    if cost_center is not None:
        tags["CostCenter"] = cost_center
    return json.dumps(tags, ensure_ascii=False)

def should_drop_tag() -> tuple[bool, bool]:
    """Return (drop_project, drop_cost_center) with ~12% combined miss rate."""
    r = random.random()
    if r < 0.07:
        return True, False      # ~7% drop Project
    if r < 0.12:
        return False, True      # ~5% drop CostCenter
    return False, False

def row(d: date, model: str, project: str, cost_center: str, env: str,
        owner: str, base_in: int, base_out: int, base_req: int,
        key_label: str) -> dict:
    tin = jitter(base_in)
    tout = jitter(base_out)
    req = max(1, jitter(base_req, 0.15))
    dp, dc = should_drop_tag()
    tags = make_tags(
        project=None if dp else project,
        env=env,
        owner=owner,
        cost_center=None if dc else cost_center,
    )
    return {
        "date": fmt_date(d),
        "provider": MODELS[model]["provider"],
        "model": model,
        "project": "" if dp else project,
        "cost_center": "" if dc else cost_center,
        "tokens_input": tin,
        "tokens_output": tout,
        "request_count": req,
        "cost_usd": cost_of(model, tin, tout),
        "api_key_hash": hash_key(key_label),
        "tags": tags,
    }

def generate() -> list[dict]:
    start = date(2026, 3, 1)
    days = [start + timedelta(days=i) for i in range(31)]
    rows: list[dict] = []

    # ---- Workload 1: api/customer-chat (CC-200)
    # Baseline: claude-3-5-sonnet daily. 3/18~3/22 token SPIKE 5x via gpt-4o swap (E1).
    for d in days:
        w = weekday_weight(d)
        if date(2026, 3, 18) <= d <= date(2026, 3, 22):
            # E1: model swap + 5x tokens. Keep claude baseline plus extra gpt-4o row.
            rows.append(row(d, "claude-3-5-sonnet", "api", "CC-200", "prod",
                            "api-platform@hbt.co.kr",
                            int(800_000 * w), int(220_000 * w), int(5_500 * w),
                            "api-chat-anthropic"))
            rows.append(row(d, "gpt-4o", "api", "CC-200", "prod",
                            "api-platform@hbt.co.kr",
                            int(3_200_000 * w), int(1_100_000 * w), int(22_000 * w),
                            "api-chat-openai-spike"))
        else:
            rows.append(row(d, "claude-3-5-sonnet", "api", "CC-200", "prod",
                            "api-platform@hbt.co.kr",
                            int(800_000 * w), int(220_000 * w), int(5_500 * w),
                            "api-chat-anthropic"))

    # ---- Workload 2: ml/embedding-summary (CC-300)
    # Daily gpt-4o-mini embedding + summarization job.
    for d in days:
        w = weekday_weight(d, peak=1.0, trough=0.70)
        rows.append(row(d, "gpt-4o-mini", "ml", "CC-300", "prod",
                        "ml-platform@hbt.co.kr",
                        int(2_400_000 * w), int(400_000 * w), int(9_000 * w),
                        "ml-embedding"))

    # ---- Workload 3: data/classification — E2 oversized-model anti-pattern
    # Classification using gpt-4o where gpt-4o-mini would suffice.
    for d in days:
        w = weekday_weight(d, peak=1.0, trough=0.30)
        rows.append(row(d, "gpt-4o", "data", "CC-300", "prod",
                        "data-platform@hbt.co.kr",
                        int(600_000 * w), int(80_000 * w), int(4_500 * w),
                        "data-classifier-oversized"))

    # ---- Workload 4: web/content-assist (CC-200) — Haiku daily
    for d in days:
        w = weekday_weight(d, peak=1.0, trough=0.40)
        rows.append(row(d, "claude-3-haiku", "web", "CC-200", "prod",
                        "web-team@hbt.co.kr",
                        int(300_000 * w), int(80_000 * w), int(1_200 * w),
                        "web-content-haiku"))

    # ---- Workload 4b: api/support-summarization (CC-200) — gpt-4o-mini daily
    for d in days:
        w = weekday_weight(d, peak=1.0, trough=0.60)
        rows.append(row(d, "gpt-4o-mini", "api", "CC-200", "prod",
                        "api-platform@hbt.co.kr",
                        int(1_100_000 * w), int(180_000 * w), int(3_200 * w),
                        "api-support-mini"))

    # ---- Workload 5: R&D/o1 reasoning — infra team R&D sandbox (CC-100)
    rd_days = [days[i] for i in (1, 4, 8, 11, 15, 19, 23, 26, 29)]
    for d in rd_days:
        rows.append(row(d, "o1", "ml", "CC-100", "dev",
                        "rnd@hbt.co.kr",
                        jitter(120_000, 0.30), jitter(180_000, 0.30),
                        jitter(60, 0.30),
                        "rnd-o1-sandbox"))

    # ---- Workload 6: Mixed small batch — claude-3-haiku ad-hoc
    mix_days = [days[i] for i in (2, 6, 9, 13, 17, 20, 24, 27)]
    for d in mix_days:
        rows.append(row(d, "claude-3-haiku", "api", "CC-200", "stg",
                        "api-platform@hbt.co.kr",
                        jitter(180_000), jitter(45_000), jitter(900),
                        "api-haiku-adhoc"))

    # ---- Workload 7: ml/batch-translation — weekly (Mon) Claude Sonnet
    mondays = [d for d in days if d.weekday() == 0]
    for d in mondays:
        rows.append(row(d, "claude-3-5-sonnet", "ml", "CC-300", "prod",
                        "ml-platform@hbt.co.kr",
                        jitter(2_200_000), jitter(900_000), jitter(3_400),
                        "ml-batch-translate"))

    # ---- Workload 8: data/report-gen — weekly (Fri) gpt-4o-mini
    fridays = [d for d in days if d.weekday() == 4]
    for d in fridays:
        rows.append(row(d, "gpt-4o-mini", "data", "CC-300", "prod",
                        "data-platform@hbt.co.kr",
                        jitter(900_000), jitter(260_000), jitter(1_100),
                        "data-report-mini"))

    # ---- Workload 9: dev-assist — scattered days across CC-100 infra team
    dev_days = [days[i] for i in (0, 3, 5, 7, 10, 12, 14, 16, 21, 25, 28)]
    for d in dev_days:
        rows.append(row(d, "claude-3-5-sonnet", "api", "CC-100", "dev",
                        "infra@hbt.co.kr",
                        jitter(150_000, 0.30), jitter(60_000, 0.30),
                        jitter(120, 0.30),
                        "dev-assist-sonnet"))

    return rows

def main() -> None:
    rows = generate()
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    # Post-hoc summary for verification.
    total = len(rows)
    missing_project = sum(1 for r in rows if not r["project"])
    missing_cc = sum(1 for r in rows if not r["cost_center"])
    total_cost = round(sum(r["cost_usd"] for r in rows), 2)
    by_model: dict[str, float] = {}
    for r in rows:
        by_model[r["model"]] = round(by_model.get(r["model"], 0.0) + r["cost_usd"], 2)

    # E1 verification: 3/18~3/22 api-project gpt-4o rows present
    spike = [r for r in rows if r["model"] == "gpt-4o" and r["project"] == "api"
             and "2026-03-18" <= r["date"] <= "2026-03-22"]

    print(f"rows={total}  missing_project={missing_project}  missing_cost_center={missing_cc}")
    print(f"tag_miss_rate={(missing_project + missing_cc) / total:.2%}")
    print(f"total_cost_usd={total_cost}")
    print(f"by_model={by_model}")
    print(f"E1_spike_rows={len(spike)}  (expected 5)")

if __name__ == "__main__":
    main()
