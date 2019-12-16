"""
High quality gomoku AI Made by Fusion86.
https://github.com/Fusion86/gomoku_yasuo/blob/master/src/yasuo.py

Usage:
```
player1 = yasuo.yasuo()
player2 = random_player.random_dummy_player()
comp = competition()
comp.register_player(player1)
comp.register_player(player2)
comp.play_competition()
comp.print_scores()
```
"""

from __future__ import annotations

import math
import time
import random
import itertools
from collections import namedtuple


class yasuo_gomoku_game:
    """This class specifies the game dynamics of the gomoku game
    implementing the tournaments rules as on https://www.jijbent.nl/spelregels/go-moku.php"""

    def __init__(self, bsize_=19, board_=None, ply_=1, current_empty=None):
        if(board_ is None):
            self.board = []
            for _ in range(bsize_):
                # Not repeating the list because of the pointers
                self.board.append([0] * bsize_)
        else:
            self.board = board_
        self.ply = ply_
        self.bsize = bsize_
        self.previous_move = None
        rclist = list(range(bsize_))
        if(current_empty is None):
            self.empty = list(itertools.product(rclist, rclist))
        else:
            self.empty = current_empty

    def current_board(self):
        """Returns a deep copy of the board, making it harder for agents to state of the board by accident."""
        return deepcopy2d(self.board)

    def current_board_unsafe(self):
        """Returns the (reference to the) board, should not be used for the competition."""
        return self.board

    def valid_moves(self):
        """This method returns a list of valid moves, where each move is a tuple with an x and y position on the board."""
        if self.ply == 1:
            middle = int(self.bsize / 2)
            valid_moves = [(middle, middle)]
            return valid_moves
        elif self.ply == 3:
            middle = int(self.bsize / 2)
            valid_moves = deepcopy(self.empty)
            rclist = list(range(middle-2, middle+3))
            centre = list(itertools.product(rclist, rclist))
            # Leads to an error otherwise; cannot remove as not contained in valid_moves
            centre.remove((middle, middle))
            if(self.previous_move in centre):
                # if white moved in the centre
                centre.remove(self.previous_move)
            for x in centre:
                try:
                    valid_moves.remove(x)
                except:
                    pass  # Just accept that it is like this

            return valid_moves
        else:
            valid_moves = deepcopy(self.empty)
            return valid_moves

    def check_win(self, last_move):
        """This method checks whether the last move played wins the game.
        The rule for winning is: /exactly/ 5 stones line up (so not 6 or more),
        horizontally, vertically, or diagonally."""
        color = self.board[last_move[0]][last_move[1]]
        # check up-down
        number_ud = 1
        if(last_move[1] < self.bsize-1):
            lim1 = last_move[1]+1
            lim2 = last_move[1]+6 if last_move[1] + \
                6 < self.bsize else self.bsize
            for i in range(lim1, lim2):
                if self.board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if (last_move[1] > 0):
            lim2 = last_move[1] - 5 if last_move[1]-5 > 0 else 0
            for i in reversed(range(lim2, last_move[1])):
                if self.board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if number_ud == 5:
            return True
        # check left - right
        number_lr = 1
        if (last_move[0] < self.bsize - 1):
            lim1 = last_move[0] + 1
            lim2 = last_move[0] + 6 if last_move[0] + \
                6 < self.bsize else self.bsize
            for i in range(lim1, lim2):
                if self.board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if (last_move[0] > 0):
            lim2 = last_move[0] - 5 if last_move[0] - 5 > 0 else 0
            for i in reversed(range(lim2, last_move[0])):
                if self.board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if number_lr == 5:
            return True
        # check lower left - upper right
        number_diag = 1
        xlim = last_move[0] - 1
        ylim = last_move[1] - 1
        while (xlim >= 0 and ylim >= 0):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim-1
            ylim = ylim-1
        xlim = last_move[0] + 1
        ylim = last_move[1] + 1
        while (xlim < self.bsize and ylim < self.bsize):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim + 1
        if number_diag == 5:
            return True
        # check lower right - upper left
        number_diag = 1
        xlim = last_move[0] + 1
        ylim = last_move[1] - 1
        while (xlim < self.bsize and ylim >= 0):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim - 1
        xlim = last_move[0] - 1
        ylim = last_move[1] + 1
        while (xlim >= 0 and ylim < self.bsize):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim - 1
            ylim = ylim + 1
        if number_diag == 5:
            return True
        return False

    def move(self, move_tuple):
        """Performs the provided move. The move is a tuple of an x and y position on the board."""
        if move_tuple[0] < 0 or move_tuple[0] >= self.bsize or move_tuple[1] < 0 or move_tuple[1] >= self.bsize:
            return False, False
        if self.board[move_tuple[0]][move_tuple[1]] == 0:
            if self.ply in [1, 3]:
                if move_tuple not in self.valid_moves():
                    return False, False
            place = 2 if self.ply % 2 else 1
            self.board[move_tuple[0]][move_tuple[1]] = place
            self.ply += 1
            self.empty.remove(move_tuple)
            self.previous_move = move_tuple
            return True, self.check_win(move_tuple)
        else:
            return False, False


def prettyboard(board):
    """
    Function to print the board to the standard out
    :param board: a d by d list representing the board, 0 being empty, 1 black stone, and 2 a white stone
    """
    for row in board:
        for val in row:
            if(val == 0):
                print('- ', end='')
            elif(val == 1):
                print('o ', end='')
            else:
                print('x ', end='')
        print()


def deepcopy(arr):
    return arr[:]


def deepcopy2d(arr):
    return [row[:] for row in arr]


class yasuo_node:
    def __init__(self, parent: yasuo_node, ply: int, board: list, valid_moves: list, current_move: list, board_empty: list = None):
        self.parent = parent
        self.children: list(yasuo_node) = []
        self.ply = ply

        # Board with current move applied
        self.board = board
        self.board_empty = board_empty

        self.visits = 0
        self.score = 0

        # If this is the final node, aka board + current_move resulted in a game over
        self.terminal = False

        # 1 if black won, 2 if white won
        self.winner = None

        self.current_move = current_move
        self.unexplored_moves = valid_moves
        self.is_fully_explored = False

    def uct(self):
        if (self.visits == 0):
            return 0

        # 0.7 = c
        return (self.score / self.visits) \
            + 0.7 * math.sqrt(math.log2(self.parent.visits) / self.visits)

    def rollout(self, max_depth=math.inf, game: yasuo_gomoku_game = None) -> yasuo_node:
        """
        Rollout.

        Returns final node.
        """

        if self.is_fully_explored:
            return self
        elif not self.has_unexplored_moves():
            # Check is True when `len(self.children) == 0`
            if all(x.is_fully_explored for x in self.children):
                self.is_fully_explored = True
                return self

            node = self.get_best_child()
        else:
            node, game = self.explore_random_move(game)

        if node.terminal:
            return node

        if (max_depth > 0):
            return node.rollout(max_depth - 1, game)
        else:
            return node

    def get_best_child(self) -> yasuo_node:
        """
        Returns best child based on uct().
        """
        return max(self.children, key=lambda x: x.uct())

    def has_unexplored_moves(self):
        return len(self.unexplored_moves) != 0

    def expand(self) -> yasuo_node:
        """
        Add new child node for a random unexplored move.

        Returns new node.
        """
        if not self.has_unexplored_moves():
            raise Exception("Cannot expand when there are no unexplored moves!")

        return self.explore_random_move()[0]

    def is_black(self):
        return self.ply % 2 == 1

    def get_board_size(self):
        return len(self.board)

    def prettyboard(self):
        prettyboard(self.board)

    # def get_board_with_move_applied(self, move):
    #     # FIXME: Deepcopy bad
    #     board = copy.deepcopy(self.board)
    #     stone = 1 if self.is_black() else 2
    #     board[move[0]][move[1]] = stone
    #     return board

    def explore_random_move(self, game: yasuo_gomoku_game = None) -> yasuo_node:
        """
        Explore random unexplored move.

        Returns new node.
        """
        # TODO: This might be broken
        if game == None:
            if self.board_empty == None:
                self.board_empty = yasuo.get_empty_spaces(self.board)
            game = yasuo_gomoku_game(self.get_board_size(), deepcopy2d(self.board), self.ply + 1, deepcopy2d(self.board_empty))

        # Select random unexplored move to expand
        next_move = random.choice(self.unexplored_moves)
        self.unexplored_moves.remove(next_move)

        res = game.move(next_move)

        # TODO: This is probably broken?
        # if game.ply == 2 or game.ply == 3 or game.ply == 4:
        unexplored_moves = game.valid_moves()
        # else:
        #     unexplored_moves = deepcopy(self.unexplored_moves)

        node = yasuo_node(self, self.ply + 1, deepcopy2d(game.board),
                          unexplored_moves, next_move, deepcopy2d(game.empty))
        self.children.append(node)

        if not res[0]:
            raise Exception("Invalid move!")

        # There is a winner
        if res[1]:
            node.is_fully_explored = True
            node.terminal = True
            node.winner = 1 if node.is_black() else 2
        elif not node.has_unexplored_moves():
            node.is_fully_explored = True

        return node, game


class yasuo:
    """
    Monte Carlo tree search based player for gomoku.
    """

    def __init__(self, black=True):
        """
        Constructor for the player.
        """
        self.black = black
        self.root = None
        self.total_counter = None

    def new_game(self, black):
        """
        At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black
        self.root: yasuo_node = None
        self.total_counter = 0
        # print("New game")
        # print("Black: {}".format(self.black))

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """
        This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        remaining_ns = max_time_to_move * 1_000_000  # Milliseconds to nanoseconds

        # Create root node if there is none
        if self.root == None:
            ply = 0 if self.black else 1
            self.root = yasuo_node(None, ply, board, deepcopy(valid_moves), last_move)
        else:
            # TODO: This might be broken
            new_root = None
            for x in self.root.children:
                for y in x.children:
                    if y.board == board:
                        y.parent = None
                        new_root = y
                        break

            if new_root == None:
                new_root = yasuo_node(None, self.root.ply + 2, board, deepcopy(valid_moves), last_move)

            self.root = new_root

        counter = 0
        depth = 2
        while True:
            start = time.time_ns()
            node = self.find_spot_to_expand(self.root)
            tail = node.rollout(depth)
            val = 0.5
            if node.terminal:
                my_id = 1 if self.black else 2
                if node.winner == my_id:
                    val = 1
                elif node.winner != None:
                    val = 0
            self.backup_value(tail, val)

            counter = counter + 1
            if not self.root.has_unexplored_moves():
                depth = depth + 2  # This happens almost never, so that might be a bug?

            # Time stuff
            used_time = time.time_ns() - start
            remaining_ns = remaining_ns - used_time
            if remaining_ns < (used_time * 100):
                break  # Out of time, stop

        best_child = self.root.get_best_child()

        if best_child != None:
            self.total_counter = self.total_counter + counter
            total_avg = self.total_counter / (best_child.ply / 2)
            # print("Counter      {}          {}".format(counter, total_avg))

        # Hacky code, but I don't feel like fixing it
        if best_child is not None and best_child.current_move in valid_moves:
            return best_child.current_move

        # Just pick a random move as a last resort
        # print("Picked random move")
        return random.choice(valid_moves)

    def id(self):
        """
        Please return a string here that uniquely identifies your submission e.g., "name (student_id)"
        """
        return "0/8 powerspike (1735388)"

    def find_spot_to_expand(self, root: yasuo_node) -> yasuo_node:
        if root.terminal:
            return root

        if root.has_unexplored_moves():
            return root.expand()

        return self.find_spot_to_expand(root.get_best_child())

    def backup_value(self, tail: yasuo_node, value):
        while tail != None:
            tail.visits = tail.visits + 1
            # If own move
            if tail.is_black() == self.black:
                tail.score = tail.score + value
            else:
                tail.score = tail.score - value
            tail = tail.parent

    @staticmethod
    def get_empty_spaces(board: list):
        empty = []
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == 0:
                    empty.append((x, y))
        return empty
