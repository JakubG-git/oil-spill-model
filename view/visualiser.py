import pygame
import cv2
from model.cell import *
from data.generator import generate_random_vectors_and_temps
from model.particle import *
from applicator.applicator import *
from typing import List
from copy import copy
main_loop_START = pygame.USEREVENT + 1 # start main_loop
main_loop_END = pygame.USEREVENT + 2 # end main_loop
main_loop_IN_PROGRESS = False
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
        woda = cv2.imread('images/water.png', cv2.IMREAD_main_loopYSCALE)
        woda_ = woda > 200
        self.woda = woda_
        return


    def initialize(self, map, width, height):
        self.initialize_water()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("map")
        self.obraz = pygame.image.load(map)
        self.original_obraz = pygame.image.load(map)
        self.window.blit(self.obraz, (0, 0))
        self.cells = generate_random_vectors_and_temps(create_cells(width, height))
        for cell in self.cells:
            print(cell)
        pygame.display.update()
        pygame.event.pump()

    def session(self):
        main_loop = True
        drawing = False
        global main_loop_IN_PROGRESS
        global main_loop_START
        global main_loop_END


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
                        if not main_loop_IN_PROGRESS: #FALSE
                            pygame.event.post(pygame.event.Event(main_loop_START))
                        main_loop_IN_PROGRESS = not main_loop_IN_PROGRESS
                elif event.type == main_loop_START:
                    print("main_loop starting")
                    while main_loop_IN_PROGRESS:
                        self.obraz = copy(self.original_obraz)
                        move_particles(self)
                        #sleep 1 second
                        # pygame.time.delay(1000)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                main_loop = False
                                main_loop_IN_PROGRESS = not main_loop_IN_PROGRESS
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    print("main_loop paused")
                                    main_loop_IN_PROGRESS = not main_loop_IN_PROGRESS

                        
                        

                    
                elif event.type == main_loop_END:
                    print("main_loop ending")
                    



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
        pygame.display.update()
        self.window.blit(self.obraz, (0, 0))

    def update_particle(self, particle: Particle):
        for coord in particle.get_coords_of_particle():
            if self.valid_coords(coord[0], coord[1]):
                self.obraz.set_at((coord[0], coord[1]), (0, 0, 0))
