import binary_puzzle as bp
import numpy as np
from visual import GameVisual
import time
import heuristics

class ExpectimaxBoard:
    def __init__(self, board: bp.Board, depth: int = 3, heuristic: callable = None):
        self.board = board
        self.depth = depth
        if heuristic is None:
            self.heuristic = heuristics.score_heuristic
        else:
            self.heuristic = heuristic

    def expectimax(self, board: bp.Board, depth: int, is_max: bool) -> tuple[float, str]:
        if depth == 0 or board.is_game_over():
            return self.heuristic(board), None

        if is_max:
            # Player's turn - try all possible moves
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                # This should never happen, but just in case
                raise ValueError("No valid moves")
                    
            max_value = float('-inf')
            best_move = valid_moves[0]
            
            for move in valid_moves:
                new_board = board.copy()
                new_board.swipe(move)
                value, _ = self.expectimax(new_board, depth - 1, False)
                if value > max_value:
                    max_value = value
                    best_move = move
            
            return max_value, best_move
        
        else:
            # Chance node - get the expected value for all possible tile 
            # placements and return the average
            open_cells = board.get_open_cells()
            total_value = 0
            if len(open_cells) == 0:
                # This should never happen, but just in case
                raise ValueError("No open cells")
            
            # 2 and 4 are the possible values for a new tile
            for cell in open_cells:
                # 90% chance of getting a 2, 10% chance of getting a 4
                for tile in [(2, 0.9), (4, 0.1)]:
                    new_board = board.copy()
                    new_board.place_tile(cell, tile[0])
                    value, _ = self.expectimax(new_board, depth - 1, True)
                    total_value += value * tile[1]

            return total_value / len(open_cells), None

    def get_best_move(self) -> str:
        _, best_move = self.expectimax(self.board, self.depth, True)
        return best_move
    
    def take_best_move(self) -> bool:
        move = self.get_best_move()
        if move is None:
            return False
        # print(f"Taking move {move}")
        self.board.move(move)
        return True

    def __str__(self):
        return str(self.board)
    

class VisualEB(GameVisual):
    def __init__(self, expectimax_board: ExpectimaxBoard, delay=1000):
        super().__init__()
        self.board = expectimax_board.board
        self.expectimax_board = expectimax_board
        self.delay = delay
        self.update_grid_cells()
        self.after(self.delay, self.ai_move)
        self.mainloop()

    def ai_move(self):
        if self.expectimax_board.take_best_move():
            self.update_grid_cells()
            if self.board.is_game_over():
                self.show_game_over()
            else:
                self.after(self.delay, self.ai_move)

if __name__ == '__main__':
    # Test with score heuristic
    board = bp.Board()
    expectimax_board = ExpectimaxBoard(board, depth=5, heuristic=heuristics.score_heuristic)
    visual = VisualEB(expectimax_board, delay=10)

    # Test with open cells heuristic
    board = bp.Board()
    expectimax_board = ExpectimaxBoard(board, depth=3, heuristic=heuristics.open_cells_heuristic)
    visual = VisualEB(expectimax_board, delay=10)

    # Test with max tile heuristic
    board = bp.Board()
    expectimax_board = ExpectimaxBoard(board, depth=3, heuristic=heuristics.max_tile_heuristic)
    visual = VisualEB(expectimax_board, delay=10)

    # Test with tile sum heuristic
    board = bp.Board()
    expectimax_board = ExpectimaxBoard(board, depth=3, heuristic=heuristics.tile_sum_heuristic)
    visual = VisualEB(expectimax_board, delay=10)

    # Test with tile sum game over heuristic
    board = bp.Board()
    expectimax_board = ExpectimaxBoard(board, depth=3, heuristic=heuristics.tile_sum_and_gamover_heuristic)
    visual = VisualEB(expectimax_board, delay=10)
