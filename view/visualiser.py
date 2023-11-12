import pygame
import cv2
from model.field import *


class Visualizer:

    def __init__(self):
        self.window = None
        self.obraz = None
        self.woda = None

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
        self.window.blit(self.obraz, (0, 0))
        # fields_list = create_fields(width, height)
        # for e in fields_list:
        #     print(e)
        pygame.display.update()

    def session(self):
        gra = True
        drawing = False

        while gra:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gra = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False

            if drawing:
                x, y = pygame.mouse.get_pos()
                for i in range(-2, 2):
                    for j in range(-2, 2):
                        if self.valid_coords(x + i, y + j) and self.woda[y + j, x + i]:
                            self.obraz.set_at((x + i, y + j), (0, 0, 0))

            self.update()

    def valid_coords(self, x, y):
        return 0 <= x < 800 and 0 <= y < 600

    def update(self):
        self.window.blit(self.obraz, (0, 0))
        pygame.display.update()
