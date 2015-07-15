import random
from strategy import Strategy


class StrategyMinimaxMyopic(Strategy):
    ''' Interface to suggest a strong move.

    '''
    
    def __init__(self, interactive=False):
        '''(StrategyMinimaxMyopic, bool) -> NoneType

        Create new StrategyMinimaxMyopic (self), prompt user if interactive.
        '''    

    def suggest_move(self, state):
        '''(StrategyMinimaxMyopic, GameState) -> Move

        Return a strong move from those available for state.

        Overrides Strategy.suggest_move
        '''
        
        score_to_move = {}
        n = 3 #how deep we decide to go
        for m in state.possible_next_moves():
            s = state.apply_move(m)
            score = - minimax_move(s, n)
            if score not in score_to_move: #add score as a key in dictionary, if it's not already
                score_to_move[score] = []
            score_to_move[score].append(m) #add move as a value to score
        best_score = max(score_to_move.keys())
        return random.choice(score_to_move[best_score])


def minimax_move(state, n):
    ''' (StrategyMinimaxMyopic, int) -> int
        
    Return a score(0, 1, -1) of each move with respect to next_player.
    '''

    if n <= 0: #when n == 0, the desired depth has been reached 
        return state.rough_outcome()
    elif state.over:
        return state.outcome()
    else:
        return max([-minimax_move(state.apply_move(x), n - 1) #n-1, so that this function is called recursively n times
                    for x in state.possible_next_moves()])
                    
