import pygame


pygame.init()


LARGURA = 900

ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadradinho Mágico")


relogio = pygame.time.Clock()

rodando = True

while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    
    tela.fill((180, 180, 255))

    
    pygame.display.flip()

    
    relogio.tick(60)


pygame.quit()
