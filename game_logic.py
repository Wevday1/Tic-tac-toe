from typing import List

class TicTacToeLogic:
    def __init__(self) -> None:

        """
        Initialize the Tic Tac Toe game logic.
        """
        self.current_player: str = "X"
        self.scores = {"X": 0, "O": 0, "Draws": 0}

    def switch_player(self) -> None:

        """
        Switch the current player from X to O or from O to X.
        """
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, board: List[List[str]]) -> bool:

        """
        Check if there is a winner on the given board state.
        """
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != "":
                return True

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return True

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return True
        if board[0][2] == board[1][1] == board[2][0] != "":
            return True

        return False

    def check_draw(self, board: List[List[str]]) -> bool:

        """
        Check if the given board state is a draw (no empty cells and no winners).
        """
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    return False
        return True

    def increment_win_counter(self) -> None:

        """
        Increment the win counter for the current player.
        """
        self.scores[self.current_player] += 1

    def increment_draw_count(self) -> None:

        """
        Increment the draw count.
        """
        self.scores["Draws"] += 1

    def reset_game(self) -> None:

        """
        Reset the game state to its initial conditions.
        """
        self.current_player = "X"