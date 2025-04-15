import pandas as pd
import matplotlib.pyplot as plt

def normalize_and_plot(hm_path, normal_path, label):
    # Load CSVs
    hm_df = pd.read_csv(hm_path, sep=';')
    norm_df = pd.read_csv(normal_path, sep=';')

    # Merge on generation
    merged = pd.merge(hm_df, norm_df, on='generation', suffixes=('_hm', '_norm'), how='inner')

    # Normalize
    merged['mean_fitness'] = merged['mean_fitness_hm'] / merged['mean_fitness_norm']
    merged['best_fitness'] = merged['best_fitness_hm'] / merged['best_fitness_norm']

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(merged['generation'], merged['mean_fitness'], label=f'{label} - Mean Fitness', alpha=0.7)
    plt.plot(merged['generation'], merged['best_fitness'], label=f'{label} - Best Fitness', alpha=0.7)

    plt.title(f'Normalized Fitness: {label}')
    plt.xlabel('Generation')
    plt.ylabel('Normalized Fitness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save
    plot_file = f'normalized_{label}.png'
    plt.savefig(plot_file)
    print(f"Saved plot: {plot_file}")
    plt.close()

# Usage
normalize_and_plot('../csv/foolishHMDelta.csv', '../csv/foolishDeltaNormal.csv', 'HMDelta')
normalize_and_plot('../csv/foolishHMNew.csv', '../csv/foolishNewNormal.csv', 'HMNew')