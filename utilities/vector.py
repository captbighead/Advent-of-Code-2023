class vector:
    """2D vector objects that provide more functionality than tuples"""

    _UP = None
    _RIGHT = None
    _DOWN = None
    _LEFT = None
    _UNIT_VECTORS = None
    _DIAG_VECTORS = None
    
    def __init__(self, x:int=0, y:int=0) -> None:
        self._x = x
        self._y = y
        self._adjacents = set([])
        self._diagonals = set([])

    def distance(self, other):
        """Returns the Manhattan Distance between two vectors"""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def adjacents(self):
        if len(self._adjacents) == 0:
            self._adjacents = set([self + uv for uv in vector.UNIT_VECTORS()])
        return self._adjacents
    
    def rotate_cw(self, steps):
        """Rotates the vector clockwise a number of 90-degree steps."""
        if steps % 4 == 0:
            return self
        elif steps % 4 == 1:
            return vector(-self.y, self.x)
        elif steps % 4 == 2:
            return self * -1
        elif steps % 4 == 3:
            return vector(self.y, -self.x)
    
    def rotate_ccw(self, steps):
        """Rotates the vector counter-clockwise a number of 90-degree steps."""
        if steps % 4 == 0:
            return self
        elif steps % 4 == 1:
            return vector(self.y, -self.x)
        elif steps % 4 == 2:
            return self * -1
        elif steps % 4 == 3:
            return vector(-self.y, self.x)
        
    def pseudo_normalize(self):
        """Reduces x and y such that abs(x) and abs(y) are in [0, 1]

        This isn't a true normalize function since the x and y values are 
        constrained to integers, but it reduces the vector such that it's in 
        either the UNIT_VECTORS or DIAG_VECTORS sets. 
        """
        return vector(
            self._x // abs(self._x) if self._x else 0, 
            self._y // abs(self._y) if self._y else 0
        )

    
    @property
    def diagonals(self):
        if len(self._diagonals) == 0:
            self._diagonals = set([self + uv for uv in vector.DIAG_VECTORS()])
        return self._diagonals

    def __add__(self, other):
        return vector(self._x + other._x, self._y + other._y)
    
    def __sub__(self, other):
        return vector(self._x - other._x, self._y - other._y)
    
    def __mul__(self, scalar:int):
        return vector(self._x * scalar, self._y * scalar)
    
    def __eq__(self, other):
        is_vector = isinstance(other, vector)
        return is_vector and self._x == other._x and self._y == other._y
    
    def __str__(self) -> str:
        return f"({self._x}, {self._y})"
    
    def __repr__(self) -> str:
        return f"({self._x}, {self._y})"
    
    def __hash__(self) -> int:
        return hash((self._x, self._y))
    
    @staticmethod
    def UP():
        if vector._UP is None:
            vector._UP = vector(0, -1)
        return vector._UP
    
    @staticmethod
    def RIGHT():
        if vector._RIGHT is None:
            vector._RIGHT = vector(1, 0)
        return vector._RIGHT
    
    @staticmethod
    def DOWN():
        if vector._DOWN is None:
            vector._DOWN = vector(0, 1)
        return vector._DOWN
    
    @staticmethod
    def LEFT():
        if vector._LEFT is None:
            vector._LEFT = vector(-1, 0)
        return vector._LEFT
    
    @staticmethod
    def UNIT_VECTORS():
        if vector._UNIT_VECTORS is None:
            vector._UNIT_VECTORS = [
                vector.UP(), 
                vector.RIGHT(), 
                vector.DOWN(), 
                vector.LEFT()
            ]
        return vector._UNIT_VECTORS.copy()
    
    @staticmethod
    def DIAG_VECTORS():
        if vector._DIAG_VECTORS is None:
            vector._DIAG_VECTORS = [
                vector.UP() + vector.RIGHT(), 
                vector.DOWN() + vector.RIGHT(), 
                vector.DOWN() + vector.LEFT(), 
                vector.UP() + vector.LEFT(), 
            ]
        return vector._DIAG_VECTORS.copy()
    
    @staticmethod
    def LOOKUP_UDLR():
        """A dict of unit vectors keyed to the characters U, D, L, R"""
        return {
            "U": vector.UP(), 
            "D": vector.DOWN(), 
            "L": vector.LEFT(),
            "R": vector.RIGHT()
        }

    @staticmethod
    def LOOKUP_NESW():
        """A dict of unit vectors keyed to the characters N, E, S, W"""
        return {
            "N": vector.UP(), 
            "E": vector.RIGHT(),
            "S": vector.DOWN(), 
            "W": vector.LEFT()
        }