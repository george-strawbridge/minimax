import random
from strategy import Strategy


class StrategyMinimaxMemoize(Strategy):
    ''' Interface to suggest a strong move.

    '''
    
    def __init__(self, interactive=False):
        '''(StrategyMinimaxMemoize) -> None
        
        Create new StrategyMinimaxMemoize (self), prompt user if interactive.
        '''
        self.state_to_score = {}
        
    def suggest_move(self, state):
        '''(StrategyMinimaxMemoize, GameState) -> Move

        Return a strong move from those available for state.

        Overrides Strategy.suggest_move
        '''
        
        score_to_move = {}
        for m in state.possible_next_moves():
            s = state.apply_move(m)
            score = - minimax_move(s, self.state_to_score)
            if score not in score_to_move: #add the score as a new key to dictionary, if it's not already
                score_to_move[score] = []
            score_to_move[score].append(m) #add move as a value to the score
            if repr(s) not in self.state_to_score: #add the gamestate to the dictionary, if it's not already
                self.state_to_score[repr(s)] = score            
        best_score = max(score_to_move.keys()) #find the best score
        if repr(state) not in self.state_to_score: #add the gamestate to the dictionary, if it's not already
            self.state_to_score[repr(state)] = best_score
        return random.choice(score_to_move[best_score])


def minimax_move(state, state_to_score):
    ''' (GameState, dic of str to int) -> int
        
    Return a score(0, 1, -1) of each move with respect to next_player. 
    If state is in state_to_score, return the score directly.
    '''

    if repr(state) in state_to_score: #check if the gamestate has already been visited
        return state_to_score[repr(state)]
    else: 
        if state.over: #if the game's over, return the score
            score = state.outcome()
            if repr(state) not in state_to_score: #add the gamestate to the dictionary, if it's not already
                state_to_score[repr(state)] = score      
            return score
        else: #recursively run this function until the game is over
            score = max([-minimax_move(state.apply_move(x), state_to_score) 
                        for x in state.possible_next_moves()])
            if repr(state) not in state_to_score: #add the gamestate to the dictionary, if it's not already
                state_to_score[repr(state)] = score  
            return score
            
