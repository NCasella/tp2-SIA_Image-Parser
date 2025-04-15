import os
import pandas as pd

folder_path = '../csv'

all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

from collections import defaultdict
grouped = defaultdict(lambda: {'foolish': None, 'pintura': None})

for f in all_files:
    if f.startswith('foolish'):
        grouped[f[7:-4]]['foolish'] = f
    elif f.startswith('pintura'):
        grouped[f[7:-4]]['pintura'] = f

def load_df_safe(filename):
    if not filename:
        return pd.DataFrame(columns=['generation', 'mean_fitness', 'std_fitness', 'best_fitness'])
    df = pd.read_csv(os.path.join(folder_path, filename), sep=';')
    return df

if '50' not in grouped or not grouped['50']['foolish'] or not grouped['50']['pintura']:
    raise ValueError("Missing normalization base: foolish50.csv and pintura50.csv")

base_df1 = load_df_safe(grouped['50']['foolish'])
base_df2 = load_df_safe(grouped['50']['pintura'])

base_merged = pd.merge(base_df1, base_df2, on='generation', how='outer', suffixes=('_foolish', '_pintura'))

base_result = pd.DataFrame()
base_result['generation'] = base_merged['generation']
for col in ['mean_fitness', 'std_fitness', 'best_fitness']:
    base_result[col] = base_merged[[f'{col}_foolish', f'{col}_pintura']].mean(axis=1, skipna=True)

base_result = base_result.sort_values('generation').reset_index(drop=True)

for suffix, files in grouped.items():
    if suffix == '50':
        continue

    df1 = load_df_safe(files['foolish'])
    df2 = load_df_safe(files['pintura'])

    if df1.empty and df2.empty:
        continue  # skip if both are missing

    merged = pd.merge(df1, df2, on='generation', how='outer', suffixes=('_foolish', '_pintura'))

    result = pd.DataFrame()
    result['generation'] = merged['generation']
    for col in ['mean_fitness', 'std_fitness', 'best_fitness']:
        result[col] = merged[[f'{col}_foolish', f'{col}_pintura']].mean(axis=1, skipna=True)

    result = result.sort_values('generation').reset_index(drop=True)

    norm_df = pd.merge(result, base_result, on='generation', suffixes=('', '_base'))
    for col in ['mean_fitness', 'std_fitness', 'best_fitness']:
        norm_df[col] = norm_df[col] / norm_df[f'{col}_base']

    final_df = norm_df[['generation', 'mean_fitness', 'std_fitness', 'best_fitness']]

    out_file = os.path.join(folder_path, f'normalized_{suffix}.csv')
    final_df.to_csv(out_file, sep=';', index=False)
    print(f"Saved: normalized_{suffix}.csv")