import pygame
import cv2
from model.cell import *
from data.generator import generate_random_vectors_and_temps
from model.particle import *
from applicator.applicator import *
from typing import List
from copy import copy
import matplotlib.pyplot as plt
import numpy as np
SIMULATION_START = pygame.USEREVENT + 1 # start simulation
SIMULATION_END = pygame.USEREVENT + 2 # end simulation
DISPLAY = pygame.display.set_mode((800, 600))
SIMULATION_IN_PROGRESS = False
class Visualizer:
    def __init__(self):
        self.window = None
        self.original_obraz = None
        self.obraz = None
        self.woda = None
        self.cells = None
        self.particles = []

    def get_cells(self):
        return self.cells
    def get_particles(self):
        return self.particles

    def initialize_display(self):
        pygame.init()


    def initialize_water(self):
        woda = cv2.imread('images/water.png', cv2.IMREAD_GRAYSCALE)
        woda_ = woda > 200
        self.woda = woda_
        return


    def initialize(self, map, width, height):
        pygame.init()
        self.initialize_water()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("map")
        self.obraz = pygame.image.load(map)
        self.original_obraz = pygame.image.load(map)
        self.window.blit(self.obraz, (0, 0))
        self.cells = generate_random_vectors_and_temps(create_cells(width, height))
        # self.generate_arrow_image()
        for cell in self.cells:
            print(cell)
        pygame.display.update()

    def session(self):
        main_loop = True
        drawing = False
        global SIMULATION_IN_PROGRESS
        global SIMULATION_START
        global SIMULATION_END


        while main_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not SIMULATION_IN_PROGRESS: #FALSE
                            pygame.event.post(pygame.event.Event(SIMULATION_START))
                        SIMULATION_IN_PROGRESS = not SIMULATION_IN_PROGRESS
                elif event.type == SIMULATION_START:
                    print("Simulation starting")
                    while SIMULATION_IN_PROGRESS:
                        self.obraz = copy(self.original_obraz)
                        move_particles(self)
                        #sleep 1 second
                        pygame.time.delay(500)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                main_loop = False
                                SIMULATION_IN_PROGRESS = not SIMULATION_IN_PROGRESS
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    print("Simulation paused")
                                    SIMULATION_IN_PROGRESS = not SIMULATION_IN_PROGRESS 
                elif event.type == SIMULATION_END:
                    print("Simulation ending")
                    



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


    def draw_cells(self):
        for cell in self.cells:
            pygame.draw.rect(self.obraz, (128, 128, 128), (cell.x, cell.y, cell.size, cell.size), 1)

    def update(self):
        pygame.display.update()
        self.draw_cells()
        self.window.blit(self.obraz, (0, 0))

    def update_particle(self, particle: Particle):
        for coord in particle.get_coords_of_particle():
            if self.valid_coords(coord[0], coord[1]) and self.woda[coord[1], coord[0]]:
                self.obraz.set_at((coord[0], coord[1]), (0, 0, 0))
            elif self.valid_coords(coord[0], coord[1]) and not self.woda[coord[1], coord[0]]:
                particle.isActive = False
            elif not self.valid_coords(coord[0], coord[1]):
                particle.isDead = True
        if particle.isDead:
            self.particles.remove(particle)
            
    # def generate_arrow_image(self):
    #     arrow_image = np.zeros((600, 800, 3), dtype=np.uint8)
    #     arrow_length = 20

    #     for cell in self.cells:
    #         center_x = cell.x + cell.size // 2
    #         center_y = cell.y + cell.size // 2

    #         advection_vector = cell.get_advection_vector()  # Assume you have a method to get advection vector in Cell class

    #         if advection_vector:
    #             # Normalize the vector and scale it to arrow_length
    #             normalized_vector = advection_vector / np.linalg.norm(advection_vector)
    #             arrow_end_x = int(center_x + normalized_vector[0] * arrow_length)
    #             arrow_end_y = int(center_y + normalized_vector[1] * arrow_length)

    #             pygame.draw.line(arrow_image, (255, 0, 0), (center_x, center_y), (arrow_end_x, arrow_end_y), 2)
    #             pygame.draw.polygon(arrow_image, (255, 0, 0), [(arrow_end_x, arrow_end_y - 5),
    #                                                            (arrow_end_x - 5, arrow_end_y + 5),
    #                                                            (arrow_end_x + 5, arrow_end_y + 5)])

    #     pygame.image.save(pygame.surfarray.make_surface(arrow_image), 'arrows.png')
