from move import Move


class TippyMove(Move):
    ''' A move in the game of Tippy.

    coord: tuple -- position to place players move.
    '''

    def __init__(self, coord):
        ''' (TippyMove, tuple) -> NoneType

        Initialize a new TippyMove adding players move.

        Assume: position is valid, and two numbers. First number is row
        position, second number is column position, with the first row and 
        first column being 0.
        '''
        self.coord = coord

    def __repr__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove.
        >>> m1 = TippyMove((1, 2))
        >>> m1
        TippyMove((1, 2))
        '''
        return 'TippyMove({})'.format(self.coord)

    def __str__(self):
        ''' (TippyMove) -> str

        Return a string representation of this TippyMove
        that is suitable for users to read.

        >>> m1 = TippyMove('41')
        >>> print(m1)
        Place at row 4, column 1
        '''

        return 'Place at row {}, column {}'.format((self.coord[0]),
                                                   (self.coord[1]))

    def __eq__(self, other):
        ''' (TippyMove, TippyMove) -> bool

        Return True iff this TippyMove is the same as other.

        >>> m1 = TippyMove(4)
        >>> m2 = TippyMove(3)
        >>> print(m1 == m2)
        False
        '''
        return (isinstance(other, TippyMove) and 
                self.coord == other.coord)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
