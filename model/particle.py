from model.cell import Cell

class Particle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 3  # Size of the particle (adjust as needed)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __repr__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move_with_wind(self, vis):
        # Find the cell the particle is in
        current_cell = self.get_current_cell(vis)

        # Move the particle based on the wind vector of the cell
        if current_cell and current_cell.wind_vector:
            self.x = (self.x + int(current_cell.wind_vector[0])) % 800
            self.y = (self.y + int(current_cell.wind_vector[1])) % 600

    def get_current_cell(self, vis) -> Cell:
        for cell in vis.get_cells():
            if cell.x <= self.x <= cell.x + cell.size and cell.y <= self.y <= cell.y + cell.size:
                return cell
        return None

    def get_coords_of_particle(self) -> list:
        coords = []
        for i in range(-2, 2):
            for j in range(-2, 2):
                coords.append((self.x + i, self.y + j))
        return coords