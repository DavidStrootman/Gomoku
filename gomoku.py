import copy
import itertools

class gomoku_game:
    """This class specifies the game dynamics of the gomoku game
    implementing the tournaments rules as on https://www.jijbent.nl/spelregels/go-moku.php"""
    def __init__(self, bsize_=19, board_=None, ply_=1, current_empty=None):
        if(board_ is None):
            self.board = []
            for i in range(bsize_):
                self.board.append([0] * bsize_)  # Not repeating the list because of the pointers
        else:
            self.board = board_
        self.ply=ply_
        self.bsize = bsize_
        self.previous_move = None
        rclist = list(range(bsize_))
        if(current_empty is None):
            self.empty = list(itertools.product(rclist,rclist))
        else:
            self.empty = current_empty
        assert self.bsize%2 == 1

    def current_board(self):
        """Returns a deep copy of the board, making it harder for agents to state of the board by accident."""
        return copy.deepcopy(self.board)

    def current_board_unsafe(self):
        """Returns the (reference to the) board, should not be used for the competition."""
        return self.board

    def valid_moves(self):
        """This method returns a list of valid moves, where each move is a tuple with an x and y position on the board."""
        middle = int(self.bsize / 2)
        if self.ply == 1:
            valid_moves = [(middle, middle)]
            return valid_moves
        elif self.ply == 3:
            valid_moves = copy.deepcopy(self.empty)
            rclist = list(range(middle-2,middle+3))
            centre = list(itertools.product(rclist,rclist))
            centre.remove((middle,middle)) #Leads to an error otherwise; cannot remove as not contained in valid_moves
            if(self.previous_move in centre):
                centre.remove(self.previous_move) #if white moved in the centre
            for x in centre:
                valid_moves.remove(x)
            return valid_moves
        else:
            valid_moves = copy.deepcopy(self.empty)
            return valid_moves

    def check_win(self, last_move):
        """This method checks whether the last move played wins the game.
        The rule for winning is: /exactly/ 5 stones line up (so not 6 or more),
        horizontally, vertically, or diagonally."""
        color = self.board[last_move[0]][last_move[1]]
        #check up-down
        number_ud = 1
        if(last_move[1]<self.bsize-1):
            lim1 = last_move[1]+1
            lim2 = last_move[1]+6 if last_move[1]+6<self.bsize else self.bsize
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
        #check left - right
        number_lr = 1
        if (last_move[0] < self.bsize - 1):
            lim1 = last_move[0] + 1
            lim2 = last_move[0] + 6 if last_move[0] + 6 < self.bsize else self.bsize
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
        #check lower left - upper right
        number_diag = 1
        xlim = last_move[0] - 1
        ylim = last_move[1] - 1
        while (xlim>=0 and ylim>=0):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim-1
            ylim = ylim-1
        xlim = last_move[0] + 1
        ylim = last_move[1] + 1
        while (xlim<self.bsize and ylim<self.bsize):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim + 1
        if number_diag == 5:
            return True
        #check lower right - upper left
        number_diag = 1
        xlim = last_move[0] + 1
        ylim = last_move[1] - 1
        while (xlim <self.bsize and ylim >= 0):
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
        if move_tuple[0]<0 or move_tuple[0]>=self.bsize or move_tuple[1]<0 or move_tuple[1]>=self.bsize:
            return False, False
        if self.board[move_tuple[0]][move_tuple[1]] == 0:
            if self.ply in [1,3]:
                if move_tuple not in self.valid_moves() :
                    return False, False
            place = 2 if self.ply%2 else 1
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
    :param board: a d by d list representing the board, 0 being empty, 1 white? stone, and 2 a black? stone
    """
    for row in board:
        for val in row:
            if(val==0):
                print('- ',end='')
            elif(val==1):
                print('w ',end='')
            elif(val==2):
                print('b ',end='')
        print()





