import pygame
import cv2
from model.cell import *
from data.generator import *
from model.particle import *
from applicator.applicator import *
import os
from copy import copy

SIMULATION_START = pygame.USEREVENT + 1  # start simulation
SIMULATION_END = pygame.USEREVENT + 2  # end simulation
DISPLAY = pygame.display.set_mode((840, 720))
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
        woda = cv2.imread('images/binarized.png', cv2.IMREAD_GRAYSCALE)
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
        self.cells = set_vectors_and_temps(create_cells(width, height))
        # Zapis pliku tekstowego z info o cellach i wyświetlanie ich
        # path = os.path.join("data", "cells.txt")
        # with open(path, 'w') as file:
        #     for cell in self.cells:
        #         file.write(str(cell) + "\n")

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
                        # sleep 0.3s
                        pygame.time.delay(50)
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
                    p = Particle(x, y)
                    if p not in self.particles:
                        self.particles.append(p)
                        print(self.particles)
                        for coord in p.get_coords_of_particle():
                            self.obraz.set_at((coord[0], coord[1]), (0, 0, 0))

            self.update()

    def valid_coords(self, x, y):
        return 0 <= x < 840 and 0 <= y < 720

    def draw_cells(self):
        for cell in self.cells:
            pygame.draw.rect(self.obraz, (128, 128, 128), (cell.x, cell.y, cell.size, cell.size), 1)

    def update(self):
        pygame.display.update()
        self.window.blit(self.obraz, (0, 0))

    def update_particle(self, particle: Particle):
        rgb = particle.get_color()
        for coord in particle.get_coords_of_particle():
            if self.valid_coords(coord[0], coord[1]) and self.woda[coord[1], coord[0]]:
                self.obraz.set_at((coord[0], coord[1]), rgb)
            elif self.valid_coords(coord[0], coord[1]) and not self.woda[coord[1], coord[0]]:
                particle.isActive = False
            elif not self.valid_coords(coord[0], coord[1]):
                particle.isDead = True
        if particle.isDead:
            self.particles.remove(particle)
