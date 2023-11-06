import pygame

pygame.init()

szerokosc = 800
wysokosc = 600
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("mapa")

obraz = pygame.image.load("obraz.png")

mapa_pikseli = []
for y in range(wysokosc):
    wiersz = []
    for x in range(szerokosc):
        kolor = obraz.get_at((x, y))
        wiersz.append(kolor)
    mapa_pikseli.append(wiersz)
# print(mapa_pikseli)

gra = True
while gra:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            obraz.set_at((x, y), (0,0,0))

    okno.blit(obraz, (0, 0))
    pygame.display.update()
