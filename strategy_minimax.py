import random
from strategy import Strategy


class StrategyMinimax(Strategy):
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


def minimax_move(state):
    ''' (Move, GameState) -> int
        
    Return a score(0, 1, -1) of each move with respect to next_player.
    '''

    if state.over:
        return state.outcome()
    else:
        return max([-minimax_move(state.apply_move(x)) 
                    for x in state.possible_next_moves()])
