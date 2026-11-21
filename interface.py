"""Desenha menus, instruções, apresentações, HUD e a tela de vitória."""

import pygame
from pathlib import Path


class Interface:
    """Concentra o desenho das telas e os retângulos dos botões."""

    def __init__(self):
        """Carrega imagens e fontes e prepara os botões reutilizados nas telas."""
        self.fonte_titulo = pygame.font.Font(None, 64)
        self.fonte_texto = pygame.font.Font(None, 32)

        # Artes geradas com auxílio do ChatGPT; carregadas só uma vez.
        pasta = Path(__file__).resolve().parent / "assets" / "imagens"
        fundo = pygame.image.load(str(pasta / "fundo_menu.png")).convert()
        self.fundo_menu = pygame.transform.scale(fundo, (900, 600))
        titulo = pygame.image.load(str(pasta / "titulo.png")).convert_alpha()
        largura = 800
        altura = round(titulo.get_height() * largura / titulo.get_width())
        self.titulo_menu = pygame.transform.scale(titulo, (largura, altura))
        self.fonte_opcoes = pygame.font.SysFont(
            "couriernew,dejavusansmono", 27, bold=True
        )
        self.fonte_rodape = pygame.font.SysFont(
            "couriernew,dejavusansmono", 14, bold=True
        )
        # Fonte pixelada incluída no projeto, sem instalação no Windows.
        fonte_pixel = (
            Path(__file__).resolve().parent
            / "assets"
            / "fontes"
            / "PressStart2P-Regular.ttf"
        )
        self.fontes_frases = [
            pygame.font.Font(str(fonte_pixel), tamanho) for tamanho in (40, 32, 24)
        ]
        self.pixel_grande = pygame.font.Font(str(fonte_pixel), 32)
        self.pixel_media = pygame.font.Font(str(fonte_pixel), 16)
        self.pixel_pequena = pygame.font.Font(str(fonte_pixel), 12)

        # Recursos da vitória são preparados uma única vez.
        self.pixel_vitoria = pygame.font.Font(str(fonte_pixel), 40)
        self.pixel_botoes = pygame.font.Font(str(fonte_pixel), 24)
        self.fundo_vitoria = self.fundo_menu.copy()
        escurecer = pygame.Surface((900, 600), pygame.SRCALPHA)
        escurecer.fill((4, 8, 23, 145))
        self.fundo_vitoria.blit(escurecer, (0, 0))
        self.botoes_vitoria = {
            "reiniciar": pygame.Rect(220, 395, 460, 52),
            "menu": pygame.Rect(220, 465, 460, 52),
        }

        self.botao_menu_hud = pygame.Rect(12, 0, 130, 44)

        self.botoes_menu = {
            "jogar": pygame.Rect(290, 390, 320, 50),
            "instrucoes": pygame.Rect(290, 454, 320, 50),
        }

    def texto_centralizado(self, tela, texto, y, titulo=False):
        """Centraliza um texto na altura y, usando a fonte comum ou a de título."""
        if titulo:
            fonte = self.fonte_titulo
        else:
            fonte = self.fonte_texto

        cor = (200, 16, 46) if titulo else (45, 45, 52)
        imagem = fonte.render(texto, True, cor)
        posicao = imagem.get_rect(center=(tela.get_width() // 2, y))
        tela.blit(imagem, posicao)

    def desenhar_menu(self, tela, continuar=False):
        """Mostra as artes em pixel art e as duas opções interativas."""
        tela.blit(self.fundo_menu, (0, 0))
        posicao = self.titulo_menu.get_rect(midtop=(450, 38))
        tela.blit(self.titulo_menu, posicao)

        mouse = pygame.mouse.get_pos()
        opcoes = (
            ("jogar", "CONTINUAR" if continuar else "JOGAR", "ENTER"),
            ("instrucoes", "COMO JOGAR", "I"),
        )

        for acao, rotulo, atalho in opcoes:
            retangulo = self.botoes_menu[acao]
            selecionado = retangulo.collidepoint(mouse)
            cor = (255, 222, 119) if selecionado else (255, 243, 212)
            pygame.draw.rect(tela, (10, 14, 30), retangulo.move(4, 4))
            pygame.draw.rect(tela, (25, 31, 53), retangulo)
            pygame.draw.rect(tela, cor, retangulo, 3)
            imagem = self.fonte_opcoes.render(rotulo, True, cor)
            tela.blit(imagem, imagem.get_rect(center=retangulo.center))
            tecla = self.fonte_rodape.render(atalho, True, cor)
            tela.blit(tecla, (retangulo.right + 14, retangulo.centery - 8))

        nomes = self.fonte_rodape.render(
            "BERNARDO / JOSÉ / GUILHERME", True, (255, 243, 212)
        )
        sombra = self.fonte_rodape.render(
            "BERNARDO / JOSÉ / GUILHERME", True, (7, 10, 22)
        )
        posicao = nomes.get_rect(center=(450, 573))
        tela.blit(sombra, posicao.move(2, 2))
        tela.blit(nomes, posicao)

    def desenhar_instrucoes(self, tela):
        """Apresenta controles, objetivos e o funcionamento dos checkpoints."""
        tela.fill((240, 240, 243))

        self.texto_centralizado(tela, "Como jogar", 100, titulo=True)

        linhas = [
            "Use as setas ou WASD para se movimentar.",
            "Desvie dos círculos azuis.",
            "Colete todas as moedas amarelas.",
            "Entre na saída verde após coletar as moedas.",
            "Ao morrer, moedas não salvas reaparecem.",
            "Puffs salvam seu retorno e as moedas coletadas.",
            "ESC — Voltar ao menu",
        ]

        for indice, texto in enumerate(linhas):
            self.texto_centralizado(tela, texto, 210 + indice * 45)

    def linhas_pixel(self, texto, fonte, largura):
        """Quebra frases nos espaços para respeitar a largura disponível."""
        linhas = []
        atual = ""
        for palavra in texto.split():
            tentativa = f"{atual} {palavra}".strip()
            if atual and fonte.size(tentativa)[0] > largura:
                linhas.append(atual)
                atual = palavra
            else:
                atual = tentativa
        if atual:
            linhas.append(atual)
        return linhas

    def pixel_centralizado(self, tela, texto, fonte, y, cor):
        """Desenha uma linha pixelada com sombra, sem suavização."""
        sombra = fonte.render(texto, False, (0, 0, 0))
        imagem = fonte.render(texto, False, cor)
        posicao = imagem.get_rect(center=(tela.get_width() // 2, y))
        tela.blit(sombra, posicao.move(3, 3))
        tela.blit(imagem, posicao)

    def desenhar_apresentacao(
        self, tela, numero, total, nome, frases, progresso, mortes=0
    ):
        """Mostra a mensagem central com fonte retrô e um cabeçalho simples.

        Nome e progresso mantêm a compatibilidade com a chamada anterior.
        Desenho desenvolvido com auxílio do ChatGPT.
        """
        largura, altura = tela.get_size()
        # Degradê lilás para branco, como na referência enviada.
        for y in range(altura):
            mistura = y / max(altura - 1, 1)
            cor = tuple(
                round(inicio + (255 - inicio) * mistura) for inicio in (215, 212, 252)
            )
            pygame.draw.line(tela, cor, (0, y), (largura - 1, y))

        self.desenhar_hud(tela, numero, total, mortes)

        # Prefere duas linhas grandes; frases maiores usam a próxima fonte.
        texto = " ".join(frases).upper()
        for fonte in self.fontes_frases:
            linhas = self.linhas_pixel(texto, fonte, largura - 100)
            if len(linhas) <= 2:
                break

        intervalo = fonte.get_linesize() + 22
        centro_y = (altura + 44) // 2
        inicio_y = centro_y - (len(linhas) - 1) * intervalo / 2
        for indice, linha in enumerate(linhas):
            imagem = fonte.render(linha, False, (15, 13, 23))
            posicao = imagem.get_rect(
                center=(largura // 2, round(inicio_y + indice * intervalo))
            )
            tela.blit(imagem, posicao)

    def desenhar_hud(self, tela, numero, total, mortes, coletadas=None, total_moedas=0):
        """Desenha a barra superior e a contagem de moedas abaixo dela."""
        largura = tela.get_width()
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, largura, 44))
        cor_menu = (
            (255, 222, 119)
            if self.botao_menu_hud.collidepoint(pygame.mouse.get_pos())
            else (255, 255, 255)
        )
        menu = self.pixel_media.render("MENU", False, cor_menu)
        fase = self.pixel_media.render(f"{numero}/{total}", False, (255, 255, 255))
        contador = self.pixel_media.render(f"MORTES: {mortes}", False, (255, 255, 255))
        tela.blit(menu, menu.get_rect(midleft=(24, 22)))
        tela.blit(fase, fase.get_rect(center=(largura // 2, 22)))
        tela.blit(contador, contador.get_rect(midright=(largura - 24, 22)))
        if coletadas is not None and total_moedas > 0:
            moedas = self.pixel_pequena.render(
                f"MOEDAS: {coletadas}/{total_moedas}", False, (30, 25, 40)
            )
            tela.blit(moedas, (24, 65))

    def desenhar_vitoria(self, tela, mortes, total_fases):
        """Mostra o resultado real e as opções após a última fase.

        Implementação desenvolvida com auxílio do ChatGPT.
        """
        import texturas

        tela.blit(self.fundo_vitoria, (0, 0))
        creme = (255, 243, 212)
        ouro = (255, 216, 99)
        self.pixel_centralizado(
            tela, "INSPER'S HARDEST GAME", self.pixel_pequena, 35, creme
        )
        self.pixel_centralizado(tela, "VOCÊ ESCAPOU", self.pixel_grande, 100, creme)
        self.pixel_centralizado(tela, "DO INSPER!", self.pixel_vitoria, 156, ouro)

        estudante = texturas.estudante(96, 96)
        tela.blit(estudante, estudante.get_rect(center=(450, 260)))
        self.pixel_centralizado(
            tela,
            f"FASES: {total_fases}/{total_fases}    MORTES: {mortes}",
            self.pixel_media,
            343,
            creme,
        )

        mouse = pygame.mouse.get_pos()
        for acao, rotulo in (
            ("reiniciar", "JOGAR NOVAMENTE"),
            ("menu", "VOLTAR AO MENU"),
        ):
            retangulo = self.botoes_vitoria[acao]
            cor = ouro if retangulo.collidepoint(mouse) else creme
            pygame.draw.rect(tela, (5, 7, 17), retangulo.move(4, 4))
            pygame.draw.rect(tela, (21, 25, 44), retangulo)
            pygame.draw.rect(tela, cor, retangulo, 2)
            texto = self.pixel_botoes.render(rotulo, False, cor)
            tela.blit(texto, texto.get_rect(center=retangulo.center))

        self.pixel_centralizado(
            tela, "ENTER / R: REINICIAR     ESC: MENU", self.pixel_pequena, 563, creme
        )
