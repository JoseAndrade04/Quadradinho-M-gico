"""Controla movimento, colisões e animação de morte do estudante."""

import pygame
import texturas


class Jogador:
    """Representa o estudante e mantém sua posição e seu estado de vida."""

    def __init__(self, x, y):
        """Cria o estudante em (x, y), com colisão de 24 × 24 pixels."""
        self.rect = pygame.Rect(x, y, 24, 24)
        self.posicao = pygame.Vector2(x, y)
        self.cor = (200, 16, 46)
        self.velocidade = 220
        self.morto = False
        self.tempo_morte = 0
        self.duracao_morte = 400  # Milissegundos.

    def desenhar(self, tela):
        """Pisca em vermelho durante a morte; fora dela usa o desenho normal."""
        imagem = texturas.estudante(*self.rect.size)
        if self.morto:
            if self.tempo_morte >= 320 or (int(self.tempo_morte) // 80) % 2:
                return
            imagem = imagem.copy()
            imagem.fill((255, 65, 65), special_flags=pygame.BLEND_RGB_MULT)
        tela.blit(imagem, self.rect)

    def iniciar_morte(self):
        """Inicia a animação uma única vez para cada colisão fatal."""
        self.morto = True
        self.tempo_morte = 0

    def atualizar_morte(self, dt, ponto_retorno):
        """Retorna True no quadro em que renasce, sem bloquear os eventos."""
        self.tempo_morte += dt * 1000
        if self.tempo_morte >= self.duracao_morte:
            self.voltar_ao_inicio(ponto_retorno)
            self.morto = False
            self.tempo_morte = 0
            return True
        return False

    def mover(self, teclas, dt, paredes):
        """Move pelas teclas pressionadas, respeitando as paredes.

        dt é o tempo do quadro em segundos. A direção é normalizada para
        manter a mesma velocidade ao andar na diagonal. As colisões são
        resolvidas separadamente nos eixos x e y.
        """
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
        """Mantém o estudante dentro da tela e sincroniza sua posição."""
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
        """Retorna se o retângulo do estudante toca o círculo do obstáculo.

        Usa o ponto do retângulo mais próximo ao centro do círculo para
        comparar a distância ao quadrado com o raio ao quadrado.
        """
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
        """Reposiciona o estudante no início ou no checkpoint informado."""
        self.posicao = pygame.Vector2(inicio[0], inicio[1])
        self.rect.topleft = (
            round(self.posicao.x),
            round(self.posicao.y),
        )
