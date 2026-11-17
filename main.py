import pygame
from jogador import Jogador
from fases import Fase, TOTAL_FASES
from interface import Interface

pygame.init()


LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadradinho Mágico")
relogio = pygame.time.Clock()

numero_fase=1
fase=Fase(numero_fase)
jogador=Jogador(fase.inicio[0], fase.inicio[1])

mortes=0
fonte=pygame.font.Font(None,36)

venceu=False

interface = Interface()
tela_atual = "menu"

rodando = True

while rodando:
    dt = min(relogio.tick(60) / 1000, 0.05)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            if tela_atual == "menu":
                if evento.key == pygame.K_RETURN:
                    tela_atual = "jogo"

                elif evento.key == pygame.K_i:
                    tela_atual = "instrucoes"

            elif tela_atual == "instrucoes":
                if evento.key == pygame.K_ESCAPE:
                    tela_atual = "menu"

            elif tela_atual == "jogo":
                if evento.key == pygame.K_r and venceu:
                    numero_fase = 1
                    fase = Fase(numero_fase)

                    jogador = Jogador(
                        fase.inicio[0], fase.inicio[1]
                    )

                    mortes = 0
                    venceu = False

    if not rodando:
        break

    if tela_atual == "menu":
        interface.desenhar_menu(tela)
        pygame.display.flip()
        continue

    if tela_atual == "instrucoes":
        interface.desenhar_instrucoes(tela)
        pygame.display.flip()
        continue

    if not venceu:
        teclas = pygame.key.get_pressed()
        jogador.mover(teclas, dt, fase.paredes)
        jogador.limitar_na_tela(tela)
        fase.atualizar(dt)
        
        for obstaculo in fase.obstaculos:
    
            if (
                not fase.esta_em_area_segura(jogador.rect)
                and jogador.encostou_obstaculo(obstaculo)
            ):
                mortes += 1

                jogador.voltar_ao_inicio(
                    fase.ponto_retorno
                )

                fase.reiniciar_moedas()
                break
        
        fase.coletar_moedas(jogador.rect)
        fase.verificar_checkpoints(jogador.rect)

        if fase.foi_concluida(jogador.rect):
            if numero_fase < TOTAL_FASES:
                numero_fase+=1
                fase=Fase(numero_fase)
                jogador.voltar_ao_inicio(fase.inicio)
            else:
                venceu=True

    tela.fill((180, 180, 255))
    fase.desenhar(tela)
    jogador.desenhar(tela)

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
