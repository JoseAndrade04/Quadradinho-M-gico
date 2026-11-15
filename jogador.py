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

    def mover(self, teclas, dt, paredes):

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

        self.posicao.x += direcao.x * self.velocidade * dt
        self.rect.x = round(self.posicao.x)

        for parede in paredes:
            if self.rect.colliderect(parede):
                if direcao.x > 0:
                    self.rect.right = parede.left
                elif direcao.x < 0:
                    self.rect.left = parede.right

                self.posicao.x = self.rect.x

        self.posicao.y += direcao.y * self.velocidade * dt
        self.rect.y = round(self.posicao.y)

        for parede in paredes:
            if self.rect.colliderect(parede):
                if direcao.y > 0:
                    self.rect.bottom = parede.top
                elif direcao.y < 0:
                    self.rect.top = parede.bottom

                self.posicao.y = self.rect.y

    def limitar_na_tela(self, tela):
    
        limites = tela.get_rect()

        if self.posicao.x < limites.left:
            self.posicao.x = limites.left

        if self.posicao.x > limites.right - self.rect.width:
            self.posicao.x = limites.right - self.rect.width

        if self.posicao.y < limites.top:
            self.posicao.y = limites.top

        if self.posicao.y > limites.bottom - self.rect.height:
            self.posicao.y = limites.bottom - self.rect.height

        self.rect.topleft = (
            round(self.posicao.x),
            round(self.posicao.y),
        )

    def encostou_obstaculo(self, obstaculo):

        ponto_x = max(
            self.rect.left,
            min(obstaculo.posicao.x, self.rect.right),
        )
        ponto_y = max(
            self.rect.top,
            min(obstaculo.posicao.y, self.rect.bottom),
        )

        distancia_x = obstaculo.posicao.x - ponto_x
        distancia_y = obstaculo.posicao.y - ponto_y

        distancia_quadrado = distancia_x**2 + distancia_y**2

        return distancia_quadrado <= obstaculo.raio**2

    def voltar_ao_inicio(self, inicio):

        self.posicao = pygame.Vector2(inicio[0], inicio[1])
        self.rect.topleft = (
            round(self.posicao.x),
            round(self.posicao.y),
        )

    