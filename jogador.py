import pygame

class Jogador:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.posicao = pygame.Vector2(x, y)
        self.cor = (255, 0, 0)
        self.velocidade = 240
        

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        pygame.draw.rect(tela, (0, 0, 0), self.rect, 3)

        def mover(self, teclas, dt):
        
        direcao = pygame.Vector2(0, 0)

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direcao.x -= 1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direcao.x += 1

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direcao.y -= 1

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direcao.y += 1

        if direcao.length_squared() > 0:
            direcao = direcao.normalize()

        self.posicao += direcao * self.velocidade * dt

        self.rect.topleft = (
            round(self.posicao.x),
            round(self.posicao.y),
        )