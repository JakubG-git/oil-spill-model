from model.cell import Cell
import math
class Particle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 3  # Size of the particle
        self.isActive = True
        self.isDead = False

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __repr__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    

    def get_current_cell(self, vis) -> Cell:
        index = math.floor(self.x / 2) + (420 * math.floor(self.y / 2))
        return vis.get_cells()[index]

    def get_coords_of_particle(self) -> list:
        coords = []
        for i in range(-2, 2):
            for j in range(-2, 2):
                coords.append((int(self.x + i), int(self.y + j)))
        return coords