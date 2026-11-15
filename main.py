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
mortes=0
fonte=pygame.font.Font(None,36)
venceu=False
rodando = True

while rodando:
    dt = min(relogio.tick(60) / 1000, 0.05)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and venceu:
                fase = Fase()
                jogador = Jogador(
                    fase.inicio[0], fase.inicio[1]
                )

                mortes = 0
                venceu = False
    if not venceu:
        teclas = pygame.key.get_pressed()
        jogador.mover(teclas, dt, fase.paredes)
        jogador.limitar_na_tela(tela)
        fase.atualizar(dt)
        for obstaculo in fase.obstaculos:
            if jogador.encostou_obstaculo(obstaculo):
                mortes += 1
                jogador.voltar_ao_inicio(fase.inicio)
                fase.reiniciar_moedas()
                break

        fase.coletar_moedas(jogador.rect)

        if fase.foi_concluida(jogador.rect):
            venceu = True
    tela.fill((180, 180, 255))
    fase.desenhar(tela)
    jogador.desenhar(tela)

    # Mostra as mortes.
    texto_mortes = fonte.render(
        f"Mortes: {mortes}", True, (0, 0, 0)
    )
    tela.blit(texto_mortes, (20, 20))
    coletadas = 0
    for moeda in fase.moedas:
        if moeda.coletada:
            coletadas += 1
    texto_moedas = fonte.render(
        f"Moedas: {coletadas}/{len(fase.moedas)}",
        True,
        (0, 0, 0),
    )
    tela.blit(texto_moedas, (20, 60))
    if venceu:
        mensagem = fonte.render(
            "Fase concluída!", True, (0, 0, 0)
        )
        posicao_mensagem = mensagem.get_rect(
            center=(LARGURA // 2, 110)
        )
        tela.blit(mensagem, posicao_mensagem)
    if venceu:
        mensagem = fonte.render(
            "Fase concluída!", True, (0, 0, 0)
        )
        posicao_mensagem = mensagem.get_rect(
            center=(LARGURA // 2, 110)
        )
        tela.blit(mensagem, posicao_mensagem)

        instrucao = fonte.render(
            "Pressione R para jogar novamente",
            True,
            (0, 0, 0),
        )
        posicao_instrucao = instrucao.get_rect(
            center=(LARGURA // 2, 500)
        )
        tela.blit(instrucao, posicao_instrucao)
    pygame.display.flip()

pygame.quit()
