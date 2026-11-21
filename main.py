"""Inicializa o jogo e controla eventos, telas e a atualização da partida."""

import pygame
from jogador import Jogador
from fases import Fase, TOTAL_FASES
from interface import Interface
from sons import Sons

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Insper's Hardest Game")
relogio = pygame.time.Clock()

numero_fase = 1
fase = Fase(numero_fase)
jogador = Jogador(fase.inicio[0], fase.inicio[1])

mortes = 0

venceu = False

interface = Interface()
sons = Sons()
# Guarda a tela para retomar a mesma partida ao sair do menu.
tela_retorno = "apresentacao"
tela_atual = "menu"
inicio_apresentacao = 0
duracao_apresentacao = 2000  # Milissegundos: 2 segundos.

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
        acao_vitoria = None
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if tela_atual == "menu":
                if interface.botoes_menu["jogar"].collidepoint(evento.pos):
                    tela_atual = tela_retorno
                    inicio_apresentacao = pygame.time.get_ticks()
                elif interface.botoes_menu["instrucoes"].collidepoint(evento.pos):
                    tela_atual = "instrucoes"
            elif tela_atual in ("jogo", "apresentacao"):
                if interface.botao_menu_hud.collidepoint(evento.pos):
                    tela_retorno = tela_atual
                    tela_atual = "menu"

            elif tela_atual == "vitoria":
                for acao, retangulo in interface.botoes_vitoria.items():
                    if retangulo.collidepoint(evento.pos):
                        acao_vitoria = acao
                        break

        elif evento.type == pygame.KEYDOWN:
            if tela_atual == "menu":
                if evento.key == pygame.K_RETURN:
                    tela_atual = tela_retorno
                    inicio_apresentacao = pygame.time.get_ticks()

                elif evento.key == pygame.K_i:
                    tela_atual = "instrucoes"

            elif tela_atual == "instrucoes":
                if evento.key == pygame.K_ESCAPE:
                    tela_atual = "menu"

            elif tela_atual == "apresentacao":
                if evento.key == pygame.K_ESCAPE:
                    tela_retorno = "apresentacao"
                    tela_atual = "menu"

            elif tela_atual == "jogo":
                if evento.key == pygame.K_ESCAPE:
                    tela_retorno = "jogo"
                    tela_atual = "menu"

            elif tela_atual == "vitoria":
                if evento.key in (pygame.K_RETURN, pygame.K_r):
                    acao_vitoria = "reiniciar"
                elif evento.key == pygame.K_ESCAPE:
                    acao_vitoria = "menu"

        if acao_vitoria is not None:
            # As duas opções encerram a partida concluída e preparam uma nova.
            numero_fase = 1
            fase = Fase(numero_fase)
            jogador = Jogador(*fase.inicio)
            mortes = 0
            venceu = False
            tela_retorno = "apresentacao"
            tela_atual = "apresentacao" if acao_vitoria == "reiniciar" else "menu"
            inicio_apresentacao = pygame.time.get_ticks()

    if not rodando:
        break

    sons.atualizar_tela(tela_atual)

    if tela_atual == "menu":
        interface.desenhar_menu(tela, continuar=(tela_retorno == "jogo"))
        pygame.display.flip()
        continue

    if tela_atual == "instrucoes":
        interface.desenhar_instrucoes(tela)
        pygame.display.flip()
        continue

    if tela_atual == "apresentacao":
        tempo_passado = pygame.time.get_ticks() - inicio_apresentacao
        progresso = min(tempo_passado / duracao_apresentacao, 1)

        interface.desenhar_apresentacao(
            tela,
            numero_fase,
            TOTAL_FASES,
            fase.nome,
            frases_fases.get(numero_fase, ["Prepare-se!"]),
            progresso,
            mortes=mortes,
        )
        pygame.display.flip()

        if tempo_passado >= duracao_apresentacao:
            tela_atual = "jogo"

        continue

    if tela_atual == "vitoria":
        interface.desenhar_vitoria(tela, mortes, TOTAL_FASES)
        pygame.display.flip()
        continue

    if not venceu:
        # O cenário continua em movimento mesmo durante a animação de morte.
        fase.atualizar(dt)

        if jogador.morto:
            if jogador.atualizar_morte(dt, fase.ponto_retorno):
                fase.reiniciar_moedas()
        else:
            teclas = pygame.key.get_pressed()
            jogador.mover(teclas, dt, fase.paredes)
            jogador.limitar_na_tela(tela)

            for obstaculo in fase.obstaculos:
                if not fase.esta_em_area_segura(
                    jogador.rect
                ) and jogador.encostou_obstaculo(obstaculo):
                    mortes += 1
                    jogador.iniciar_morte()
                    sons.tocar_morte()
                    break

            # Um personagem morto não coleta, ativa checkpoints nem termina fases.
            if not jogador.morto:
                coletadas_antes = sum(moeda.coletada for moeda in fase.moedas)
                fase.coletar_moedas(jogador.rect)
                coletadas_depois = sum(moeda.coletada for moeda in fase.moedas)
                for _ in range(coletadas_depois - coletadas_antes):
                    sons.tocar_moeda()
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
                        tela_atual = "vitoria"
                        continue

    tela.fill((240, 240, 243))
    fase.desenhar(tela)
    jogador.desenhar(tela)

    coletadas = sum(moeda.coletada for moeda in fase.moedas)
    interface.desenhar_hud(
        tela,
        numero_fase,
        TOTAL_FASES,
        mortes,
        coletadas,
        len(fase.moedas),
    )

    pygame.display.flip()

sons.encerrar()
pygame.quit()
