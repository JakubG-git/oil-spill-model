from model.cell import Cell
import math
class Particle:

    def __init__(self, x, y, density=2):
        self.x = x
        self.y = y
        self.size = 3  # Size of the particle
        self.density = 2
        self.isActive = True
        self.isDead = False

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __repr__(self):
        return f"X: {self.x}, Y: {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_density(self):
        return self.density

    def get_current_cell(self, vis) -> Cell:
        index = math.floor(self.x / 2) + (420 * math.floor(self.y / 2))
        try:
            current_cell = vis.get_cells()[index]
        except:
            current_cell = vis.get_cells()[index % len(vis.get_cells())]
        # print(current_cell)
        return current_cell

    def get_coords_of_particle(self) -> list:
        coords = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                coords.append((int(self.x + i), int(self.y + j)))
        return coords
    
    def get_color(self):
        # get color based on density in grayscale
        r = int(255 - (255 * self.density)) % 255
        g = int(255 - (255 * self.density)) % 255
        b = int(255 - (255 * self.density)) % 255
        if r > 100:
            self.isActive = False
        return (r, g, b)
        