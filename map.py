import pygame

pygame.init()

szerokosc = 800
wysokosc = 600
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("mapa")

obraz = pygame.image.load("obraz.jpg")

mapa_pikseli = []
for y in range(wysokosc):
    wiersz = []
    for x in range(szerokosc):
        kolor = obraz.get_at((x, y))
        wiersz.append(kolor)
    mapa_pikseli.append(wiersz)
print(mapa_pikseli)

gra = True
while gra:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra = False

        # Obsługa zdarzeń użytkownika, np. kliknięcia myszy

    # Aktualizacja ekranu
    for y in range(wysokosc):
        for x in range(szerokosc):
            pygame.draw.rect(okno, mapa_pikseli[y][x], (x, y, 1, 1))

    pygame.display.update()
