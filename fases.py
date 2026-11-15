import pygame

class Fase:
    def __init__(self):
        self.paredes=[pygame.Rect(50,150,800,20), pygame.Rect(50,430,800,20),pygame.Rect(50,150,20,300),pygame.Rect(830,150,20,300)]
        self.area_inicial= pygame.Rect(70,170,120,260)
        self.area_final= pygame.Rect(710,170,120,260)
        self.inicio = (100,300)
        self.obstaculos=[Obstaculo(300,300,220,680),]
        self.moedas=[Moeda(350,230),Moeda(550,370),]

    def atualizar(self,dt):
        for obstaculo in self.obstaculos:
            obstaculo.atualizar(dt)

    def desenhar(self,tela):
        pygame.draw.rect(tela,(240,240,255), (70,170,760,260))
        pygame.draw.rect(tela,(170,255,170),self.area_inicial)
        pygame.draw.rect(tela,(170,255,170),self.area_final)

        for parede in self.paredes:
            pygame.draw.rect(tela,(0,0,0),parede)

        for moeda in self.moedas:
            moeda.desenhar(tela)

        for obstaculo in self.obstaculos:
            obstaculo.desenhar(tela)

    def coletar_moedas(self,jogador_rect):
        for moeda in self.moedas:
            moeda.tentar_coletar(jogador_rect)

    def reniciar_moedas(self):
        for moeda in self.moedas:
            moeda.coletada=False

    def foi_concluida(self,jogador_rect):
        for moeda in self.moedas:
            if not moeda.coletada:
                return False

        return self.area_final.contains(jogador_rect)

class Obstaculo:
    def __init__(self,x,y,limite_esquerdo,limite_direito):
        self.posicao=pygame.Vector2(x,y)
        self.raio=10
        self.velocidade=180
        self.direcao=1

        self.limite_esquerdo=limite_esquerdo
        self.limite_direito=limite_direito

    def atualizar(self,dt):
        self.posicao.x+= self.velocidade * self.direcao * dt

        if self.posicao.x >= self.limite_direito:
            self.posicao.x= self.limite_direito
            self.direcao=-1

        elif self.posicao.x<=self.limite_esquerdo:
            self.posicao.x=self.limite_esquerdo
            self.direcao=1

    def desenhar(self,tela):
        centro=(round(self.posicao.x),round(self.posicao.y),)
        pygame.draw.circle(tela,(0,0,255),centro,self.raio)
        pygame.draw.circle(tela,(0,0,0),centro,self.raio,3)

class Moeda:
    def __init__(self,x,y):
        self.posicao= pygame.Vector2(x,y)
        self.raio=8
        self.coletada=False

    def tentar_coletar(self,jogador_rect):
        if self.coletada:
            return
        ponto_x=max(jogador_rect.left,min(self.posicao.x,jogador_rect.right))
        ponto_y=max(jogador_rect.top,min(self.posicao.y,jogador_rect.bottom))

        distancia_x= self.posicao.x-ponto_x
        distancia_y= self.posicao.y-ponto_y

        if distancia_x**2 + distancia_y**2 <= self.raio**2:
            self.coletada=True

    def desenhar(self,tela):
        if not self.coletada:
            centro=(round(self.posicao.x),round(self.posicao.y),)

            pygame.draw.circle(tela,(255,220,0),centro,self.raio)
            pygame.draw.circle(tela,(0,0,0,0),centro,self.raio,2)