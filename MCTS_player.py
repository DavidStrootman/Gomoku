import random
import MCTS
import gomoku
class MCTSPlayer:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.board_size = None
        self.black = black_
        self.simulation_game = None
        self.debug_alg = None

        self.round = 0

    def new_game(self, black_):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        if self.round == 1:
            self.simulation_game = gomoku.gomoku_game(bsize_=self.board_size)

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        if self.board_size is None:
            self.board_size = len(board[0])
        if self.simulation_game is None:
            self.simulation_game = gomoku.gomoku_game(bsize_=len(board[0]))
        if last_move is not None:
            self.simulation_game.move(last_move)
        self.debug_alg = MCTS.MCTS(self.simulation_game, max_time_to_move, self.black)
        best_move = self.debug_alg.best_move()
        return best_move

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "dumb_robot 1737557"