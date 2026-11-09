class BoardModel:
    """
    Generic 4D model of a board as a linear int array with tensor representation of the content
    """
    def empty_array(self)->list[int]:
        return [0 for _ in range(0, self._size_x * self._size_y * self._size_z * self._size_t)]
        
    def initial_array(self):
        self._array = self.empty_array()
        

    def __init__(self, size_x, size_y, size_z, size_t):
        self._size_x = size_x
        self._size_y = size_y
        self._size_z = size_z
        self._size_t = size_t
        self._array = self._initial_array()
        
