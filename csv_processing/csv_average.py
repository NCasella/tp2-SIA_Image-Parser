import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_average_fitness(folder_path, save_plot=True, generation_cap=5000):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        raise ValueError(f"No CSV files found in folder: {folder_path}")

    dfs = []
    for file in csv_files:
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path, sep=';')
        df = df[['generation', 'mean_fitness', 'best_fitness']]
        df = df[df['generation'] <= generation_cap]
        dfs.append(df)

    # Start merge process
    merged = dfs[0].copy()
    merged.rename(columns={'mean_fitness': 'mean_0', 'best_fitness': 'best_0'}, inplace=True)

    for i, df in enumerate(dfs[1:], start=1):
        df = df.rename(columns={
            'mean_fitness': f'mean_{i}',
            'best_fitness': f'best_{i}'
        })
        merged = pd.merge(merged, df, on='generation', how='outer')

    mean_cols = [col for col in merged.columns if col.startswith('mean_')]
    best_cols = [col for col in merged.columns if col.startswith('best_')]

    avg_df = pd.DataFrame()
    avg_df['generation'] = merged['generation']
    avg_df['mean_fitness'] = merged[mean_cols].mean(axis=1, skipna=True)
    avg_df['best_fitness'] = merged[best_cols].mean(axis=1, skipna=True)
    avg_df = avg_df.sort_values('generation').reset_index(drop=True)

    folder_name = os.path.basename(os.path.normpath(folder_path))
    plt.figure(figsize=(12, 6))
    plt.plot(avg_df['generation'], avg_df['mean_fitness'], label='Mean Fitness', alpha=0.7)
    plt.plot(avg_df['generation'], avg_df['best_fitness'], label='Best Fitness', alpha=0.7)

    plt.title(f'Average Fitness over Generations - {folder_name} (up to {generation_cap})')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_plot:
        output_file = os.path.join(folder_path, f'{folder_name}_average_plot_capped_{generation_cap}.png')
        plt.savefig(output_file)
        print(f"Saved plot to: {output_file}")

plot_average_fitness("../uniform_real", True, 5000)