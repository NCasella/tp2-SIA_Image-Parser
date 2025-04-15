import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = '../csv/'

csv_files = [f for f in os.listdir(folder_path) if
             f.endswith('.csv') and (f.startswith('foolish') or f.startswith('pintura'))]

for file in csv_files:
    filepath = os.path.join(folder_path, file)

    df = pd.read_csv(filepath, sep=';')

    plt.figure(figsize=(12, 6))
    plt.plot(df['generation'], df['mean_fitness'], label='Mean Fitness', alpha=0.7)
    plt.plot(df['generation'], df['best_fitness'], label='Best Fitness', alpha=0.7)

    plt.title(f'Fitness over Generations - {file}')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)

    if df['generation'].max() > 1000:
        plt.xticks(ticks=range(0, df['generation'].max(), int(df['generation'].max() / 10)))

    plt.tight_layout()

    output_file = os.path.join(folder_path, f'{file}_plot.png')
    plt.savefig(output_file)
    plt.close()
