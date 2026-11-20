import pygame


class Interface:

    def __init__(self):
        self.fonte_titulo = pygame.font.Font(None, 64)
        self.fonte_texto = pygame.font.Font(None, 32)

    def texto_centralizado(self, tela, texto, y, titulo=False):
        if titulo:
            fonte = self.fonte_titulo
        else:
            fonte = self.fonte_texto

        cor=(200,16,46) if titulo else (45,45,52)
        imagem = fonte.render(texto, True, cor)
        posicao = imagem.get_rect(
            center=(tela.get_width() // 2, y)
        )
        tela.blit(imagem, posicao)

    def desenhar_menu(self, tela):
        tela.fill((240, 240, 243))

        self.texto_centralizado(
            tela, "INSPER'S HARDEST GAME", 180, titulo=True
        )
        self.texto_centralizado(
            tela, "ENTER — Começar", 300
        )
        self.texto_centralizado(
            tela, "I — Instruções", 350
        )

    def desenhar_instrucoes(self, tela):
        tela.fill((240, 240, 243))

        self.texto_centralizado(
            tela, "Como jogar", 100, titulo=True
        )

        linhas = [
            "Use as setas ou WASD para se movimentar.",
            "Desvie dos círculos azuis.",
            "Colete todas as moedas amarelas.",
            "Entre na saída verde após coletar as moedas.",
            "Ao morrer, as moedas da fase reaparecem.",
            "ESC — Voltar ao menu",
        ]

        for indice, texto in enumerate(linhas):
            self.texto_centralizado(
                tela, texto, 210 + indice * 45
            )