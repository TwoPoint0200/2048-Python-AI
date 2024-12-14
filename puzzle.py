import constants as c
import binary_puzzle as bp
from visual import GameVisual

class GameGrid(GameVisual):
    def __init__(self):
        super().__init__()
        self.master.bind("<Key>", self.key_down)
        self.board = bp.Board()

        self.commands = {
            c.KEY_UP: lambda: self.board.move("up"),
            c.KEY_DOWN: lambda: self.board.move("down"),
            c.KEY_LEFT: lambda: self.board.move("left"),
            c.KEY_RIGHT: lambda: self.board.move("right"),
            c.KEY_UP_ALT1: lambda: self.board.move("up"),
            c.KEY_DOWN_ALT1: lambda: self.board.move("down"),
            c.KEY_LEFT_ALT1: lambda: self.board.move("left"),
            c.KEY_RIGHT_ALT1: lambda: self.board.move("right"),
            c.KEY_UP_ALT2: lambda: self.board.move("up"),
            c.KEY_DOWN_ALT2: lambda: self.board.move("down"),
            c.KEY_LEFT_ALT2: lambda: self.board.move("left"),
            c.KEY_RIGHT_ALT2: lambda: self.board.move("right"),
        }

        self.check_valid_moves = {
            c.KEY_UP: lambda: self.board.can_swipe_up(),
            c.KEY_DOWN: lambda: self.board.can_swipe_down(),
            c.KEY_LEFT: lambda: self.board.can_swipe_left(),
            c.KEY_RIGHT: lambda: self.board.can_swipe_right(),
            c.KEY_UP_ALT1: lambda: self.board.can_swipe_up(),
            c.KEY_DOWN_ALT1: lambda: self.board.can_swipe_down(),
            c.KEY_LEFT_ALT1: lambda: self.board.can_swipe_left(),
            c.KEY_RIGHT_ALT1: lambda: self.board.can_swipe_right(),
            c.KEY_UP_ALT2: lambda: self.board.can_swipe_up(),
            c.KEY_DOWN_ALT2: lambda: self.board.can_swipe_down(),
            c.KEY_LEFT_ALT2: lambda: self.board.can_swipe_left(),
            c.KEY_RIGHT_ALT2: lambda: self.board.can_swipe_right(),
        }

        self.update_grid_cells()
        self.mainloop()

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT: exit()
        if key in self.commands:
            if self.check_valid_moves[key]():
                self.commands[key]()
                self.update_grid_cells()
                if self.board.is_game_over():
                    self.show_game_over()

game_grid = GameGrid()