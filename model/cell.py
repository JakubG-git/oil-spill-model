class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 2
        self.wind_vector = None
        self.water_vector = None
        self.water_temp = None

    def set_vectors_n_temp(self, wind_vec: (float, float), water_vec: (float, float), water_tmp: float):
        self.water_temp = water_tmp
        self.wind_vector = wind_vec
        self.water_vector = water_vec

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Wind: {self.wind_vector}, Current: {self.water_vector}, Temp: {self.water_temp}"


def create_cells(width, height) -> list[Cell]:
    return [Cell(x * 2, y * 2) for y in range(height // 2) for x in range(width // 2)]

