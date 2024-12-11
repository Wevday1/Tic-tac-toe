from tkinter import Tk
from gui import TicTacToeGUI
from game_logic import TicTacToeLogic

def main() -> None:

    """
    Run the Tic Tac Toe application.
    """
    root = Tk()
    logic = TicTacToeLogic()
    app = TicTacToeGUI(root, logic)
    root.mainloop()

if __name__ == "__main__":
    main()