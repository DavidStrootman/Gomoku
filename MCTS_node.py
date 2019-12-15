class MCTSNode:
    def __init__(self, board, parent_node, unexplored_moves, depth, move):
        self.board = board
        self.parent_node = parent_node
        self.unexplored_moves = unexplored_moves
        self.depth = depth
        self.current_move = move

        self.child_nodes = []
        self.uct = float("-inf")

        if len(self.unexplored_moves) == 0:
            self.terminal = True
        else:
            self.terminal = False
        self.n_wins = 0
        self.n_visits = 0

    def get_valid_moves(self):
        valid_moves = self.unexplored_moves.copy()
        for child in self.child_nodes:
            valid_moves.append(child.current_move)
        return valid_moves

    def add_child(self, node):
        self.child_nodes.append(node)

    def is_fully_expanded(self):
        if len(self.unexplored_moves) is 0:
            return True
        return False
