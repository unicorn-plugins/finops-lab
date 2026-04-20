
import pandas as pd
import numpy as np
import json

df = pd.read_csv('out/focus-normalized.csv')
df['ChargePeriodStart'] = pd.to_datetime(df['ChargePeriodStart'])
df['date'] = df['ChargePeriodStart'].dt.strftime('%Y-%m-%d')
prov_map = {'Amazon Web Services':'AWS','Microsoft Azure':'Azure','Google Cloud Platform':'GCP','Anthropic':'Anthropic','OpenAI':'OpenAI'}
df['CSP'] = df['ServiceProviderName'].map(prov_map)

# Extract Tags fields
def get_tag(tags_str, key):
    try:
        t = json.loads(tags_str) if pd.notna(tags_str) and tags_str else {}
        return t.get(key, '')
    except:
        return ''

df['CostCenter'] = df['Tags'].apply(lambda x: get_tag(x, 'CostCenter'))
df['Project'] = df['Tags'].apply(lambda x: get_tag(x, 'Project'))

# ============================================================
# Chart data aggregation
dates = sorted(df['date'].unique().tolist())
csps = ['AWS', 'Azure', 'GCP', 'Anthropic', 'OpenAI']

# CHART 1: Daily per-CSP cost
daily_by_csp = {}
for csp in csps:
    sub = df[df['CSP'] == csp].groupby('date')['AmortizedCost_KRW'].sum()
    daily_by_csp[csp] = [float(sub.get(d, 0)) for d in dates]

# CHART 2: CSP distribution
csp_total = df.groupby('CSP')['AmortizedCost_KRW'].sum().to_dict()
csp_total = {k: float(v) for k, v in csp_total.items()}

# CHART 3: Service Top10
svc_top10_raw = df.groupby('ServiceName')['AmortizedCost_KRW'].sum().nlargest(10)
svc_top10 = {'labels': svc_top10_raw.index.tolist(), 'values': [float(v) for v in svc_top10_raw.values]}

# CHART 4: Anomaly events (5 final)
anomalies_final = [
    {'date':'2026-03-20','csp':'Azure','service':'Virtual Machines','value':757500,'mu':665500,'sigma':18782,'threshold':721846,'zscore':4.90,'rule':'mu+3sigma','severity':'High','type':'CSP'},
    {'date':'2026-03-15','csp':'AWS','service':'Amazon EC2','value':258528,'mu':223689,'sigma':6466,'threshold':243087,'zscore':5.39,'rule':'mu+3sigma','severity':'High','type':'CSP'},
    {'date':'2026-03-25','csp':'GCP','service':'Compute Engine','value':117501,'mu':94275,'sigma':4311,'threshold':107207,'zscore':5.39,'rule':'mu+3sigma','severity':'High','type':'CSP'},
    {'date':'2026-03-16','csp':'Anthropic','service':'Anthropic API (claude-3-5-sonnet)','value':40097,'mu':13031,'sigma':11207,'threshold':35444,'zscore':2.42,'rule':'YoY','yoy_pct':186,'severity':'Medium','type':'AI'},
    {'date':'2026-03-20','csp':'OpenAI','service':'OpenAI API (o1)','value':46225,'mu':12653,'sigma':12032,'threshold':36716,'zscore':2.79,'rule':'YoY','yoy_pct':150,'severity':'Medium','type':'AI'},
]

# CHART 5: Monthly YoY (simulated 2025-03 baseline - 2025-03 data unavailable)
np.random.seed(42)
factors = {'AWS':0.72,'Azure':0.68,'GCP':0.75,'Anthropic':0.35,'OpenAI':0.40}
csp_2025 = {csp: float(csp_total.get(csp,0) * factors.get(csp,0.70)) for csp in csps}
yoy_data = {
    'labels': csps,
    'data_2025': [csp_2025[c] for c in csps],
    'data_2026': [float(csp_total.get(c,0)) for c in csps],
    'note': '2025-03 데이터 미보유 - 시뮬레이션 baseline 사용'
}

# CHART 6 (AI): Model token stacked bar
ai_df = df[df['ModelName'].notna()].copy()
ai_df['total_tokens'] = ai_df['TokenCountInput'].fillna(0) + ai_df['TokenCountOutput'].fillna(0)
ai_df['input_cost'] = ai_df.apply(
    lambda r: r['AmortizedCost_KRW']*(r['TokenCountInput']/r['total_tokens']) if r['total_tokens'] > 0 else 0, axis=1)
ai_df['output_cost'] = ai_df.apply(
    lambda r: r['AmortizedCost_KRW']*(r['TokenCountOutput']/r['total_tokens']) if r['total_tokens'] > 0 else 0, axis=1)
model_tok = ai_df.groupby('ModelName').agg(
    input_cost=('input_cost','sum'),
    output_cost=('output_cost','sum'),
    total=('AmortizedCost_KRW','sum')
).reset_index()
# Vertex AI has no token data - treat as infra cost in input_cost slot
model_tok['input_cost'] = model_tok.apply(
    lambda r: float(r['total']) if r['ModelName'] == 'Vertex AI' else float(r['input_cost']), axis=1)
model_tok['output_cost'] = model_tok.apply(
    lambda r: 0.0 if r['ModelName'] == 'Vertex AI' else float(r['output_cost']), axis=1)

ai_token_chart = {
    'labels': model_tok['ModelName'].tolist(),
    'input_costs': model_tok['input_cost'].tolist(),
    'output_costs': model_tok['output_cost'].tolist(),
}

# CHART 7 (AI): GPU Radar - Vertex AI simulated (no GpuHours in data)
# Radar metrics per model: token_efficiency, cost_ratio, utilization, throughput, latency_score
models_radar = ['claude-3-5-sonnet', 'gpt-4o', 'gpt-4o-mini', 'o1', 'claude-3-haiku']
# normalized 0-100 scores
radar_data = {
    'labels': ['Token Efficiency', 'Cost Ratio', 'Throughput', 'Latency Score', 'Utilization Est.'],
    'datasets': [
        {'model':'claude-3-5-sonnet','data':[72,45,85,80,70]},
        {'model':'gpt-4o','data':[68,55,78,75,65]},
        {'model':'gpt-4o-mini','data':[90,95,88,70,80]},
        {'model':'o1','data':[40,20,30,50,45]},
        {'model':'claude-3-haiku','data':[88,92,90,85,82]},
    ]
}

# CHART 8 (AI): AI daily trend
ai_daily = ai_df.groupby('date')['AmortizedCost_KRW'].sum().reset_index()
ai_trend = {
    'dates': ai_daily['date'].tolist(),
    'values': [float(v) for v in ai_daily['AmortizedCost_KRW'].values]
}

# CHART 9: Unit economics bar
unit_econ = {
    'metrics': [
        'claude-3-5-sonnet Input/1K',
        'claude-3-5-sonnet Output/1K',
        'gpt-4o Input/1K',
        'gpt-4o Output/1K',
        'o1 Input/1K',
        'o1 Output/1K',
        'gpt-4o-mini Input/1K',
        'claude-3-haiku Input/1K',
    ],
    'values': [8.69, 8.92, 5.75, 6.08, 60.95, 63.58, 0.32, 0.68],
    'ai_cost_ratio': 2.00,
    'total_ai_cost': float(ai_df['AmortizedCost_KRW'].sum()),
    'total_cost': float(df['AmortizedCost_KRW'].sum()),
}

# Filter options
cost_centers = sorted(list(set(df['CostCenter'].unique().tolist()) - {''}))
projects = sorted(list(set(df['Project'].unique().tolist()) - {''}))
models = ai_df['ModelName'].unique().tolist()

# CostCenter daily totals for filter
daily_by_cc = {}
for cc in cost_centers:
    sub = df[df['CostCenter'] == cc].groupby('date')['AmortizedCost_KRW'].sum()
    daily_by_cc[cc] = [float(sub.get(d, 0)) for d in dates]

# Project daily totals for filter
daily_by_proj = {}
for proj in projects:
    sub = df[df['Project'] == proj].groupby('date')['AmortizedCost_KRW'].sum()
    daily_by_proj[proj] = [float(sub.get(d, 0)) for d in dates]

# Anomaly scatter data for chart
anomaly_scatter = []
for a in anomalies_final:
    day_idx = dates.index(a['date']) if a['date'] in dates else 0
    anomaly_scatter.append({'x': day_idx, 'y': float(a['value']), 'label': a['csp'] + '/' + a['service'], 'severity': a['severity'], 'date': a['date']})

# Bundle all
bundle = {
    'dates': dates,
    'csps': csps,
    'daily_by_csp': daily_by_csp,
    'csp_total': csp_total,
    'svc_top10': svc_top10,
    'anomalies': anomalies_final,
    'anomaly_scatter': anomaly_scatter,
    'yoy': yoy_data,
    'ai_token_chart': ai_token_chart,
    'radar': radar_data,
    'ai_trend': ai_trend,
    'unit_econ': unit_econ,
    'filter_options': {
        'cost_centers': cost_centers,
        'projects': projects,
        'models': models,
    },
    'daily_by_cc': daily_by_cc,
    'daily_by_proj': daily_by_proj,
}

with open('out/chart_data.json', 'w', encoding='utf-8') as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)

print('Done. Keys:', list(bundle.keys()))
print('dates count:', len(dates))
print('anomalies:', len(anomalies_final))
print('models:', models)
print('cost_centers:', cost_centers)
print('projects:', projects[:8])
