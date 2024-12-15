import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_results():
    # Load all JSON result files from the 'results' directory
    results = {}
    for filename in os.listdir('results'):
        if filename.endswith('.json'):
            algorithm = filename.split('_')[0]
            filepath = os.path.join('results', filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                results[algorithm] = data
    return results

def compute_statistics(results):
    stats = {}
    for algorithm, variants in results.items():
        stats[algorithm] = {}
        for variant, games in variants.items():
            scores = [game['score'] for game in games]
            moves = [game['moves'] for game in games]
            times = [game['time'] for game in games]
            max_tiles = [np.max(game['board']) for game in games]
            stats[algorithm][variant] = {
                'scores': scores,
                'moves': moves,
                'times': times,
                'max_tiles': max_tiles,
                'avg_score': np.mean(scores),
                'median_score': np.median(scores),
                'max_score': np.max(scores),
                'avg_moves': np.mean(moves),
                'avg_time_per_move': np.mean(times) / np.mean(moves),
                'avg_time_per_game': np.mean(times),
                'tile_counts': {}
            }
            for tile in [512, 1024, 2048, 4096]:
                count = sum(1 for mt in max_tiles if mt >= tile)
                stats[algorithm][variant]['tile_counts'][tile] = count / len(games)
    return stats

def plot_scores(stats):
    # Plot average and median scores for each algorithm variant
    for algorithm, variants in stats.items():
        variants_list = list(variants.keys())
        avg_scores = [variants[variant]['avg_score'] for variant in variants_list]
        median_scores = [variants[variant]['median_score'] for variant in variants_list]

        x = np.arange(len(variants_list))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x - width/2, avg_scores, width, label='Average Score')
        plt.bar(x + width/2, median_scores, width, label='Median Score')

        plt.ylabel('Scores')
        plt.title(f'Scores by Variant for {algorithm.capitalize()}')
        plt.xticks(x, variants_list, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'figures/{algorithm}_scores.png')
        plt.close()

def plot_max_tiles(stats):
    # Plot achievement rates of key tiles for each algorithm variant
    key_tiles = [512, 1024, 2048, 4096]
    for algorithm, variants in stats.items():
        variants_list = list(variants.keys())
        x = np.arange(len(variants_list))
        width = 0.2

        plt.figure(figsize=(10, 6))
        for i, tile in enumerate(key_tiles):
            achievement_rates = [variants[variant]['tile_counts'][tile]*100 for variant in variants_list]
            plt.bar(x + (i - 1.5)*width, achievement_rates, width, label=f'Tile {tile}')

        plt.ylabel('Achievement Rate (%)')
        plt.title(f'Key Tile Achievement Rates for {algorithm.capitalize()}')
        plt.xticks(x, variants_list, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'figures/{algorithm}_tile_achievements.png')
        plt.close()

def plot_time_per_move(stats):
    # Plot average time per move for each algorithm variant
    for algorithm, variants in stats.items():
        variants_list = list(variants.keys())
        times_per_move = [variants[variant]['avg_time_per_move'] for variant in variants_list]

        x = np.arange(len(variants_list))

        plt.figure(figsize=(10, 6))
        plt.bar(x, times_per_move)
        plt.ylabel('Time per Move (s)')
        plt.title(f'Average Time per Move for {algorithm.capitalize()}')
        plt.xticks(x, variants_list, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'figures/{algorithm}_time_per_move.png')
        plt.close()

def plot_time_per_game(stats):
    # Plot average time per game for each algorithm variant
    for algorithm, variants in stats.items():
        variants_list = list(variants.keys())
        times_per_game = [variants[variant]['avg_time_per_game'] for variant in variants_list]

        x = np.arange(len(variants_list))

        plt.figure(figsize=(10, 6))
        plt.bar(x, times_per_game)
        plt.ylabel('Time per Game (s)')
        plt.title(f'Average Time per Game for {algorithm.capitalize()}')
        plt.xticks(x, variants_list, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'figures/{algorithm}_time_per_game.png')
        plt.close()

def create_tile_achievement_table(stats):
    # Create tables showing the rate of achieving key tile values
    key_tiles = [512, 1024, 2048, 4096]
    for algorithm, variants in stats.items():
        data = []
        index = []
        for variant, info in variants.items():
            row = [info['tile_counts'][tile]*100 for tile in key_tiles]
            data.append(row)
            index.append(variant)
        df = pd.DataFrame(data, columns=[f'Tile {tile}' for tile in key_tiles], index=index)
        df.index.name = 'Variant'
        df.to_csv(f'figures/{algorithm}_tile_achievement_rates.csv')

def plot_combined_scores(stats):
    # Plot average scores for all algorithm variants in one graph
    variants_list = []
    avg_scores = []
    median_scores = []
    for algorithm, variants in stats.items():
        for variant, data in variants.items():
            variants_list.append(f"{algorithm}_{variant}")
            avg_scores.append(data['avg_score'])
            median_scores.append(data['median_score'])
    
    width = 0.35
    x = np.arange(len(variants_list))
    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, avg_scores, width, label='Average Score', color='skyblue')
    plt.bar(x + width/2, median_scores, width, label='Median Score', color='lightgreen')
    plt.ylabel('Scores')
    plt.title('Average and Median Scores Across All Algorithm Variants')
    plt.xticks(x, variants_list, rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/combined_avg_median_scores.png')
    plt.close()

def plot_combined_max_tiles(stats):
    # Plot key tile achievement rates for all algorithm variants in one graph
    key_tiles = [512, 1024, 2048, 4096]
    variants_list = []
    tile_rates = {tile: [] for tile in key_tiles}
    for algorithm, variants in stats.items():
        for variant, data in variants.items():
            variants_list.append(f"{algorithm}_{variant}")
            for tile in key_tiles:
                tile_rates[tile].append(data['tile_counts'][tile] * 100)
    
    x = np.arange(len(variants_list))
    width = 0.2
    plt.figure(figsize=(12, 6))
    for i, tile in enumerate(key_tiles):
        plt.bar(x + (i - 1.5)*width, tile_rates[tile], width, label=f'Tile {tile}')
    plt.ylabel('Achievement Rate (%)')
    plt.title('Key Tile Achievement Rates Across All Algorithm Variants')
    plt.xticks(x, variants_list, rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/combined_tile_achievements.png')
    plt.close()

def plot_combined_time_per_move(stats):
    # Plot average time per move for all algorithm variants in one graph
    variants_list = []
    times_per_move = []
    for algorithm, variants in stats.items():
        for variant, data in variants.items():
            variants_list.append(f"{algorithm}_{variant}")
            times_per_move.append(data['avg_time_per_move'])
    
    x = np.arange(len(variants_list))
    plt.figure(figsize=(12, 6))
    plt.bar(x, times_per_move, color='orange')
    plt.ylabel('Time per Move (s)')
    plt.title('Average Time per Move Across All Algorithm Variants')
    plt.xticks(x, variants_list, rotation=90)
    plt.tight_layout()
    plt.savefig('figures/combined_time_per_move.png')
    plt.close()

def plot_combined_time_per_game(stats):
    # Plot average time per game for all algorithm variants in one graph
    variants_list = []
    times_per_game = []
    for algorithm, variants in stats.items():
        for variant, data in variants.items():
            variants_list.append(f"{algorithm}_{variant}")
            times_per_game.append(data['avg_time_per_game'])
    
    x = np.arange(len(variants_list))
    plt.figure(figsize=(12, 6))
    plt.bar(x, times_per_game, color='green')
    plt.ylabel('Time per Game (s)')
    plt.title('Average Time per Game Across All Algorithm Variants')
    plt.xticks(x, variants_list, rotation=90)
    plt.tight_layout()
    plt.savefig('figures/combined_time_per_game.png')
    plt.close()

def main():
    results = load_results()
    stats = compute_statistics(results)
    if not os.path.exists('figures'):
        os.makedirs('figures')
    plot_scores(stats)
    plot_max_tiles(stats)
    plot_time_per_move(stats)
    plot_time_per_game(stats)
    create_tile_achievement_table(stats)
    plot_combined_scores(stats)
    plot_combined_max_tiles(stats)
    plot_combined_time_per_move(stats)
    plot_combined_time_per_game(stats)

if __name__ == '__main__':
    main()
