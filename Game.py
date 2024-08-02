import random
from Agent import AgentFactory, AgentType
from Board import Board
import json


class Tournament:
    """
    Manages a tournament of Tic-Tac-Toe games between two types of agents.
    """

    def __init__(self, player1_type: AgentType, player2_type: AgentType, amount_of_games=1):
        """
        Initializes the tournament with specified player types and number of games.

        :param player1_type: Type of the first player (AgentType).
        :param player2_type: Type of the second player (AgentType).
        :param amount_of_games: Number of games to play in the tournament.
        """
        self.player1_type = player1_type
        self.player2_type = player2_type
        self.points_player1 = 0
        self.points_player2 = 0
        self.amount_of_games = amount_of_games
        self.win = "no"

    def start_a_tournament(self):
        """
        Starts the tournament, playing the specified number of games and updating scores.
        """
        print("The tournament begins!")
        for i in range(self.amount_of_games):
            print(f"game number: {i + 1}")
            winner = Game(self.player1_type, self.player2_type).start_game()
            if winner == "player1":
                self.points_player1 += 1
            elif winner == "player2":
                self.points_player2 += 1
            if self.points_player1 > self.points_player2:
                self.win = "player1"
            elif self.points_player1 < self.points_player2:
                self.win = "player2"
            else:
                self.win = "no"
            print(f"{self.win} leads. Scoring mode: Player 1- {self.points_player1}, Player 2- {self.points_player2}")

    @staticmethod
    def collect_data(amount_of_games=1000000):
        """
        Collects data by running a large number of games between smart and random agents.

        :param amount_of_games: Number of games to be played for data collection.
        """
        for i in range(amount_of_games):
            Game(AgentType.SMARTAGENT, AgentType.RANDOM_AGENT).start_game()


class Game:
    """
    Represents a single game of Tic-Tac-Toe between two agents and manages game play.
    """

    def __init__(self, player1_type: AgentType, player2_type: AgentType):
        """
        Initializes the game with specified player types and sets up the board.

        :param player1_type: Type of the first player (AgentType).
        :param player2_type: Type of the second player (AgentType).
        """
        self.board = Board()
        try:
            with open('sample.json', 'r') as openfile:
                self.scoreboards = json.load(openfile)
        except FileNotFoundError:
            self.scoreboards = {}
        if player1_type == AgentType.SMARTAGENT:
            self.markers = ['X', 'O']
        elif player2_type == AgentType.SMARTAGENT:
            self.markers = ['O', 'X']
        else:
            self.markers = ['O', 'X']
            random.shuffle(self.markers)
        if player1_type == AgentType.SMARTAGENT and player2_type == AgentType.SMARTAGENT:
            raise Exception("You can't play with two smart agents")
        self.player1 = AgentFactory.get_agent(player1_type, self.markers[0], self.board, self.scoreboards)
        self.player2 = AgentFactory.get_agent(player2_type, self.markers[1], self.board, self.scoreboards)
        self.last_move = self.markers.index('O') + 1
        self.current_game_boards = []
        self.gamma = 0.9
        self.winner = None
        self.winner_name = ""

    def add_board(self, board: str, score):
        """
        Updates the scoreboard with the given board state and score.

        :param board: The string representation of the board state.
        :param score: The score to be added.
        """
        if board in self.scoreboards:
            self.scoreboards[board][0] = (self.scoreboards[board][0] * self.scoreboards[board][1] + score) / (
                    self.scoreboards[board][1] + 1)
            self.scoreboards[board][1] += 1
        else:
            self.scoreboards[board] = [score, 1]

    def endgame_calculations(self, first_score):
        """
        Calculates and updates scores for the board states based on the endgame results.

        :param first_score: The initial score assigned based on the game result.
        """
        score = first_score
        self.add_board(self.current_game_boards[-1], score)
        for board in self.current_game_boards[-2::-1]:
            score *= self.gamma
            self.add_board(board, score)

    def start_game(self):
        """
        Starts the game, handles turns, checks for winners, and manages endgame calculations.

        :return: The name of the winning player ("player1" or "player2"), or None if the game was a draw.
        """
        self.print_initial_info()
        while not self.board.is_full() and not self.is_winner():
            self.play_turn()
        self.end_game()
        self.save_scoreboard()
        return self.winner_name

    def print_initial_info(self):
        """
        Prints the initial information of the game including player types, markers, and board state.
        """
        print("The game is starting:")
        print(f"The shape of the first player of type {self.player1.agent_type.name} is {self.player1.marker}")
        print(f"The shape of the second player of type {self.player2.agent_type.name} is {self.player2.marker}")
        self.board.print_board()
        self.current_game_boards.append(self.board.get_str_board())

    def is_winner(self):
        """
        Checks if there is a winner in the current game.

        :return: True if there is a winner, False otherwise.
        """
        return self.winner is not None

    def play_turn(self):
        """
        Executes a single turn of the game based on the current player's move and updates game state.
        """
        current_player = self.player1 if self.last_move == 2 else self.player2
        current_marker = self.player1.marker if self.last_move == 2 else self.player2.marker
        print(f"The turn of {current_marker} ")
        move = current_player.get_player_move()
        if not self.board.submit_move(move, current_marker):
            print("Error! The move is not submitted.")
            return
        self.board.print_board()
        self.current_game_boards.append(self.board.get_str_board())
        if self.board.is_winner(current_marker):
            self.winner = current_marker
            self.winner_name = "player1" if self.last_move == 2 else "player2"
        self.last_move = 2 if self.last_move == 1 else 1

    def end_game(self):
        """
        Handles endgame calculations and determines the result of the game.
        """
        if self.winner is None:
            print("The game ended in a draw")
            self.endgame_calculations(0.5)
        elif self.winner == 'X':
            self.endgame_calculations(1)
        else:
            self.endgame_calculations(0)

    def save_scoreboard(self):
        """
        Saves the current scoreboard to a JSON file.
        """
        with open("sample.json", "w") as outfile:
            json.dump(self.scoreboards, outfile, indent=4)


tic_tac_toe = Tournament(AgentType.RANDOM_AGENT, AgentType.RANDOM_AGENT, 3)
tic_tac_toe.start_a_tournament()
