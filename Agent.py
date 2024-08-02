import random
from abc import ABC, abstractmethod
from enum import Enum


class AgentType(Enum):
    """
    Enumeration for the types of agents that can play the game.
    """
    HUMAN_AGENT = 1
    RANDOM_AGENT = 2
    SMARTAGENT = 3


class Agent(ABC):
    """
    Abstract base class for agents in the Tic-Tac-Toe game.
    """

    def __init__(self, marker, board):
        """
        Initializes the agent with a marker and board.

        :param marker: The marker for the agent ('X' or 'O').
        :param board: The game board instance.
        """
        self.marker = marker
        self.board = board

    @abstractmethod
    def get_player_move(self):
        """
        Abstract method for getting the player's move. To be implemented by subclasses.
        """
        pass


class HumanAgent(Agent):
    """
    Represents a human player in the Tic-Tac-Toe game.
    """

    def __init__(self, marker, board, agent_type: AgentType):
        """
        Initializes the human agent.

        :param marker: The marker for the human agent ('X' or 'O').
        :param board: The game board instance.
        :param agent_type: The type of the agent (AgentType).
        """
        super().__init__(marker, board)
        self.agent_type = agent_type

    def get_player_move(self):
        """
        Gets the move from the human player via console input. Ensures the move is valid.

        :return: The validated move as a string.
        """
        move = input("Please enter a move, for example 1A: ")
        while not self.board.is_move_valid(move):
            move = input(f"The move {move} is invalid, Please enter a move, for example 1A: ")
        return move


class RandomAgent(Agent):
    """
    Represents a random agent in the Tic-Tac-Toe game.
    """

    def __init__(self, marker, board, agent_type: AgentType):
        """
        Initializes the random agent.

        :param marker: The marker for the random agent ('X' or 'O').
        :param board: The game board instance.
        :param agent_type: The type of the agent (AgentType).
        """
        super().__init__(marker, board)
        self.agent_type = agent_type

    def get_player_move(self):
        """
        Gets a random move from the list of empty places on the board.

        :return: A random move as a string.
        """
        return random.choice(self.board.get_empty_places())


class SmartAgent(Agent):
    """
    Represents a smart agent in the Tic-Tac-Toe game that uses a strategy to make decisions.
    """

    def __init__(self, marker, board, agent_type: AgentType, scoreboards):
        """
        Initializes the smart agent.

        :param marker: The marker for the smart agent ('X' or 'O').
        :param board: The game board instance.
        :param agent_type: The type of the agent (AgentType).
        :param scoreboards: The scoreboard data for evaluating moves.
        """
        super().__init__(marker, board)
        self.agent_type = agent_type
        self.scoreboards = scoreboards

    def get_player_move(self):
        """
        Decides on a move based on a mix of 70% smart strategy and 30% random choice.

        :return: The chosen move as a string.
        """
        r = random.randint(1, 100)
        if r > 30:
            print("play smart")
            return self.smart_decision()
        else:
            print("play random")
            return random.choice(self.board.get_empty_places())

    def smart_decision(self):
        """
        Chooses the best move based on the current board state and scoreboards.

        :return: The best move as a string.
        """
        possible_moves = self.possible_moves()
        best_move = []
        best_score_move = -1
        for move in possible_moves:
            score_move = self.score_move(move[1])
            if score_move > best_score_move:
                best_score_move = score_move
                best_move = move
        return best_move[0]

    def possible_moves(self):
        """
        Calculates all possible moves and their resulting board states.

        :return: A list of possible moves and their resulting board states.
        """
        possible_moves = []
        str_board = self.board.get_str_board()
        empty_places = self.board.get_empty_places()
        for place in empty_places:
            x = int(place[0]) - 1
            y = ord(place[1]) - ord('A')
            update_str_board = list(str_board)
            update_str_board[translate(x, y)] = self.marker
            possible_moves.append([place, ''.join(update_str_board)])
        return possible_moves

    def score_move(self, move):
        """
        Scores a given move based on the current scoreboard.

        :param move: The board state resulting from the move.
        :return: The score associated with the move.
        """
        if self.marker == 'X':
            if move in self.scoreboards:
                return self.scoreboards[move][0]
            else:
                return 0
        move = move.replace('X', 'Y')
        move = move.replace('O', 'X')
        move = move.replace('Y', 'O')
        if move in self.scoreboards:
            return self.scoreboards[move][0]
        else:
            raise Exception("You can't play with two smart agents")
            pass


def translate(x, y):
    """
    Translates the board coordinates into an index for the board's string representation.

    :param x: The row coordinate.
    :param y: The column coordinate.
    :return: The index in the string representation of the board.
    """
    if x == 0:
        return y + 1
    elif x == 1:
        return y + 8
    else:
        return y + 15


class AgentFactory:
    """
    Factory class for creating agents based on the specified type.
    """

    @staticmethod
    def get_agent(i: AgentType, marker, board, scoreboards):
        """
        Creates an agent instance based on the agent type.

        :param i: The type of the agent (AgentType).
        :param marker: The marker for the agent ('X' or 'O').
        :param board: The game board instance.
        :param scoreboards: The scoreboard data for evaluating moves.
        :return: An instance of the appropriate agent.
        """
        if i == AgentType.SMARTAGENT:
            return SmartAgent(marker, board, i, scoreboards)
        agents = [None, HumanAgent, RandomAgent]
        return agents[i.value](marker, board, i)
