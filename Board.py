class Board:
    """
    Represents the Tic-Tac-Toe board and handles operations related to the board.
    """

    def __init__(self):
        """
        Initializes the board with an empty 3x3 grid.
        """
        self.game_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def print_board(self):
        """
        Prints the current state of the board to the console.
        """
        print("\t".join([" ", "A", "B", "C"]))
        for i, row in enumerate(self.game_board):
            print("\t".join([str(i + 1)] + row))

    def is_move_valid(self, move: str):
        """
        Checks if the given move is valid based on board state and move format.

        :param move: A string representing the move in the format "rowLetter" (e.g., "1A").
        :return: True if the move is valid, False otherwise.
        """
        if len(move) != 2:
            return False
        if not move[0].isdigit():
            return False
        x = int(move[0]) - 1
        if x < 0 or x > 2:
            return False
        y = ord(move[1]) - ord('A')
        if y < 0 or y > 2:
            return False
        if self.game_board[x][y] != ' ':
            return False
        return True

    def submit_move(self, move: str, player: str) -> bool:
        """
        Submits a move for the player and updates the board if the move is valid.

        :param move: A string representing the move in the format "rowLetter" (e.g., "1A").
        :param player: A string representing the player's marker ('X' or 'O').
        :return: True if the move was successfully submitted, False otherwise.
        """
        x = int(move[0]) - 1
        y = ord(move[1]) - ord('A')
        if self.game_board[x][y] == ' ':
            self.game_board[x][y] = player
            return True
        return False

    def is_winner(self, player):
        """
        Checks if the given player has won the game.

        :param player: A string representing the player's marker ('X' or 'O').
        :return: True if the player is a winner, False otherwise.
        """
        for row in self.game_board:
            if all(i == player for i in row):
                print(f"{player} is the winner")
                return True
        for i in range(3):
            if all(self.game_board[j][i] == player for j in range(3)):
                print(f"{player} is the winner")
                return True
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] == player:
            print(f"{player} is the winner")
            return True
        if self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] == player:
            print(f"{player} is the winner")
            return True
        return False

    def is_full(self):
        """
        Checks if the board is completely filled with no empty spaces.

        :return: True if the board is full, False otherwise.
        """
        return len(self.get_empty_places()) == 0

    def is_tie(self):
        """
        Checks if the game has ended in a tie (draw).

        :return: True if the game is a tie, False otherwise.
        """
        return self.is_full() and not self.is_winner('X') and not self.is_winner('O')

    def get_empty_places(self):
        """
        Gets a list of all empty places on the board where a move can be made.

        :return: A list of strings representing empty places in the format "rowLetter".
        """
        empty = []
        for y, row in enumerate(self.game_board):
            for x, cell in enumerate(row):
                if cell == ' ':
                    empty.append(f"{y + 1}{chr(x + ord('A'))}")
        return empty

    def get_str_board(self):
        """
        Gets a string representation of the board for storage or display purposes.

        :return: A string representation of the board where empty spaces are replaced with underscores.
        """
        str_board = "[" + "][".join([",".join(self.game_board[i]) for i in range(3)]) + "]"
        return str_board.replace(" ", "_")
