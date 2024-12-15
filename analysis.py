import binary_puzzle as bp
from greedy_ai import GreedyBoard
from expectimax_ai import ExpectimaxBoard
from mcts_ai import MCTSBoard
import heuristics
import numpy as np
import json
from datetime import datetime
import os
import time
import multiprocessing

def run_game(ai_board, algorithm, params):
    print(f"\nStarting {algorithm} game with parameters:", end=" ")
    if algorithm == "greedy":
        print(f"heuristic={params['heuristic_name']}")
    elif algorithm == "expectimax":
        print(f"depth={params['depth']}, heuristic={params['heuristic_name']}")
    elif algorithm == "mcts":
        print(f"simulation_time={params['sim_time']:.1f}, exploration={params['exploration']}")
        
    start_time = time.time()
    while not ai_board.board.is_game_over():
        ai_board.take_best_move()
    end_time = time.time()
    
    # Convert board to regular Python list and ensure all numbers are standard Python integers
    board_data = [[int(cell) for cell in row] for row in ai_board.board.get_2048_board().tolist()]
    
    return {
        'score': int(ai_board.board.score()),  # Convert NumPy integers to Python integers
        'moves': int(ai_board.board.total_moves),
        'board': board_data,
        'time': float(end_time - start_time)
    }

def run_game_wrapper(args):
    # Initialize Board's merge_array for this process
    if bp.Board.merge_array is None:
        bp.Board._initialize_merge_array()
    
    algorithm, original_params = args
    # Make a copy of params to avoid modifying the original
    params = original_params.copy()
    
    ai_board_class = params.pop('ai_board_class')
    
    # Store parameters needed for printing before removing them
    print_params = {
        'heuristic_name': params.get('heuristic_name'),
        'depth': params.get('depth'),
        'sim_time': params.get('sim_time'),
        'exploration': params.get('exploration')
    }
    
    # Remove non-constructor parameters
    params.pop('heuristic_name', None)
    params.pop('sim_time', None)
    
    ai_board = ai_board_class(**params)
    result = run_game(ai_board, algorithm, print_params)
    return (algorithm, original_params, result)  # Return original_params instead of modified params

def save_results(algorithm, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('results'):
        os.makedirs('results')
    
    filename = f'results/{algorithm}_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(results, f)
    print(f"\nSaved {algorithm} results to {filename}")
    
    # Print summary statistics
    print(f"\n{algorithm.upper()} Summary:")
    for variant, games in results.items():
        scores = [game['score'] for game in games]
        moves = [game['moves'] for game in games]
        times = [game['time'] for game in games]
        print(f"\n{variant}:")
        print(f"Average score: {float(np.mean(scores)):.2f} ± {float(np.std(scores)):.2f}")
        print(f"Average moves: {float(np.mean(moves)):.2f} ± {float(np.std(moves)):.2f}")
        print(f"Average time: {float(np.mean(times)):.2f}s ± {float(np.std(times)):.2f}s")
        print(f"Max score: {int(np.max(scores))}")
        print(f"Min score: {int(np.min(scores))}")
        print(f"Total time: {float(sum(times)):.2f}s")

def run_experiments(iterations=10):
    tasks = []
    # Prepare tasks for Greedy
    for i in range(iterations):
        tasks.append((
            'greedy',
            {
                'ai_board_class': GreedyBoard,
                'board': bp.Board(),
                'heuristic': heuristics.score_heuristic,
                'heuristic_name': 'score_heuristic'
            }
        ))
        tasks.append((
            'greedy',
            {
                'ai_board_class': GreedyBoard,
                'board': bp.Board(),
                'heuristic': heuristics.open_cells_heuristic,
                'heuristic_name': 'open_cells_heuristic'
            }
        ))
    # Prepare tasks for Expectimax
    for depth in range(1, 6):  # Changed from range(1, 5)
        for i in range(iterations):
            tasks.append((
                'expectimax',
                {
                    'ai_board_class': ExpectimaxBoard,
                    'board': bp.Board(),
                    'depth': depth,
                    'heuristic': heuristics.score_heuristic,
                    'heuristic_name': 'score_heuristic'
                }
            ))
            tasks.append((
                'expectimax',
                {
                    'ai_board_class': ExpectimaxBoard,
                    'board': bp.Board(),
                    'depth': depth,
                    'heuristic': heuristics.open_cells_heuristic,
                    'heuristic_name': 'open_cells_heuristic'
                }
            ))
    # Prepare tasks for MCTS
    sim_times = np.arange(0.1, 0.6, 0.1)
    for sim_time in sim_times:
        for i in range(iterations):
            tasks.append((
                'mcts',
                {
                    'ai_board_class': MCTSBoard,
                    'board': bp.Board(),
                    'simulation_time': sim_time,
                    'heuristic': heuristics.tile_sum_heuristic,
                    'exploration': 0.1,
                    'sim_time': sim_time
                }
            ))
    # Run tasks using a multiprocessing Pool
    with multiprocessing.Pool(processes=8) as pool:
        results = pool.map(run_game_wrapper, tasks)
    # Organize and save results
    greedy_results = {'score_heuristic': [], 'open_cells_heuristic': []}
    expectimax_results = {
        f"depth_{depth}_{heur}": [] 
        for depth in range(1, 6)  # Changed from range(1, 5)
        for heur in ['score_heuristic', 'open_cells_heuristic']
    }
    mcts_results = {f"sim_time_{sim_time:.1f}": [] for sim_time in sim_times}
    for algorithm, params, result in results:
        if algorithm == 'greedy':
            key = params['heuristic_name']
            greedy_results[key].append(result)
        elif algorithm == 'expectimax':
            key = f"depth_{params['depth']}_{params['heuristic_name']}"
            expectimax_results[key].append(result)
        elif algorithm == 'mcts':
            key = f"sim_time_{params['sim_time']:.1f}"
            mcts_results[key].append(result)
    save_results('greedy', greedy_results)
    save_results('expectimax', expectimax_results)
    save_results('mcts', mcts_results)

if __name__ == '__main__':
    run_experiments(100)
