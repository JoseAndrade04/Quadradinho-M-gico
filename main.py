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
inicio_apresentacao = 0
duracao_apresentacao = 2000  # Milissegundos: 3 segundos.

frases_fases = {
    1: ["Cada enxadada uma minhoca"],
    2: ["APS chegando"],
    3: ["O professor disse que essa era fácil."],
    4: ["Pode entrar. Sua paz fica do lado de fora."],
    5: ["Terminar o Praire Learn era melhor"],
    6: ["Não leva a mochila"],
    7: ["Coloca o EPI"],
    8: ["Esse jogo foi mais fácil do que pegar DP"],
}
rodando = True

while rodando:
    dt = min(relogio.tick(60) / 1000, 0.05)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            if tela_atual == "menu":
                if evento.key == pygame.K_RETURN:
                    tela_atual = "apresentacao"
                    inicio_apresentacao = pygame.time.get_ticks()

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
                    tela_atual = "apresentacao"
                    inicio_apresentacao = pygame.time.get_ticks()

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

    if tela_atual == "apresentacao":
        tela.fill((240, 240, 243))

        interface.texto_centralizado(
            tela,
            f"FASE {numero_fase}",
            150,
            titulo=True,
        )

        interface.texto_centralizado(
            tela,
            fase.nome,
            220,
        )

        frases = frases_fases.get(
            numero_fase,
            ["Prepare-se!"],
        )

        for indice, frase in enumerate(frases):
            interface.texto_centralizado(
                tela,
                frase,
                300 + indice * 40,
            )

        pygame.display.flip()

        tempo_passado = (
            pygame.time.get_ticks() - inicio_apresentacao
        )

        if tempo_passado >= duracao_apresentacao:
            tela_atual = "jogo"

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
                numero_fase += 1
                fase = Fase(numero_fase)
                jogador.voltar_ao_inicio(fase.inicio)

                tela_atual = "apresentacao"
                inicio_apresentacao = pygame.time.get_ticks()
                continue
            else:
                venceu = True

    tela.fill((240, 240, 243))
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
    texto_fase = interface.fonte_texto.render(
    f"Sala {numero_fase}/{TOTAL_FASES}: {fase.nome}",
    True,
    (200, 16, 46),
    )

    posicao_fase = texto_fase.get_rect(
    topright=(LARGURA - 20, 20)
    )

    tela.blit(texto_fase, posicao_fase)

    

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
