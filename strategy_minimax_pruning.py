import random
from strategy import Strategy


class StrategyMinimaxPruning(Strategy):
    ''' Interface to suggest a strong move.

    '''

    def suggest_move(self, state):
        '''(Minimax, GameState) -> Move

        Return a strong move from those available for state.

        Overrides Strategy.suggest_move
        '''
        
        score_to_move = {}
        for m in state.possible_next_moves():
            s = state.apply_move(m)
            score = - minimax_move(s)
            if score not in score_to_move:
                score_to_move[score] = []
            score_to_move[score].append(m)
        best_score = max(score_to_move.keys())
        return random.choice(score_to_move[best_score])


def minimax_move(state, min = -1, max = 1):
    ''' (Move, GameState) -> int
        
    Return a score(0, 1, -1) of each move with respect to next_player.
    '''
    if state.over:
        return state.outcome()
    elif state.next_player == 'p1':
        v = min
        if v != 1:
            for x in state.possible_next_moves():
                if minimax_move(state.apply_move(x), min = v) > v:
                    v = minimax_move(state.apply_move(x))
            return v
    else:
        v = max
        if v != -1:
            for x in state.possible_next_moves():
                if minimax_move(state.apply_move(x), max = v) < v:
                    v = minimax_move(state.apply_move(x))
            return v
