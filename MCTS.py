import copy
import random

import gomoku
import MCTS_node
import time
import math

def deepcopy(arr):
    return arr[:]

def deepcopy2d(arr):
    return [row[:] for row in arr]

class MCTS:
    def __init__(self, game, max_time, black):
        self.game = game
        self.max_time = max_time
        self.black = black

        self.current_board = deepcopy2d(self.game.board)
        self.root_node = MCTS_node.MCTSNode(self.current_board.copy(), None, self.game.valid_moves(), 0, None)
        self.start_time = time.time_ns()
        self.exploration_term = 0.11

    def best_move(self):
        while (self.max_time * 1_000_000) / 2 > time.time_ns() - self.start_time:
            leaf_node = self.find_spot_to_expand(self.root_node)

            val = self.rollout(leaf_node)
            self.backup_value(leaf_node, val)

        # TODO: maybe optimise this by saving uct in node
        best_child = self.find_child_with_highest_uct_value(self.root_node)
        if best_child is None:
            print("not enough time to create child node/slow code maybe")
        self.root_node = best_child
        self.game.move(best_child.current_move)
        self.current_board = self.game.current_board()

        return best_child.current_move

    def find_child_with_highest_uct_value(self, parent_node):
        highest_uct = float('-inf')
        node_with_highest_uct = None
        for child_node in parent_node.child_nodes:
            if child_node.n_visits == 0:
                uct = 0
            else:
                exploitation = child_node.n_wins / child_node.n_visits
                exploration = self.exploration_term * math.sqrt(math.log2(parent_node.n_visits) / child_node.n_visits)
                uct = exploitation + exploration
                child_node.uct = uct
            if uct > highest_uct:
                highest_uct = uct
                node_with_highest_uct = child_node
        return node_with_highest_uct

    def find_spot_to_expand(self, parent_node):
        if parent_node.terminal:
            return parent_node
        if not parent_node.is_fully_expanded():
            new_move = random.choice(parent_node.unexplored_moves)

            parent_node.unexplored_moves.remove(new_move)
            new_board = self.game.current_board_unsafe()
            new_valid_moves = self.game.empty.copy()
            new_valid_moves.remove(new_move)
            if parent_node.unexplored_moves == 0:
                parent_node.terminal = True
            new_node = MCTS_node.MCTSNode(new_board, parent_node, new_valid_moves, parent_node.depth + 1, new_move)
            parent_node.add_child(new_node)
            return new_node
        highest_uct_node = self.find_child_with_highest_uct_value(parent_node)
        return self.find_spot_to_expand(highest_uct_node)

    def rollout(self, node):
        simulated_game = gomoku.gomoku_game(self.game.bsize, deepcopy2d(self.current_board), self.game.ply + 1, self.game.empty.copy())
        new_move = node.current_move
        while not node.terminal:
            available_moves = list(set(simulated_game.valid_moves()) & set(node.unexplored_moves))
            new_move = random.choice(available_moves)
            win = simulated_game.move(new_move)[1]
            node.unexplored_moves.remove(new_move)
            if node.unexplored_moves == 0 or win:
                node.terminal = True
            # Create a new node with the current move, parent node and its unexplored moves
            new_node = MCTS_node.MCTSNode(simulated_game.current_board_unsafe(), node, node.unexplored_moves.copy(), node.depth + 1, new_move)
            node.add_child(new_node)
        node.final_state = simulated_game.check_win(new_move)
        return node.final_state

    def backup_value(self, node, val):
        while node is not None:
            node.n_visits += 1
            # FIXME: Check if this actually does anything
            if self.black and (node.depth % 2 == 0) or not self.black and (node.depth % 2 != 0):
                node.n_wins -= val
            else:
                node.n_wins += val
            node = node.parent_node
