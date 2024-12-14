import binary_puzzle as bp
import numpy as np
from visual import GameVisual
import time
import heuristics

class GreedyBoard():
    def __init__(self, board: bp.Board, heuristic: callable):
        self.board = board
        if heuristic is None:
            self.heuristic = heuristics.score_heuristic
        else:
            self.heuristic = heuristic

    def get_best_move(self) -> str:
        valid_moves = self.board.get_valid_moves()
        best_move = None
        best_h = None
        for move in valid_moves:
            new_board = self.board.copy()
            new_board.swipe(move)
            h = self.heuristic(new_board)
            if best_h is None or h > best_h:
                best_h = h
                best_move = move

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
    

class VisualGB(GameVisual):
    def __init__(self, greedy_board: GreedyBoard, delay=1000):
        super().__init__()
        self.board = greedy_board.board
        self.greedy_board = greedy_board
        self.delay = delay
        self.update_grid_cells()
        self.after(self.delay, self.ai_move)
        self.mainloop()

    def ai_move(self):
        if self.greedy_board.take_best_move():
            self.update_grid_cells()
            if self.board.is_game_over():
                self.show_game_over()
            else:
                self.after(self.delay, self.ai_move)

if __name__ == '__main__':
    board = bp.Board()
    greedy_board = GreedyBoard(board, heuristics.score_heuristic)
    visual = VisualGB(greedy_board, delay=100)

    board = bp.Board()
    greedy_board = GreedyBoard(board, heuristics.open_cells_heuristic)
    visual = VisualGB(greedy_board, delay=100)

