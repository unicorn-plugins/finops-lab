
import json

with open('out/chart_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Serialize data as compact JSON strings for embedding
dates_json = json.dumps(d['dates'])
csps_json = json.dumps(d['csps'])
daily_by_csp_json = json.dumps(d['daily_by_csp'])
csp_total_json = json.dumps(d['csp_total'])
svc_top10_json = json.dumps(d['svc_top10'])
anomalies_json = json.dumps(d['anomalies'])
anomaly_scatter_json = json.dumps(d['anomaly_scatter'])
yoy_json = json.dumps(d['yoy'])
ai_token_chart_json = json.dumps(d['ai_token_chart'])
radar_json = json.dumps(d['radar'])
ai_trend_json = json.dumps(d['ai_trend'])
unit_econ_json = json.dumps(d['unit_econ'])
filter_options_json = json.dumps(d['filter_options'])
daily_by_cc_json = json.dumps(d['daily_by_cc'])
daily_by_proj_json = json.dumps(d['daily_by_proj'])

# Anomaly banner items
anomaly_rows = ""
for a in d['anomalies']:
    sev_cls = 'sev-high' if a['severity'] == 'High' else 'sev-medium'
    if a['rule'] == 'YoY':
        rule_detail = f"YoY +{a.get('yoy_pct',0)}% (전년 동기 대비 50% 이상 초과)"
    else:
        normal_range = f"μ={a['mu']:,} ± 3σ={a['sigma']:,}"
        rule_detail = f"{a['rule']} (z={a['zscore']}) | 정상범위: {normal_range} KRW"
    anomaly_rows += f"""
      <div class="anomaly-card {sev_cls}">
        <span class="badge">{a['severity']}</span>
        <strong>{a['csp']}</strong> / {a['service']}<br>
        <span class="date-tag">{a['date']}</span>
        <span class="val">{a['value']:,.0f} KRW</span><br>
        <small>탐지룰: {rule_detail}</small>
      </div>"""

html = f"""<!DOCTYPE html>
<html lang="ko" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinOps Cost Dashboard — HBT 2026-03</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg: #f4f6f9;
      --card: #ffffff;
      --text: #1a1a2e;
      --sub: #555;
      --border: #dde1e7;
      --accent: #3b82f6;
      --tab-active: #2563eb;
      --tab-bg: #e5e7eb;
      --banner-bg: #fff7ed;
      --banner-border: #f97316;
      --high: #dc2626;
      --medium: #d97706;
      --low: #16a34a;
    }}
    [data-theme="dark"] {{
      --bg: #0f172a;
      --card: #1e293b;
      --text: #e2e8f0;
      --sub: #94a3b8;
      --border: #334155;
      --accent: #60a5fa;
      --tab-active: #3b82f6;
      --tab-bg: #1e293b;
      --banner-bg: #1c1400;
      --banner-border: #d97706;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); transition: all .3s; }}
    header {{ background: var(--card); border-bottom: 2px solid var(--accent); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
    header h1 {{ font-size: 1.2rem; font-weight: 700; color: var(--accent); }}
    header .subtitle {{ font-size: .75rem; color: var(--sub); margin-top: 2px; }}
    .header-right {{ display: flex; gap: 10px; align-items: center; }}
    .dark-toggle {{ cursor: pointer; background: var(--tab-bg); border: 1px solid var(--border); color: var(--text); padding: 6px 14px; border-radius: 20px; font-size: .8rem; }}
    .dark-toggle:hover {{ background: var(--accent); color: #fff; }}

    /* Anomaly Banner */
    .anomaly-banner {{ background: var(--banner-bg); border-left: 4px solid var(--banner-border); padding: 14px 20px; margin: 16px 20px; border-radius: 6px; }}
    .anomaly-banner h2 {{ font-size: .95rem; color: var(--banner-border); margin-bottom: 10px; }}
    .anomaly-cards {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .anomaly-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px; min-width: 220px; flex: 1; font-size: .78rem; line-height: 1.6; }}
    .anomaly-card.sev-high {{ border-left: 4px solid var(--high); }}
    .anomaly-card.sev-medium {{ border-left: 4px solid var(--medium); }}
    .badge {{ display: inline-block; font-size: .7rem; font-weight: 700; padding: 1px 7px; border-radius: 10px; margin-right: 6px; color: #fff; }}
    .sev-high .badge {{ background: var(--high); }}
    .sev-medium .badge {{ background: var(--medium); }}
    .date-tag {{ background: #e0e7ff; color: #3730a3; border-radius: 4px; padding: 0 5px; font-size: .7rem; margin-right: 6px; }}
    [data-theme="dark"] .date-tag {{ background: #1e1b4b; color: #a5b4fc; }}
    .val {{ font-weight: 600; color: var(--accent); }}
    small {{ color: var(--sub); }}

    /* Filters */
    .filter-bar {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 10px 20px; display: flex; flex-wrap: wrap; gap: 14px; align-items: center; font-size: .8rem; }}
    .filter-bar label {{ color: var(--sub); font-weight: 600; }}
    .filter-bar select {{ border: 1px solid var(--border); border-radius: 4px; padding: 4px 8px; background: var(--bg); color: var(--text); font-size: .8rem; }}
    .filter-bar input[type=range] {{ width: 180px; accent-color: var(--accent); }}
    .range-label {{ font-size: .78rem; color: var(--sub); min-width: 170px; }}

    /* Tabs */
    .tabs {{ display: flex; padding: 0 20px; background: var(--card); border-bottom: 1px solid var(--border); }}
    .tab-btn {{ padding: 10px 24px; cursor: pointer; border: none; background: transparent; font-size: .85rem; font-weight: 600; color: var(--sub); border-bottom: 3px solid transparent; transition: all .2s; }}
    .tab-btn.active {{ color: var(--tab-active); border-bottom-color: var(--tab-active); }}
    .tab-btn:hover {{ color: var(--accent); }}

    /* Main content */
    .main {{ padding: 16px 20px; }}
    .tab-panel {{ display: none; }}
    .tab-panel.active {{ display: block; }}
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .grid-1 {{ display: grid; grid-template-columns: 1fr; gap: 16px; }}
    @media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}

    /* Cards */
    .chart-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
    .chart-card h3 {{ font-size: .85rem; font-weight: 700; color: var(--sub); margin-bottom: 10px; text-transform: uppercase; letter-spacing: .05em; }}
    .chart-wrap {{ position: relative; height: 260px; }}
    .chart-wrap.tall {{ height: 320px; }}
    .chart-wrap.short {{ height: 200px; }}

    /* Unit economics table */
    .ue-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }}
    .ue-item {{ background: var(--bg); border-radius: 6px; padding: 10px 12px; }}
    .ue-item .ue-val {{ font-size: 1.3rem; font-weight: 700; color: var(--accent); }}
    .ue-item .ue-label {{ font-size: .72rem; color: var(--sub); margin-top: 2px; }}
    .ue-item.highlight {{ background: linear-gradient(135deg, #eff6ff, #dbeafe); border: 1px solid #bfdbfe; }}
    [data-theme="dark"] .ue-item.highlight {{ background: linear-gradient(135deg, #1e3a5f, #1e3a5f); border-color: #1d4ed8; }}

    footer {{ text-align: center; padding: 12px; font-size: .72rem; color: var(--sub); border-top: 1px solid var(--border); margin-top: 10px; }}
  </style>
</head>
<body>

<header>
  <div>
    <div class="header-right" style="flex-direction:column;align-items:flex-start;">
      <h1>FinOps Cost Dashboard</h1>
      <div class="subtitle">(주)하이브리지텔레콤 · 분석기간: 2026-03-01 ~ 2026-03-31 · 총비용: 42,256,382 KRW</div>
    </div>
  </div>
  <div class="header-right">
    <button class="dark-toggle" onclick="toggleDark()">다크모드</button>
  </div>
</header>

<!-- Anomaly Banner -->
<div class="anomaly-banner">
  <h2>이상 비용 탐지 결과 — 5건 (CSP 3건 + AI 2건)</h2>
  <div class="anomaly-cards">{anomaly_rows}
  </div>
</div>

<!-- Filter Bar -->
<div class="filter-bar">
  <label>기간:</label>
  <input type="range" id="rangeSlider" min="0" max="30" value="30" step="1" oninput="updateDateRange(this.value)">
  <span class="range-label" id="rangeLabel">2026-03-01 ~ 2026-03-31</span>
  <label>CostCenter:</label>
  <select id="ccFilter" onchange="applyFilters()">
    <option value="">전체</option>
    <option value="CC-100">CC-100</option>
    <option value="CC-200">CC-200</option>
    <option value="CC-300">CC-300</option>
  </select>
  <label>Project:</label>
  <select id="projFilter" onchange="applyFilters()">
    <option value="">전체</option>
    <option value="api">api</option>
    <option value="data">data</option>
    <option value="ml">ml</option>
    <option value="web">web</option>
  </select>
  <label>Model:</label>
  <select id="modelFilter" onchange="applyFilters()">
    <option value="">전체</option>
    <option value="claude-3-5-sonnet">claude-3-5-sonnet</option>
    <option value="gpt-4o">gpt-4o</option>
    <option value="gpt-4o-mini">gpt-4o-mini</option>
    <option value="o1">o1</option>
    <option value="claude-3-haiku">claude-3-haiku</option>
    <option value="Vertex AI">Vertex AI</option>
  </select>
</div>

<!-- Tabs -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('csp', this)">CSP 비용 분석</button>
  <button class="tab-btn" onclick="switchTab('ai', this)">AI/LLM 비용 분석</button>
</div>

<div class="main">

  <!-- CSP Tab -->
  <div id="tab-csp" class="tab-panel active">
    <div class="grid-1" style="margin-bottom:16px;">
      <div class="chart-card">
        <h3>일별 총비용 추이 (CSP별)</h3>
        <div class="chart-wrap tall"><canvas id="chart1"></canvas></div>
      </div>
    </div>
    <div class="grid-2">
      <div class="chart-card">
        <h3>CSP별 비용 분포</h3>
        <div class="chart-wrap"><canvas id="chart2"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>서비스별 Top 10 비용</h3>
        <div class="chart-wrap"><canvas id="chart3"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>이상 이벤트 타임라인</h3>
        <div class="chart-wrap"><canvas id="chart4"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>월별 YoY 비교 <small style="font-size:.7rem;color:#aaa;">(2025-03 시뮬레이션 baseline)</small></h3>
        <div class="chart-wrap"><canvas id="chart5"></canvas></div>
      </div>
    </div>
  </div>

  <!-- AI Tab -->
  <div id="tab-ai" class="tab-panel">
    <div class="grid-2">
      <div class="chart-card">
        <h3>모델별 토큰 비용 (입력/출력)</h3>
        <div class="chart-wrap"><canvas id="chart6"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>모델 성능 지표 분포 (Radar)</h3>
        <div class="chart-wrap"><canvas id="chart7"></canvas></div>
      </div>
    </div>
    <div class="grid-1" style="margin-top:16px;">
      <div class="chart-card">
        <h3>AI 비용 트렌드 (일별)</h3>
        <div class="chart-wrap short"><canvas id="chart8"></canvas></div>
      </div>
    </div>
    <div class="grid-1" style="margin-top:16px;">
      <div class="chart-card">
        <h3>AI 단위경제 지표</h3>
        <div class="ue-grid">
          <div class="ue-item highlight">
            <div class="ue-val">2.00%</div>
            <div class="ue-label">AI 비용 비중 (전체 대비)</div>
          </div>
          <div class="ue-item highlight">
            <div class="ue-val">843,695 KRW</div>
            <div class="ue-label">AI 총비용 (2026-03)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">8.69 KRW</div>
            <div class="ue-label">Cost/1K Input Tokens (claude-3-5-sonnet)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">8.92 KRW</div>
            <div class="ue-label">Cost/1K Output Tokens (claude-3-5-sonnet)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">5.75 KRW</div>
            <div class="ue-label">Cost/1K Input Tokens (gpt-4o)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">60.95 KRW</div>
            <div class="ue-label">Cost/1K Input Tokens (o1)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">0.32 KRW</div>
            <div class="ue-label">Cost/1K Input Tokens (gpt-4o-mini)</div>
          </div>
          <div class="ue-item">
            <div class="ue-val">370 KRW</div>
            <div class="ue-label">Cost/GPU-Hour (Vertex AI, 128h × 62% 추정, 시뮬레이션)</div>
          </div>
        </div>
        <div class="chart-wrap short" style="margin-top:14px;"><canvas id="chart9"></canvas></div>
      </div>
    </div>
  </div>

</div>

<footer>FinOps Cost Analyst Dashboard · HBT 2026-03 · Chart.js 4.x · 이상탐지: mu+3sigma / mu+2sigma</footer>

<script>
// ============================================================
// Inline data
const DATES = {dates_json};
const CSPS = {csps_json};
const DAILY = {daily_by_csp_json};
const CSP_TOTAL = {csp_total_json};
const SVC_TOP10 = {svc_top10_json};
const ANOMALIES = {anomalies_json};
const ANOMALY_SCATTER = {anomaly_scatter_json};
const YOY = {yoy_json};
const AI_TOKEN = {ai_token_chart_json};
const RADAR = {radar_json};
const AI_TREND = {ai_trend_json};
const UNIT_ECON = {unit_econ_json};
const FILTER_OPT = {filter_options_json};
const DAILY_BY_CC = {daily_by_cc_json};
const DAILY_BY_PROJ = {daily_by_proj_json};

// Color palette
const CSP_COLORS = {{
  'AWS': '#ff9900',
  'Azure': '#0078d4',
  'GCP': '#4285f4',
  'Anthropic': '#cc785c',
  'OpenAI': '#10a37f'
}};
const RADAR_COLORS = ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6'];

let dateRange = 30;
let charts = {{}};

// Theme
function toggleDark() {{
  const html = document.documentElement;
  html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  rebuildAllCharts();
}}

function getColor(alpha=1) {{
  return getComputedStyle(document.documentElement).getPropertyValue('--text').trim();
}}

function chartDefaults() {{
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {{
    gridColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.07)',
    textColor: isDark ? '#94a3b8' : '#555',
  }};
}}

// Range slider
function updateDateRange(val) {{
  dateRange = parseInt(val);
  const startDate = DATES[30 - dateRange] || DATES[0];
  const endDate = DATES[30];
  document.getElementById('rangeLabel').textContent = startDate + ' ~ ' + endDate;
  rebuildChart1();
  rebuildChart4();
  rebuildChart8();
}}

function applyFilters() {{
  // Filters affect chart labels/titles - full rebuild for simplicity
  rebuildAllCharts();
}}

// ============================================================
// Chart 1: Daily trend line
function buildChart1() {{
  const cd = chartDefaults();
  const slicedDates = DATES.slice(30 - dateRange);
  const ccFilter = document.getElementById('ccFilter').value;
  const projFilter = document.getElementById('projFilter').value;

  let datasets;
  if (ccFilter) {{
    // Show single CostCenter total vs all CSPs
    datasets = [{{
      label: 'CostCenter: ' + ccFilter,
      data: (DAILY_BY_CC[ccFilter] || []).slice(30 - dateRange),
      borderColor: '#8b5cf6',
      backgroundColor: '#8b5cf622',
      fill: false, tension: 0.3, pointRadius: 3,
    }}];
  }} else if (projFilter) {{
    datasets = [{{
      label: 'Project: ' + projFilter,
      data: (DAILY_BY_PROJ[projFilter] || []).slice(30 - dateRange),
      borderColor: '#f59e0b',
      backgroundColor: '#f59e0b22',
      fill: false, tension: 0.3, pointRadius: 3,
    }}];
  }} else {{
    datasets = CSPS.map(csp => ({{
      label: csp,
      data: DAILY[csp].slice(30 - dateRange),
      borderColor: CSP_COLORS[csp] || '#999',
      backgroundColor: CSP_COLORS[csp] + '22',
      fill: false,
      tension: 0.3,
      pointRadius: 3,
    }}));
  }}
  charts.c1 = new Chart(document.getElementById('chart1'), {{
    type: 'line',
    data: {{ labels: slicedDates, datasets }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ labels: {{ color: cd.textColor, font: {{ size: 11 }} }} }},
        tooltip: {{ mode: 'index', intersect: false }}
      }},
      scales: {{
        x: {{ ticks: {{ color: cd.textColor, maxRotation: 45, maxTicksLimit: 10 }}, grid: {{ color: cd.gridColor }} }},
        y: {{ ticks: {{ color: cd.textColor, callback: v => (v/1000).toFixed(0)+'K' }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

// Chart 2: CSP Doughnut
function buildChart2() {{
  const cd = chartDefaults();
  const labels = Object.keys(CSP_TOTAL);
  const vals = Object.values(CSP_TOTAL);
  charts.c2 = new Chart(document.getElementById('chart2'), {{
    type: 'doughnut',
    data: {{
      labels,
      datasets: [{{ data: vals, backgroundColor: labels.map(l => CSP_COLORS[l] || '#999'), borderWidth: 2 }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ position: 'right', labels: {{ color: cd.textColor, font: {{ size: 11 }} }} }},
        tooltip: {{ callbacks: {{ label: ctx => ctx.label + ': ' + (ctx.raw/1000000).toFixed(2) + 'M KRW' }} }}
      }}
    }}
  }});
}}

// Chart 3: Service Top10 HBar
function buildChart3() {{
  const cd = chartDefaults();
  charts.c3 = new Chart(document.getElementById('chart3'), {{
    type: 'bar',
    data: {{
      labels: SVC_TOP10.labels,
      datasets: [{{ label: '비용 (KRW)', data: SVC_TOP10.values, backgroundColor: '#3b82f6cc', borderRadius: 4 }}]
    }},
    options: {{
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{ callbacks: {{ label: ctx => (ctx.raw/1000000).toFixed(2) + 'M KRW' }} }}
      }},
      scales: {{
        x: {{ ticks: {{ color: cd.textColor, callback: v => (v/1000000).toFixed(1)+'M' }}, grid: {{ color: cd.gridColor }} }},
        y: {{ ticks: {{ color: cd.textColor, font: {{ size: 10 }} }}, grid: {{ display: false }} }}
      }}
    }}
  }});
}}

// Chart 4: Anomaly Scatter
function buildChart4() {{
  const cd = chartDefaults();
  const slicedDates = DATES.slice(30 - dateRange);
  const highData = ANOMALY_SCATTER.filter(a => a.severity === 'High').map(a => ({{ x: a.x - (30 - dateRange), y: a.y, label: a.label, date: a.date }}));
  const medData = ANOMALY_SCATTER.filter(a => a.severity === 'Medium').map(a => ({{ x: a.x - (30 - dateRange), y: a.y, label: a.label, date: a.date }}));
  charts.c4 = new Chart(document.getElementById('chart4'), {{
    type: 'scatter',
    data: {{
      datasets: [
        {{ label: 'High', data: highData, backgroundColor: '#dc2626cc', pointRadius: 12, pointStyle: 'triangle' }},
        {{ label: 'Medium', data: medData, backgroundColor: '#d97706cc', pointRadius: 10, pointStyle: 'rectRot' }},
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ labels: {{ color: cd.textColor }} }},
        tooltip: {{ callbacks: {{ label: ctx => ctx.raw.date + ' ' + ctx.raw.label + ': ' + (ctx.raw.y/1000).toFixed(0)+'K KRW' }} }}
      }},
      scales: {{
        x: {{ min: 0, max: dateRange, title: {{ display: true, text: '일자 (0=Mar 1)', color: cd.textColor }}, ticks: {{ color: cd.textColor }}, grid: {{ color: cd.gridColor }} }},
        y: {{ ticks: {{ color: cd.textColor, callback: v => (v/1000).toFixed(0)+'K' }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

// Chart 5: YoY Grouped Bar
function buildChart5() {{
  const cd = chartDefaults();
  charts.c5 = new Chart(document.getElementById('chart5'), {{
    type: 'bar',
    data: {{
      labels: YOY.labels,
      datasets: [
        {{ label: '2025-03 (시뮬)', data: YOY.data_2025, backgroundColor: '#94a3b8aa', borderRadius: 4 }},
        {{ label: '2026-03', data: YOY.data_2026, backgroundColor: '#3b82f6cc', borderRadius: 4 }},
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{
        legend: {{ labels: {{ color: cd.textColor }} }},
        tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ': ' + (ctx.raw/1000000).toFixed(2)+'M KRW' }} }}
      }},
      scales: {{
        x: {{ ticks: {{ color: cd.textColor }}, grid: {{ display: false }} }},
        y: {{ ticks: {{ color: cd.textColor, callback: v => (v/1000000).toFixed(1)+'M' }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

// Chart 6: Model Token Stacked Bar
function buildChart6() {{
  const cd = chartDefaults();
  const modelFilter = document.getElementById('modelFilter').value;
  let labels = AI_TOKEN.labels;
  let inp = AI_TOKEN.input_costs;
  let out = AI_TOKEN.output_costs;
  if (modelFilter) {{
    const idx = labels.indexOf(modelFilter);
    if (idx >= 0) {{ labels = [labels[idx]]; inp = [inp[idx]]; out = [out[idx]]; }}
  }}
  charts.c6 = new Chart(document.getElementById('chart6'), {{
    type: 'bar',
    data: {{
      labels,
      datasets: [
        {{ label: '입력 토큰 비용', data: inp, backgroundColor: '#3b82f6cc', borderRadius: 4 }},
        {{ label: '출력 토큰 비용', data: out, backgroundColor: '#10b981cc', borderRadius: 4 }},
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ labels: {{ color: cd.textColor }} }}, tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ': ' + (ctx.raw/1000).toFixed(1)+'K KRW' }} }} }},
      scales: {{
        x: {{ stacked: true, ticks: {{ color: cd.textColor }}, grid: {{ display: false }} }},
        y: {{ stacked: true, ticks: {{ color: cd.textColor, callback: v => (v/1000).toFixed(0)+'K' }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

// Chart 7: GPU/Performance Radar
function buildChart7() {{
  const cd = chartDefaults();
  const modelFilter = document.getElementById('modelFilter').value;
  let datasets = RADAR.datasets;
  if (modelFilter) datasets = datasets.filter(d => d.model === modelFilter);
  if (datasets.length === 0) datasets = RADAR.datasets;
  charts.c7 = new Chart(document.getElementById('chart7'), {{
    type: 'radar',
    data: {{
      labels: RADAR.labels,
      datasets: datasets.map((ds, i) => ({{
        label: ds.model,
        data: ds.data,
        borderColor: RADAR_COLORS[i % RADAR_COLORS.length],
        backgroundColor: RADAR_COLORS[i % RADAR_COLORS.length] + '22',
        pointRadius: 4,
      }}))
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ labels: {{ color: cd.textColor, font: {{ size: 10 }} }} }} }},
      scales: {{
        r: {{
          min: 0, max: 100,
          ticks: {{ color: cd.textColor, backdropColor: 'transparent', stepSize: 20 }},
          grid: {{ color: cd.gridColor }},
          pointLabels: {{ color: cd.textColor, font: {{ size: 10 }} }}
        }}
      }}
    }}
  }});
}}

// Chart 8: AI Trend Line
function buildChart8() {{
  const cd = chartDefaults();
  const slicedDates = AI_TREND.dates.slice(30 - dateRange);
  const slicedVals = AI_TREND.values.slice(30 - dateRange);
  charts.c8 = new Chart(document.getElementById('chart8'), {{
    type: 'line',
    data: {{
      labels: slicedDates,
      datasets: [{{
        label: 'AI 일별 비용',
        data: slicedVals,
        borderColor: '#8b5cf6',
        backgroundColor: '#8b5cf622',
        fill: true,
        tension: 0.3,
        pointRadius: 3,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ labels: {{ color: cd.textColor }} }}, tooltip: {{ callbacks: {{ label: ctx => (ctx.raw/1000).toFixed(1)+'K KRW' }} }} }},
      scales: {{
        x: {{ ticks: {{ color: cd.textColor, maxTicksLimit: 8 }}, grid: {{ color: cd.gridColor }} }},
        y: {{ ticks: {{ color: cd.textColor, callback: v => (v/1000).toFixed(0)+'K' }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

// Chart 9: Unit economics bar
function buildChart9() {{
  const cd = chartDefaults();
  charts.c9 = new Chart(document.getElementById('chart9'), {{
    type: 'bar',
    data: {{
      labels: UNIT_ECON.metrics,
      datasets: [{{
        label: 'Cost/1K Tokens (KRW)',
        data: UNIT_ECON.values,
        backgroundColor: UNIT_ECON.values.map(v => v > 50 ? '#ef4444cc' : v > 5 ? '#f59e0bcc' : '#10b981cc'),
        borderRadius: 4,
      }}]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        x: {{ ticks: {{ color: cd.textColor, font: {{ size: 9 }}, maxRotation: 30 }}, grid: {{ display: false }} }},
        y: {{ ticks: {{ color: cd.textColor }}, grid: {{ color: cd.gridColor }} }}
      }}
    }}
  }});
}}

function rebuildChart1() {{ if (charts.c1) {{ charts.c1.destroy(); }} buildChart1(); }}
function rebuildChart4() {{ if (charts.c4) {{ charts.c4.destroy(); }} buildChart4(); }}
function rebuildChart8() {{ if (charts.c8) {{ charts.c8.destroy(); }} buildChart8(); }}

function rebuildAllCharts() {{
  Object.values(charts).forEach(c => c.destroy());
  charts = {{}};
  buildChart1(); buildChart2(); buildChart3(); buildChart4(); buildChart5();
  buildChart6(); buildChart7(); buildChart8(); buildChart9();
}}

// Tabs
function switchTab(name, btn) {{
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  btn.classList.add('active');
}}

// Init
document.addEventListener('DOMContentLoaded', () => {{
  buildChart1(); buildChart2(); buildChart3(); buildChart4(); buildChart5();
  buildChart6(); buildChart7(); buildChart8(); buildChart9();
}});
</script>
</body>
</html>
"""

with open('out/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize('out/dashboard.html')
print(f'dashboard.html written: {size:,} bytes ({size/1024:.1f} KB)')
print(f'Under 1.2MB: {size < 1_228_800}')
