import pygame
import cv2
from model.cell import *
from data.generator import generate_random_vectors_and_temps
from model.particle import *
from typing import List
SIMULATION_START = pygame.USEREVENT + 1 # start simulation
SIMULATION_END = pygame.USEREVENT + 2 # end simulation
SIMULATION_IN_PROGRESS = False
class Visualizer:

    def __init__(self):
        self.window = None
        self.obraz = None
        self.woda = None
        self.cells = None
        self.particles = []

    def get_cells(self):
        return self.cells
    def get_particles(self):
        return self.particles

    def initialize_water(self):
        woda = cv2.imread('images/water.png', cv2.IMREAD_GRAYSCALE)
        woda_ = woda > 200
        self.woda = woda_
        return


    def initialize(self, map, width, height):
        self.initialize_water()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("map")
        self.obraz = pygame.image.load(map)
        # p1 = Particle(450, 342)
        # self.obraz.set_at((x + i, y + j), (0, 0, 0))
        self.window.blit(self.obraz, (0, 0))
        self.cells = generate_random_vectors_and_temps(create_cells(width, height))
        for cell in self.cells:
            print(cell)
        pygame.display.update()

    def session(self):
        gra = True
        drawing = False
        global SIMULATION_IN_PROGRESS

        while gra:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gra = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         if not SIMULATION_IN_PROGRESS: #FALSE
                #             pygame.event.post(pygame.event.post(SIMULATION_START))
                #         else: # TRUE
                #             pygame.event.post(pygame.event.post(SIMULATION_END))
                #         SIMULATION_IN_PROGRESS = not SIMULATION_IN_PROGRESS


            if drawing:
                x, y = pygame.mouse.get_pos()
                if self.valid_coords(x, y) and self.woda[y, x]:
                    p = Particle(x,y)
                    if p not in self.particles:
                        self.particles.append(p)
                        print(self.particles)
                        for coord in p.get_coords_of_particle():
                                self.obraz.set_at((coord[0], coord[1]), (0, 0, 0))

            self.update()

    def valid_coords(self, x, y):
        return 0 <= x < 800 and 0 <= y < 600

    def update(self):
        self.window.blit(self.obraz, (0, 0))
        pygame.display.update()
