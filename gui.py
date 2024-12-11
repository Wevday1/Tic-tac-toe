import random
from tkinter import Tk, Button, Label, Radiobutton, StringVar, messagebox, N, S, E, W
from typing import List
from game_logic import TicTacToeLogic

class TicTacToeGUI:
    def __init__(self, master: Tk, game_logic: TicTacToeLogic) -> None:

        """
        Initialize the Tic Tac Toe GUI interface.
        """
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.resizable(False, False)

        self.game_logic = game_logic
        self.game_mode = "Multiplayer"  # Default game mode
        self.player_role = StringVar(value="X")  # Default player role in single-player mode
        self.ai_turn = False        # Track if it's the AI's turn
        self.game_over = False      # Flag to indicate game over
        self.ai_move_counter = 0    # Track the number of AI moves

        self.buttons: List[List[Button]] = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self) -> None:

        """
        Create and arrange all widgets for the GUI setup.
        """
        # Turn Indicator
        self.turn_label = Label(self.master, text=self.get_turn_text(), font=('Arial', 16, 'bold'))
        self.turn_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Game Buttons
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = Button(
                    self.master,
                    text="",
                    font=('Arial', 24),
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.handle_click(r, c)
                )
                self.buttons[row][col].grid(row=row + 1, column=col, padx=0, pady=0, sticky=N + S + E + W)

        # Score Display
        self.score_label = Label(
            self.master,
            text=self.get_score_text(),
            font=('Arial', 14)
        )
        self.score_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Game Mode Buttons
        self.mode_label = Label(self.master, text="Game Mode:", font=('Arial', 12))
        self.mode_label.grid(row=5, column=0, pady=5)
        self.single_player_button = Button(
            self.master,
            text="Single Player",
            font=('Arial', 12),
            command=self.set_single_player
        )
        self.single_player_button.grid(row=5, column=1)
        self.multiplayer_button = Button(
            self.master,
            text="Multiplayer",
            font=('Arial', 12),
            command=self.set_multiplayer,
            bg="lightblue"
        )
        self.multiplayer_button.grid(row=5, column=2)

        # Role Selection for Single Player
        self.role_label = Label(self.master, text="Choose your role:", font=('Arial', 12))
        self.role_label.grid(row=6, column=0, pady=5)
        self.role_x_button = Radiobutton(
            self.master,
            text="Play as X (First)",
            font=('Arial', 12),
            variable=self.player_role,
            value="X",
            command=self.set_role_x
        )
        self.role_x_button.grid(row=6, column=1)
        self.role_o_button = Radiobutton(
            self.master,
            text="Play as O (Second)",
            font=('Arial', 12),
            variable=self.player_role,
            value="O",
            command=self.set_role_o
        )
        self.role_o_button.grid(row=6, column=2)

        # Initially hide role selection until Single Player is selected
        self.toggle_role_options(visible=False)

    def toggle_role_options(self, visible: bool) -> None:

        """
        Show or hide role options based on game mode.
        """
        state = "normal" if visible else "disabled"
        self.role_label.config(state=state)
        self.role_x_button.config(state=state)
        self.role_o_button.config(state=state)

    def set_role_x(self) -> None:

        """
        Set player role to X, reset scores, and reset the board.
        Player goes first as X, AI will wait until after player moves.
        """
        self.player_role.set("X")
        self.reset_scores()
        self.reset_board()

    def set_role_o(self) -> None:

        """
        Set player role to O, reset scores, and reset the board.
        The AI (X) will move first after the board is reset if in single-player mode.
        """
        self.player_role.set("O")
        self.reset_scores()
        self.reset_board()

    def set_single_player(self) -> None:

        """
        Switch to Single Player mode and reset the board.
        """
        if self.game_mode != "Single Player":
            self.reset_scores()
        self.game_mode = "Single Player"
        self.single_player_button.config(bg="lightblue")
        self.multiplayer_button.config(bg="SystemButtonFace")
        self.toggle_role_options(visible=True)
        self.reset_board()

    def set_multiplayer(self) -> None:

        """
        Switch to Multiplayer mode and reset the board.
        """
        if self.game_mode != "Multiplayer":
            self.reset_scores()
        self.game_mode = "Multiplayer"
        self.multiplayer_button.config(bg="lightblue")
        self.single_player_button.config(bg="SystemButtonFace")
        self.toggle_role_options(visible=False)
        self.reset_board()
        self.ai_turn = False

    def handle_click(self, row: int, col: int) -> None:

        """
        Handle player clicks on the game board.
        """
        if self.game_over or self.ai_turn or self.buttons[row][col]["text"] != "":
            return

        self.buttons[row][col]["text"] = self.game_logic.current_player

        if self.check_game_status():
            return

        self.game_logic.switch_player()
        self.update_turn_label()

        # In single player, if after the player's move it's now the AI's turn, trigger the AI
        if self.game_mode == "Single Player" and self.game_logic.current_player != self.player_role.get():
            # The AI will move after a delay
            self.ai_turn = True
            self.master.after(2000, self.ai_move)

    def ai_move(self) -> None:

        """
        Execute the AI's move after a delay.
        The AI logic is based on the current player in self.game_logic.
        """
        if self.game_over:
            return

        ai_player = self.game_logic.current_player
        human_player = "O" if ai_player == "X" else "X"

        def find_winning_move(player: str):
            for r in range(3):
                for c in range(3):
                    if self.buttons[r][c]["text"] == "":
                        self.buttons[r][c]["text"] = player
                        temp_board = [[b["text"] for b in ro] for ro in self.buttons]
                        if self.game_logic.check_winner(temp_board):
                            self.buttons[r][c]["text"] = ""
                            return (r, c)
                        self.buttons[r][c]["text"] = ""
            return None

        self.ai_move_counter += 1

        if self.ai_move_counter % 5 == 0:
            # Random move every 5 moves
            available_moves = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
            if not available_moves:
                return
            row, col = random.choice(available_moves)
        else:
            # Try a winning move
            winning_move = find_winning_move(ai_player)
            if winning_move:
                row, col = winning_move
            else:
                # Try a blocking move
                blocking_move = find_winning_move(human_player)
                if blocking_move:
                    row, col = blocking_move
                else:
                    # No immediate win or block, choose random
                    available_moves = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
                    if not available_moves:
                        return
                    row, col = random.choice(available_moves)

        self.buttons[row][col]["text"] = ai_player

        if self.check_game_status():
            return

        self.game_logic.switch_player()
        self.update_turn_label()
        self.ai_turn = False

    def reset_board(self) -> None:

        """
        Reset the game board for a new game.
        """
        for row in self.buttons:
            for btn in row:
                btn["text"] = ""
        self.game_logic.reset_game()
        self.update_turn_label()
        self.ai_turn = False
        self.ai_move_counter = 0
        self.game_over = False

        # If Single Player and player chose O, AI (X) goes first after board reset.
        if self.game_mode == "Single Player" and self.player_role.get() == "O":
            self.ai_turn = True
            self.master.after(2000, self.ai_move)
        # If player chose X, no AI turn is triggered until after the player makes a move.

    def reset_scores(self) -> None:

        """
        Reset the scores for wins and draws.
        """
        self.game_logic.scores = {"X": 0, "O": 0, "Draws": 0}
        self.update_score_label()

    def update_turn_label(self) -> None:

        """
        Update the turn indicator label.
        """
        self.turn_label.config(text=self.get_turn_text())

    def update_score_label(self) -> None:

        """
        Update the score display label.
        """
        self.score_label.config(text=self.get_score_text())

    def get_turn_text(self) -> str:

        """
        Get the text for the current player's turn.
        """
        return f"Player {self.game_logic.current_player}'s Turn"

    def get_score_text(self) -> str:

        """
        Get the text for the score display.
        """
        return (f"X Wins: {self.game_logic.scores['X']} | "
                f"O Wins: {self.game_logic.scores['O']} | "
                f"Draws: {self.game_logic.scores['Draws']}")

    def check_game_status(self) -> bool:

        """
        Check if the game has ended with a win or draw.
        """
        board = [[btn["text"] for btn in row] for row in self.buttons]

        if self.game_logic.check_winner(board):
            self.game_over = True
            self.game_logic.increment_win_counter()
            self.update_score_label()
            messagebox.showinfo("Game Over", f"Player {self.game_logic.current_player} wins!")
            self.reset_board()
            return True

        if self.game_logic.check_draw(board):
            self.game_over = True
            self.game_logic.increment_draw_count()
            self.update_score_label()
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_board()
            return True

        return False