import binary_puzzle as bp
from greedy_ai import GreedyBoard
from expectimax_ai import ExpectimaxBoard
from mcts_ai import MCTSBoard
import heuristics
import numpy as np
import json
from datetime import datetime
import os

def run_game(ai_board):
    while not ai_board.board.is_game_over():
        ai_board.take_best_move()
    return {
        'score': ai_board.board.score(),
        'moves': ai_board.board.total_moves,
        'board': ai_board.board.get_2048_board().tolist()
    }

def run_experiments(iterations=100):
    results = {
        'greedy_score': [],
        'greedy_open': [],
        'expectimax_score': [],
        'expectimax_open': [],
        'mcts': []
    }

    for i in range(iterations):
        print(f"Running iteration {i+1}/{iterations}")

        # Greedy with score heuristic
        print("Starting Greedy with score heuristic")
        board = bp.Board()
        greedy = GreedyBoard(board, heuristics.score_heuristic)
        results['greedy_score'].append(run_game(greedy))

        # Greedy with open cells heuristic
        print("Starting Greedy with open cells heuristic")
        board = bp.Board()
        greedy = GreedyBoard(board, heuristics.open_cells_heuristic)
        results['greedy_open'].append(run_game(greedy))

        # Expectimax with score heuristic
        print("Starting Expectimax with score heuristic")
        board = bp.Board()
        expectimax = ExpectimaxBoard(board, depth=3, heuristic=heuristics.score_heuristic)
        results['expectimax_score'].append(run_game(expectimax))

        # Expectimax with open cells heuristic
        print("Starting Expectimax with open cells heuristic")
        board = bp.Board()
        expectimax = ExpectimaxBoard(board, depth=3, heuristic=heuristics.open_cells_heuristic)
        results['expectimax_open'].append(run_game(expectimax))

        # MCTS with tile sum heuristic
        print("Starting MCTS with tile sum heuristic")
        board = bp.Board()
        mcts = MCTSBoard(board, simulation_time=0.1, heuristic=heuristics.tile_sum_heuristic, exploration=0.1)
        results['mcts'].append(run_game(mcts))

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists('results'):
        os.makedirs('results')
    
    filename = f'results/analysis_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(results, f)

    print(f"Results saved to {filename}")
    
    # Print summary statistics
    for method, games in results.items():
        scores = [game['score'] for game in games]
        moves = [game['moves'] for game in games]
        print(f"\n{method} summary:")
        print(f"Average score: {np.mean(scores):.2f} ± {np.std(scores):.2f}")
        print(f"Average moves: {np.mean(moves):.2f} ± {np.std(moves):.2f}")
        print(f"Max score: {np.max(scores)}")
        print(f"Min score: {np.min(scores)}")

if __name__ == '__main__':
    run_experiments(100)
