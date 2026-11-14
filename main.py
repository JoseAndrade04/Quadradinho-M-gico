import pygame
from jogador import Jogador
from fases import Fase

pygame.init()


LARGURA = 900

ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadradinho Mágico")


relogio = pygame.time.Clock()
fase=Fase()
jogador=Jogador(fase.inicio[0], fase.inicio[1])
rodando = True

while rodando:
    dt = min(relogio.tick(60)/1000, 0.05)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    teclas=pygame.key.get_pressed()
    jogador.mover(teclas, dt, fase.paredes)
    jogador.limitar_na_tela(tela)

    
    tela.fill((180, 180, 255))
    fase.desenhar(tela)
    jogador.desenhar(tela)



    
    pygame.display.flip()

    


pygame.quit()
