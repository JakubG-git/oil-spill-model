import pygame
from model.field import *


class Visualizer:

    def __init__(self):
        self.window = None
        self.obraz = None

    def initialize(self, map, width, height):
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("map")
        self.obraz = pygame.image.load(map)
        self.window.blit(self.obraz, (0, 0))
        fields_list = create_fields(width, height)
        for e in fields_list:
            print(e)
        pygame.display.update()

    def session(self):
        gra = True
        while gra:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gra = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.obraz.set_at((x, y), (0, 0, 0))
            self.update()

    def update(self):
        self.window.blit(self.obraz, (0, 0))
        pygame.display.update()

# for y in range(0, wysokosc_mapy, rozmiar_kratki):
#     for x in range(0, szerokosc_mapy, rozmiar_kratki):
#         kratka = Kratka(x, y, rozmiar_kratki)
#         kwadraty.append(kratka)
