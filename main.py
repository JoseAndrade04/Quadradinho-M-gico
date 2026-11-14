import pygame
from jogador import Jogador

pygame.init()


LARGURA = 900

ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadradinho Mágico")


relogio = pygame.time.Clock()
jogador=Jogador(100,300)
rodando = True

while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    
    tela.fill((180, 180, 255))
    jogador.desenhar(tela)


    
    pygame.display.flip()

    
    relogio.tick(60)


pygame.quit()
