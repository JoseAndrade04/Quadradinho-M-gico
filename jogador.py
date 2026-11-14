import pygame

class Jogador:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.cor = (255, 0, 0)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)