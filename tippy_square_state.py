from game_state import GameState
from tippy_move import TippyMove
from copy import deepcopy


class TippyGameState(GameState):
    ''' The state of a Tippy game
    
    board_size: int  -- the size of a game board
    current_board: list of list  -- represents a nxn game board
    '''

    def __init__(self, p, interactive=False, board_size=3, current_board=None):
        ''' (TippyGameState, str, int, list) -> NoneType

        Initialize TippyGameState self with board_size '3x3'

        Assume:  '3x3' <= board_size is an str
                        p in {'p1', 'p2'}
        '''
        if interactive:
            board_size = int(input('Board size? '))
        GameState.__init__(self, p)
        if not current_board:  # if board is not created, create it
            self.current_board = []
            for x in range(board_size):
                d = []
                for y in range(board_size):
                    d.append('_ ')
                self.current_board.append(d)
            self.board_size = board_size
        else:
            self.current_board = deepcopy(current_board)
            self.board_size = len(self.current_board)
            
        # check if the game is over
        self.over = self.winner(self.next_player) or self.winner(
            self.opponent()) or self.possible_next_moves() == [] 
        self.instructions = ('On your turn, you may put your symbol'
                             'on any empty position of the game board ')

    def __repr__(self):
        ''' (TippyGameState) -> str

        Return a string representation of TippyGameState self
        that evaluates to an equivalent TippyGameState

        >>> s = TippyGameState('p1', board_size=1, current_board=[['_ ']])
        >>> s
        TippyGameState('p1', 1, [['_ ']])
        '''
        
        return 'TippyGameState({}, {}, {})'.format(repr(self.next_player), 
                                                   repr(self.board_size), 
                                                   repr(self.current_board))

    def __str__(self):
        ''' (TippyGameState) -> str

        Return a convenient string representation of TippyGameState self.

        >>> s = TippyGameState('p1', False)
        >>> print(s)
        next player: p1
        current game state:
        _ _ _ 
        _ _ _ 
        _ _ _ 
        '''
        board = ''
        i = 0
        for row in self.current_board:
            for column in row:
                board += column
            board += '\n'
        board = board[:-1]
        
        return ('next player: {}'.format(str(self.next_player)) + '\n' + 
                'current game state:' + '\n' + '{}'.format(str(board)))

    def __eq__(self, other):
        ''' (TippyGameState, TippyGameState) -> bool

        Return True iff this TippyGameState is the equivalent to other.

        >>> s1 = TippyGameState('p1', board_size=3, current_board=[['-']])
        >>> s2 = TippyGameState('p1', board_size=3, current_board=[['-']])
        >>> s1 == s2
        True
        '''
        return (isinstance(other, TippyGameState) and
                self.current_board == other.current_board and
                self.next_player == other.next_player and 
                self.board_size == other.board_size)

    def apply_move(self, move):
        ''' (TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyGameState reached by applying move to self.

        >>> s1 = TippyGameState('p1', False, 3)
        >>> s2 = s1.apply_move(TippyMove((1, 1)))
        >>> print(s2)
        next player: p2
        current game state:
        _ _ _ 
        _ X _ 
        _ _ _ 
        '''
        if move in self.possible_next_moves():
            new_board = deepcopy(self.current_board)
            if self.next_player == 'p1':
                new_board[move.coord[0]][move.coord[1]] = 'X '
            else:
                new_board[move.coord[0]][move.coord[1]] = 'O '
            return TippyGameState(self.opponent(), 
                                  current_board=new_board)
        else:
            return None

    def rough_outcome(self):
        '''(TippyGameState) -> float

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state self. 
        
        >>> TippyGameState('p1', board_size=3, current_board=[['_ ', '_ ', '_ '], ['_ ', '_ ', '_ '], ['_ ', '_ ', '_ ']]).rough_outcome()
        0.0
        >>> TippyGameState('p1', board_size=3, current_board=[['_ ', 'X ', '_ '], ['O ', 'X ', 'X '], ['O ', 'O ', '_ ']]).rough_outcome()
        1.0
        >>> TippyGameState('p2', board_size=3, current_board=[['O ', 'X ', 'O '], ['X ', 'X ', 'X '], ['O ', 'O ', '_ ']]).rough_outcome()
        0.0
        >>> TippyGameState('p1', board_size=3, current_board=[['X ', 'O ', '_ '], ['O ', 'O ', 'X '], ['_ ', '_ ', 'X ']]).rough_outcome()
        -1.0
        '''
        if self.next_player == 'p1':
            s = 'X '
            o = 'O '
        else:
            s = 'O '
            o = 'X '
        e = '_ '
        
        # p_score represents how many ways next_player is one move from 
        # winning, o_score represents how many ways opponent can win 
        # considering all the moves next_player can make
        p_score, o_score = 0, 0
        
        # Starts checking from the first interior position, if next_payer 
        # is one move from winning, increnment p_score by 1, if next_player 
        # can't block the opponent from winning by one move, increment
        # o_score by 1. 
        for x in range(1, self.board_size - 1):
            for y in range(1, self.board_size - 1):
                if self.current_board[x][y] == s:
                    if self.current_board[x + 1][y] == s:
                        if self.current_board[x][y + 1] == s:
                            if self.current_board[x - 1][y + 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y - 1] == e:
                                p_score += 1
                        if self.current_board[x][y - 1] == s:
                            if self.current_board[x - 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y + 1] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y - 1] == s:
                            if (
                                x + 2 <= self.board_size and
                                self.current_board[x + 2][y - 1] == e
                            ):
                                p_score += 1
                            if self.current_board[x][y + 1] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y + 1] == s:
                            if (
                                x + 2 <= self.board_size and
                                self.current_board[x + 2][y + 1] == e
                            ):
                                p_score += 1
                            if self.current_board[x][y - 1] == e:
                                p_score += 1                        
                    if self.current_board[x - 1][y] == s:
                        if self.current_board[x][y + 1] == s:
                            if self.current_board[x - 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y + 1] == e:
                                p_score += 1
                        if self.current_board[x][y - 1] == s:
                            if self.current_board[x + 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x - 1][y + 1] == e:
                                p_score += 1                        
                        if self.current_board[x - 1][y + 1] == s:
                            if self.current_board[x][y - 1] == e:
                                p_score += 1
                            if (
                                0 <= x - 2 and 
                                self.current_board[x - 2][y + 1] == e
                            ):
                                p_score += 1                        
                        if self.current_board[x - 1][y - 1] == s:
                            if (
                                0 <= x - 2 and
                                self.current_board[x - 2][y - 1] == e
                            ):
                                p_score += 1
                            if self.current_board[x][y + 1] == e:
                                p_score += 1                         
                        
                    if self.current_board[x][y + 1] == s:
                        if self.current_board[x - 1][y] == s:
                            if self.current_board[x - 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y + 1] == e:
                                p_score += 1
                        if self.current_board[x - 1][y + 1] == s:
                            if (
                                y + 2 <= self.board_size and
                                self.current_board[x - 1][y + 2] == e
                            ):
                                p_score += 1
                            if self.current_board[x + 1][y] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y] == s:
                            if self.current_board[x + 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x - 1][y + 1] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y + 1] == s:
                            if self.current_board[x - 1][y] == e:
                                p_score += 1
                            if (
                                y + 2 <= self.board_size and
                                self.current_board[x + 1][y + 2] == e
                            ):
                                p_score += 1                          
                    if self.current_board[x][y - 1] == s:
                        if self.current_board[x - 1][y] == s:
                            if self.current_board[x - 1][y + 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y - 1] == e:
                                p_score += 1
                        if self.current_board[x - 1][y - 1] == s:
                            if (
                                0 <= y - 2 and
                                self.current_board[x - 1][y - 2] == e
                            ):
                                p_score += 1
                            if self.current_board[x + 1][y] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y] == s:
                            if self.current_board[x - 1][y - 1] == e:
                                p_score += 1
                            if self.current_board[x + 1][y + 1] == e:
                                p_score += 1                        
                        if self.current_board[x + 1][y - 1] == s:
                            if self.current_board[x - 1][y] == e:
                                p_score += 1
                            if (
                                0 <= y - 2 and
                                self.current_board[x + 1][y - 2] == e
                            ):
                                p_score += 1  
                                
                elif self.current_board[x][y] == o:
                    if self.current_board[x + 1][y] == o:
                        if self.current_board[x][y + 1] == o:
                            if (
                                self.current_board[x - 1][y + 1] == e and
                                self.current_board[x + 1][y - 1] == e
                            ):
                                o_score += 1
                        if self.current_board[x][y - 1] == o:
                            if (
                                self.current_board[x - 1][y - 1] == e and
                                self.current_board[x + 1][y + 1] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y - 1] == o:
                            if (
                                x + 2 <= self.board_size and
                                self.current_board[x + 2][y - 1] == e and
                                self.current_board[x][y + 1] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y + 1] == o:
                            if (
                                x + 2 <= self.board_size and
                                self.current_board[x + 2][y + 1] == e and
                                self.current_board[x][y - 1] == e
                            ):
                                o_score += 1                        
                    if self.current_board[x - 1][y] == o:
                        if self.current_board[x][y + 1] == o:
                            if (
                                self.current_board[x - 1][y - 1] == e and
                                self.current_board[x + 1][y + 1] == e
                            ):
                                o_score += 1
                        if self.current_board[x][y - 1] == o:
                            if (
                                self.current_board[x + 1][y - 1] == e and
                                self.current_board[x - 1][y + 1] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x - 1][y + 1] == o:
                            if (
                                self.current_board[x][y - 1] == e and
                                0 <= x - 2 and self.current_board[x - 2][y + 1]
                                == e
                            ):
                                o_score += 1                        
                        if self.current_board[x - 1][y - 1] == o:
                            if (
                                0 <= x - 2 and
                                self.current_board[x - 2][y - 1] == e and
                                self.current_board[x][y + 1] == e
                            ):
                                o_score += 1                         
                        
                    if self.current_board[x][y + 1] == o:
                        if self.current_board[x - 1][y] == o:
                            if (
                                self.current_board[x - 1][y - 1] == e and
                                self.current_board[x + 1][y + 1] == e
                            ):
                                o_score += 1
                        if self.current_board[x - 1][y + 1] == o:
                            if (
                                y + 2 <= self.board_size and
                                self.current_board[x - 1][y + 2] == e and
                                self.current_board[x + 1][y] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y] == o:
                            if (
                                self.current_board[x + 1][y - 1] == e and
                                self.current_board[x - 1][y + 1] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y + 1] == o:
                            if (
                                self.current_board[x - 1][y] == e and
                                y + 2 <= self.board_size and
                                self.current_board[x + 1][y + 2] == e
                            ):
                                o_score += 1                          
                    if self.current_board[x][y - 1] == o:
                        if self.current_board[x - 1][y] == o:
                            if (
                                self.current_board[x - 1][y + 1] == e and
                                self.current_board[x + 1][y - 1] == e
                            ):
                                o_score += 1
                        if self.current_board[x - 1][y - 1] == o:
                            if (
                                0 <= y - 2 and
                                self.current_board[x - 1][y - 2] == e and
                                self.current_board[x + 1][y] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y] == o:
                            if (
                                self.current_board[x - 1][y - 1] == e and
                                self.current_board[x + 1][y + 1] == e
                            ):
                                o_score += 1                        
                        if self.current_board[x + 1][y + 1] == o:
                            if (
                                self.current_board[x - 1][y] == e and
                                0 <= y - 2 and
                                self.current_board[x + 1][y - 2] == e
                            ):
                                o_score += 1              
        # if next_player has more ways of winning than the opponent, returns
        # wins. 
        if p_score > o_score:
            return TippyGameState.WIN
        elif p_score < o_score:
            return TippyGameState.LOSE
        else:
            return TippyGameState.DRAW
                
    def get_move(self):
        '''(TippyGameState) -> TippyMove

        Prompt user and return move.
        '''
        
        x = int(input('Place at which row? (Row number starts at 0) '))
        y = int(input('Place at which column? (Column number starts at 0) '))
        return TippyMove((x, y))
    
    def winner(self, player):
        ''' (TippyGameState, str) -> bool

        Return True iff the game is over and player has won.
        
        Preconditions: player is either 'p1' or 'p2'

        >>> s1 = TippyGameState('p1', False, board_size=3)
        >>> s2 = s1.apply_move(TippyMove((0, 1)))  # p1's move
        >>> s3 = s2.apply_move(TippyMove((1, 1)))   # p2's move
        >>> s3.winner('p1')
        False
        '''
        
        if player == 'p1':
            s = 'X '
        else:
            s = 'O '
        flag = False  # flag indicates whether a z/s tetrimino is formed or not
        x = 1
        while x < self.board_size - 1 and not flag:
            y = 1
            while y < self.board_size - 1 and not flag:
                if self.current_board[x][y] == s:
                    if (
                        self.current_board[x][y - 1] ==
                        self.current_board[x + 1][y] ==
                        self.current_board[x - 1][y - 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x][y - 1] ==
                        self.current_board[x - 1][y] ==
                        self.current_board[x + 1][y - 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x - 1][y] ==
                        self.current_board[x][y + 1] ==
                        self.current_board[x + 1][y + 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x - 1][y + 1] ==
                        self.current_board[x][y + 1] ==
                        self.current_board[x + 1][y] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x - 1][y] ==
                        self.current_board[x - 1][y + 1] ==
                        self.current_board[x][y - 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x + 1][y] ==
                        self.current_board[x + 1][y + 1] ==
                        self.current_board[x][y - 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x - 1][y] ==
                        self.current_board[x - 1][y - 1] ==
                        self.current_board[x][y + 1] == s
                    ):
                        flag = True
                    elif (
                        self.current_board[x + 1][y] ==
                        self.current_board[x + 1][y - 1] ==
                        self.current_board[x][y + 1] == s
                    ):
                        flag = True
                y += 1
            x += 1
            
        return flag

    def possible_next_moves(self):
        ''' (TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal
        from the present state.

        >>> s1 = TippyGameState('p1', board_size=2, current_board=[['_ ', '_ '], ['_ ', '_ ']])
        >>> L1 = s1.possible_next_moves()
        >>> L2 = [TippyMove((0, 0)), TippyMove((0, 1)), TippyMove((1, 0)), TippyMove((1, 1))]
        >>> len(L1) == len(L2) and all([m in L2 for m in L1])
        True
        '''
        moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.current_board[x][y] == '_ ':
                    moves.append(TippyMove((x, y)))
        return moves
                                 
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
