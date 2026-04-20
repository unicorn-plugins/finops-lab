import pandas as pd
import json
import csv
from pathlib import Path
from collections import defaultdict

# 1. 데이터 로드
csv_path = 'out/focus-normalized.csv'
df = pd.read_csv(csv_path)

print("=== 태그 커버리지 분석 시작 ===")
print(f"총 행 수: {len(df)}")

# 2. Tags 컬럼 파싱
def parse_tags(tag_str):
    """JSON 형식의 Tags 문자열 파싱"""
    if pd.isna(tag_str) or tag_str == '':
        return {}
    try:
        return json.loads(tag_str)
    except:
        return {}

df['tags_dict'] = df['Tags'].apply(parse_tags)

# 3. CSP별 분류
csp_map = {
    'Amazon Web Services': 'AWS',
    'Microsoft': 'Azure',
    'Google': 'GCP',
}
df['CSP'] = df['ServiceProviderName'].map(csp_map).fillna('Other')

# 4. AI 서비스 식별
ai_keywords = ['Bedrock', 'OpenAI', 'Vertex', 'Anthropic', 'Claude', 'GPT', 'Model']
df['is_ai'] = df['ServiceName'].fillna('').apply(
    lambda x: any(kw.lower() in str(x).lower() for kw in ai_keywords)
)

# 5. 필수 태그 추출
required_tags = ['Project', 'Environment', 'Owner', 'CostCenter']
for tag in required_tags:
    df[f'has_{tag}'] = df['tags_dict'].apply(lambda x: tag in x)

# 6. 미태깅 리소스 목록
df['missing_tags'] = df[[f'has_{t}' for t in required_tags]].apply(
    lambda row: ', '.join([t for i, t in enumerate(required_tags) if not row.iloc[i]]), axis=1
)

# 7. 커버리지 계산
print("\n=== 필수 4종 태그 커버리지 ===\n")
coverage_data = []

for csp in ['AWS', 'Azure', 'GCP', 'Other']:
    csp_df = df[df['CSP'] == csp]
    if len(csp_df) == 0:
        continue
    
    stats = {
        'CSP': csp,
        'Total': len(csp_df),
        'Project': csp_df['has_Project'].sum(),
        'Environment': csp_df['has_Environment'].sum(),
        'Owner': csp_df['has_Owner'].sum(),
        'CostCenter': csp_df['has_CostCenter'].sum(),
    }
    coverage_data.append(stats)
    
    print(f"{csp} (총 {stats['Total']} 행):")
    print(f"  Project:    {stats['Project']:4d} / {stats['Total']:4d} ({100*stats['Project']/stats['Total']:6.2f}%)")
    print(f"  Environment:{stats['Environment']:4d} / {stats['Total']:4d} ({100*stats['Environment']/stats['Total']:6.2f}%)")
    print(f"  Owner:      {stats['Owner']:4d} / {stats['Total']:4d} ({100*stats['Owner']/stats['Total']:6.2f}%)")
    print(f"  CostCenter: {stats['CostCenter']:4d} / {stats['Total']:4d} ({100*stats['CostCenter']/stats['Total']:6.2f}%)")
    print()

# 8. 전체 커버리지
print("=== 전체 커버리지 ===\n")
total = len(df)
for tag in required_tags:
    count = df[f'has_{tag}'].sum()
    pct = 100 * count / total
    print(f"{tag:12s}: {count:4d} / {total:4d} ({pct:6.2f}%)")

# 9. 미태깅 리소스 Top 20 (비용 순)
print("\n=== 미태깅 리소스 Top 20 (비용 순) ===\n")

untagged = df[df['missing_tags'] != ''][
    ['ResourceId', 'ServiceProviderName', 'ServiceName', 'missing_tags', 'AmortizedCost_KRW']
].drop_duplicates('ResourceId').sort_values('AmortizedCost_KRW', ascending=False).head(20)

for idx, row in untagged.iterrows():
    rid = str(row['ResourceId']) if pd.notna(row['ResourceId']) else 'N/A'
    spn = str(row['ServiceProviderName']) if pd.notna(row['ServiceProviderName']) else 'N/A'
    sn = str(row['ServiceName']) if pd.notna(row['ServiceName']) else 'N/A'
    print(f"{rid[:40]:40s} | {spn:15s} | {sn:20s}")
    print(f"  누락: {row['missing_tags']} | 비용: {row['AmortizedCost_KRW']:,.0f} KRW")
    print()

# 10. AI 특화 태그
print("=== AI 특화 태그 현황 ===\n")
ai_df = df[df['is_ai']]
if len(ai_df) > 0:
    ai_unique = ai_df.drop_duplicates('ResourceId')
    print(f"AI 리소스 총 수: {len(ai_unique)}")
    print(f"AI 리소스 비용: {ai_df['AmortizedCost_KRW'].sum():,.0f} KRW")
    print(f"\n추가 태그 필요:")
    print(f"  - LLMApiKey:    AI 관련 리소스 중 API Key 태그 필요")
    print(f"  - ModelName:    사용 모델명 (예: gpt-4o, claude-3-5-sonnet) 태그 필요")
    print(f"  - ChargebackUnit: chargeback 단위(팀/프로젝트/BU) 태그 필요")
else:
    print("AI 리소스 없음")

# 11. 비용 기반 미태깅 분석
print("\n=== 미태깅 비용 규모 ===\n")
for tag in required_tags:
    missing = df[~df[f'has_{tag}']]
    cost = missing['AmortizedCost_KRW'].sum()
    total_cost = df['AmortizedCost_KRW'].sum()
    pct = 100 * cost / total_cost if total_cost > 0 else 0
    print(f"{tag:12s} 미태깅 비용: {cost:12,.0f} KRW ({pct:6.2f}%)")

