class hexvec:
    """Half-baked implementation of vectors for hexagonal grids."""

    _NOEA = None
    _EAST = None
    _SOEA = None
    _SOWE = None
    _WEST = None
    _NOWE = None
    _UNIT_VECTORS = None
    
    def __init__(self, x:int=0, y:int=0, z:int=0) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._adjacents = []

    # TODO: What's the equivalent of manhattan distance for hexvecs? 
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    @property
    def adjacents(self):
        if len(self._adjacents) == 0:
            self._adjacents = [self + uv for uv in hexvec.UNIT_VECTORS()]
        return self._adjacents
    
    # TODO: Rotations. CCW, CW

    def __add__(self, other):
        return hexvec(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return hexvec(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar:int):
        return hexvec(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    @staticmethod
    def NOEA():
        if hexvec._NOEA is None:
            hexvec._NOEA = hexvec( 1,  0, -1)
        return hexvec._NOEA
    
    @staticmethod
    def EAST():
        if hexvec._EAST is None:
            hexvec._EAST = hexvec( 1, -1,  0)
        return hexvec._EAST
    
    @staticmethod
    def SOEA():
        if hexvec._SOEA is None:
            hexvec._SOEA = hexvec( 0, -1,  1)
        return hexvec._SOEA
    
    @staticmethod
    def SOWE():
        if hexvec._SOWE is None:
            hexvec._SOWE = hexvec(-1,  0,  1)
        return hexvec._SOWE
    
    @staticmethod
    def WEST():
        if hexvec._WEST is None:
            hexvec._WEST = hexvec(-1,  1,  0)
        return hexvec._WEST
    
    @staticmethod
    def NOWE():
        if hexvec._NOWE is None:
            hexvec._NOWE = hexvec( 0,  1, -1)
        return hexvec._NOWE
    
    @staticmethod
    def UNIT_VECTORS():
        if hexvec._UNIT_VECTORS is None:
            hexvec._UNIT_VECTORS = [
                hexvec.NOEA(), 
                hexvec.EAST(), 
                hexvec.SOEA(), 
                hexvec.SOWE(),
                hexvec.WEST(),
                hexvec.NOWE()
            ]
        return hexvec._UNIT_VECTORS.copy()
