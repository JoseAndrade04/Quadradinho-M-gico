"""Controla as músicas e os efeitos sem bloquear a atualização do jogo.

Áudio desenvolvido com auxílio do ChatGPT.
"""

from pathlib import Path

import pygame

# Valores de 0.0 (silêncio) até 1.0 (volume máximo).
VOLUME_MENU = 0.30
VOLUME_FASES = 0.28
VOLUME_VITORIA = 0.40
VOLUME_MORTE = 0.70
VOLUME_TRANSICAO = 0.65
VOLUME_MOEDA = 0.80


class Sons:
    """Reutiliza efeitos e troca a música apenas ao mudar de tela."""

    def __init__(self):
        """Carrega os efeitos uma vez, após a inicialização do Pygame."""
        self.pasta = Path(__file__).resolve().parent / "assets" / "sons"
        self.morte = pygame.mixer.Sound(str(self.pasta / "morte.wav"))
        self.transicao = pygame.mixer.Sound(str(self.pasta / "transicao.wav"))
        self.moeda = pygame.mixer.Sound(str(self.pasta / "moeda.wav"))
        self.morte.set_volume(VOLUME_MORTE)
        self.transicao.set_volume(VOLUME_TRANSICAO)
        self.moeda.set_volume(VOLUME_MOEDA)

        # Reserva dois canais; moedas usam os demais sem cortar esses efeitos.
        pygame.mixer.set_reserved(2)
        self.canal_morte = pygame.mixer.Channel(0)
        self.canal_transicao = pygame.mixer.Channel(1)
        self.tela_anterior = None
        self.musica_atual = None

    def atualizar_tela(self, tela):
        """Escolhe o áudio de cada tela, sem reiniciar a música a cada quadro."""
        if tela == self.tela_anterior:
            return
        self.tela_anterior = tela

        # Interrompe o efeito da apresentação ao sair dela, inclusive com Esc.
        self.canal_transicao.stop()
        if tela != "jogo":
            self.canal_morte.stop()

        if tela == "apresentacao":
            pygame.mixer.music.stop()
            self.musica_atual = None
            self.canal_transicao.play(self.transicao)
        elif tela == "jogo":
            self.tocar_musica("fases.ogg", VOLUME_FASES)
        elif tela == "vitoria":
            self.tocar_musica("vitoria.ogg", VOLUME_VITORIA, repetir=True)
        else:
            # Menu e instruções compartilham a mesma música sem reiniciá-la.
            self.tocar_musica("menu.ogg", VOLUME_MENU)

    def tocar_musica(self, arquivo, volume, repetir=True):
        """Reproduz uma faixa nova; repetir=True ativa a repetição contínua."""
        if arquivo == self.musica_atual:
            return
        pygame.mixer.music.load(str(self.pasta / arquivo))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1 if repetir else 0)
        self.musica_atual = arquivo

    def tocar_morte(self):
        """Toca um Wilhelm por morte, substituindo outro grito ainda em curso."""
        self.canal_morte.play(self.morte)

    def tocar_moeda(self):
        """Toca um plim somente quando uma nova moeda é coletada."""
        self.moeda.play()

    def encerrar(self):
        """Encerra músicas e efeitos antes de fechar o Pygame."""
        pygame.mixer.music.stop()
        self.canal_morte.stop()
        self.canal_transicao.stop()
        self.moeda.stop()
