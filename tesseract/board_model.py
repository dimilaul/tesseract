class BoardModel:
    """
    Generic 4D model of a board as a linear int array with tensor representation of the content
    """
    def empty_array(self)->list[int]:
        return [0 for _ in range(0, self._size_x * self._size_y * self._size_z * self._size_t)]
        
    def _initialize_array(self)->None:
        self._array = self.empty_array()
        
    def __init__(self, size_x, size_y, size_z, size_t):
        self._size_x = size_x
        self._size_y = size_y
        self._size_z = size_z
        self._size_t = size_t
        self._initialize_array()
        
    def position_to_coordinates(self, position: int)->tuple[int, int, int, int]:
        return (position // 8, position % 8 // 4, position % 4 // 2, position % 2)

    def coordinates_to_position(self, x: int, y: int, z: int, t: int)->int:
        return x * 8 + y * 4 + z * 2 + t

    def set_cell(self, x, y, z, t, value):
        position = self.coordinates_to_position(x, y, z, t)
        self._array[position] = value
        
    def get_cell(self, x, y, z, t)->int:
        position = self.coordinates_to_position(x, y, z, t)
        return self._array[position]
        
