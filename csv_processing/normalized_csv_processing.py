import os
import pandas as pd
import matplotlib.pyplot as plt

normalized_folder = '../normalized_csv'  # Adjust if needed

csv_files = [f for f in os.listdir(normalized_folder)
             if f.startswith('normalized_') and f.endswith('.csv')]

for file in csv_files:
    filepath = os.path.join(normalized_folder, file)
    df = pd.read_csv(filepath, sep=';')

    if df.empty or 'generation' not in df.columns:
        print(f"Skipped empty or invalid file: {file}")
        continue

    df = df.sort_values(by='generation')

    plt.figure(figsize=(12, 6))
    plt.plot(df['generation'], df['mean_fitness'], label='Mean Fitness', alpha=0.7)
    plt.plot(df['generation'], df['best_fitness'], label='Best Fitness', alpha=0.7)

    plt.title(f'Normalized Fitness over Generations\n{file}', fontsize=14)
    plt.xlabel('Generation')
    plt.ylabel('Normalized Fitness')
    plt.legend()
    plt.grid(True)

    max_gen = int(df['generation'].max())
    if max_gen > 1000:
        step = max_gen // 10
        plt.xticks(ticks=range(0, max_gen + 1, step))

    plt.tight_layout()

    plot_path = os.path.join(normalized_folder, file.replace('.csv', '_plot.png'))
    plt.savefig(plot_path)
    plt.close()

    print(f"Saved plot: {plot_path}")