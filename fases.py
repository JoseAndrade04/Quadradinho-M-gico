"""Transforma mapas em objetos e aplica as regras de cada fase."""

import pygame
import texturas
import math

from mapas import (
    FASES,
    TOTAL_FASES,
    TAMANHO_BLOCO,
    ORIGEM_MAPA,
)


class Fase:
    """Reúne cenário, objetos, áreas seguras e regras de uma fase."""

    def __init__(self, numero=1):
        """Carrega a fase pelo número, começando em 1, e prepara seus objetos."""
        dados = FASES[numero - 1]

        self.nome = dados["nome"]
        self.mapa = dados["mapa"]

        self.paredes = []
        self.mesas = []
        self.chao = []
        self.areas_verdes = []
        self.chegadas = []
        self.moedas = []
        self.obstaculos = []
        self.checkpoints = []
        self.checkpoint_ativo = None

        self.inicio = None

        self.ler_mapa()

        self.ponto_retorno = self.inicio
        self.moedas_salvas = [False for moeda in self.moedas]

        for configuracao in dados["obstaculos"]:
            self.obstaculos.append(Obstaculo(configuracao))

    def ler_mapa(self):
        """Converte os símbolos do mapa em retângulos e objetos do jogo.

        A posição de cada bloco considera a origem do mapa e o tamanho
        definido em mapas.py. Mesas também entram na lista de paredes.
        """
        origem_x, origem_y = ORIGEM_MAPA

        for linha, texto in enumerate(self.mapa):
            for coluna, simbolo in enumerate(texto):
                x = origem_x + coluna * TAMANHO_BLOCO
                y = origem_y + linha * TAMANHO_BLOCO

                bloco = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

                if simbolo == "D":
                    self.paredes.append(bloco)
                    self.mesas.append(bloco)
                    continue

                if simbolo in "# ":
                    self.paredes.append(bloco)
                    continue

                cor = (245, 245, 245)

                if (linha + coluna) % 2 == 1:
                    cor = (225, 225, 230)

                self.chao.append((bloco, cor))

                if simbolo in "GSFC":
                    self.areas_verdes.append(bloco)

                if simbolo == "S":
                    self.inicio = (
                        bloco.centerx - 12,
                        bloco.centery - 12,
                    )

                elif simbolo == "F":
                    self.chegadas.append(bloco)

                elif simbolo == "M":
                    self.moedas.append(Moeda(bloco.centerx, bloco.centery))

                elif simbolo == "C":
                    self.checkpoints.append(bloco)

    def atualizar(self, dt):
        """Avança os obstáculos usando dt, o tempo do quadro em segundos."""
        for obstaculo in self.obstaculos:
            obstaculo.atualizar(dt)

    def desenhar(self, tela):
        """Desenha cenário e objetos sem modificar a geometria das colisões."""
        for bloco, cor in self.chao:
            # Troca só o desenho do piso; o retângulo continua igual.
            variante = (bloco.x // TAMANHO_BLOCO + bloco.y // TAMANHO_BLOCO) % 2
            tela.blit(texturas.piso(TAMANHO_BLOCO, variante), bloco)

        for bloco in self.areas_verdes:
            pygame.draw.rect(tela, (170, 235, 170), bloco)

        texturas.desenhar_saidas(tela, self.chegadas)

        for bloco in self.checkpoints:
            arte = texturas.puff(
                bloco.width, bloco.height, bloco == self.checkpoint_ativo
            )
            tela.blit(arte, bloco)

        # Agrupa apenas o desenho dos blocos contíguos da mesma mesa.
        texturas.desenhar_mesas(tela, self.mesas)

        for moeda in self.moedas:
            moeda.desenhar(tela)

        for obstaculo in self.obstaculos:
            obstaculo.desenhar(tela)

        self.desenhar_contorno(tela)

    def desenhar_contorno(self, tela):
        """Desenha apenas as bordas dos caminhos em contato com paredes e mesas."""
        origem_x, origem_y = ORIGEM_MAPA
        espessura = 5
        preto = (43, 43, 49)

        caminhos = set()

        for linha, texto in enumerate(self.mapa):
            for coluna, simbolo in enumerate(texto):
                if simbolo not in "# D ":
                    caminhos.add((coluna, linha))

        for coluna, linha in caminhos:
            x = origem_x + coluna * TAMANHO_BLOCO
            y = origem_y + linha * TAMANHO_BLOCO

            direita = x + TAMANHO_BLOCO
            base = y + TAMANHO_BLOCO

            if (coluna, linha - 1) not in caminhos:
                self.linha_contorno(tela, (x, y), (direita, y), espessura)

            if (coluna, linha + 1) not in caminhos:
                self.linha_contorno(tela, (x, base), (direita, base), espessura)

            if (coluna - 1, linha) not in caminhos:
                self.linha_contorno(tela, (x, y), (x, base), espessura)

            if (coluna + 1, linha) not in caminhos:
                self.linha_contorno(tela, (direita, y), (direita, base), espessura)

    def linha_contorno(self, tela, inicio, fim, espessura):
        """Desenha uma borda com pontas preenchidas para unir os cantos."""
        preto = (43, 43, 49)

        pygame.draw.line(tela, preto, inicio, fim, espessura)

        for x, y in (inicio, fim):
            ponta = pygame.Rect(
                x - espessura // 2,
                y - espessura // 2,
                espessura,
                espessura,
            )
            pygame.draw.rect(tela, preto, ponta)

    def coletar_moedas(self, jogador_rect):
        """Verifica se o estudante encostou em cada moeda ainda disponível."""
        for moeda in self.moedas:
            moeda.tentar_coletar(jogador_rect)

    def reiniciar_moedas(self):
        """Restaura as moedas ao estado salvo no último checkpoint.

        Antes do primeiro checkpoint, todas as moedas voltam ao cenário.
        Depois dele, as moedas já salvas continuam coletadas.
        """
        for indice, moeda in enumerate(self.moedas):
            moeda.coletada = self.moedas_salvas[indice]

    def foi_concluida(self, jogador_rect):
        """Retorna se todas as moedas foram coletadas e o jogador chegou.

        O retângulo inteiro do estudante deve estar dentro da união dos
        blocos de saída; apenas encostar na borda não conclui a fase.
        """
        for moeda in self.moedas:
            if not moeda.coletada:
                return False

        area_na_chegada = 0

        for bloco in self.chegadas:
            intersecao = jogador_rect.clip(bloco)
            area_na_chegada += intersecao.width * intersecao.height

        area_jogador = jogador_rect.width * jogador_rect.height

        return area_na_chegada == area_jogador

    def verificar_checkpoints(self, jogador_rect):
        """Salva o retorno e as moedas quando o estudante ocupa um checkpoint.

        A ativação exige o retângulo inteiro do estudante dentro do bloco.
        """
        for bloco in self.checkpoints:
            if bloco.contains(jogador_rect):
                self.checkpoint_ativo = bloco

                self.ponto_retorno = (
                    bloco.centerx - jogador_rect.width // 2,
                    bloco.centery - jogador_rect.height // 2,
                )

                self.moedas_salvas = [moeda.coletada for moeda in self.moedas]

                break

    def esta_em_area_segura(self, jogador_rect):
        """Retorna se o estudante está inteiramente coberto por blocos seguros."""
        area_segura = 0

        for bloco in self.areas_verdes:
            intersecao = jogador_rect.clip(bloco)
            area_segura += intersecao.width * intersecao.height

        area_jogador = jogador_rect.width * jogador_rect.height

        return area_segura == area_jogador


class Obstaculo:
    """Representa uma bola com movimento horizontal, vertical ou circular."""

    def __init__(self, dados):
        """Converte a configuração em blocos para posições e limites em pixels."""
        origem_x, origem_y = ORIGEM_MAPA

        self.tipo = dados["tipo"]

        self.raio = 11

        if self.tipo == "circular":
            self.centro = pygame.Vector2(
                origem_x + (dados["coluna_centro"] + 0.5) * TAMANHO_BLOCO,
                origem_y + (dados["linha_centro"] + 0.5) * TAMANHO_BLOCO,
            )

            self.raio_orbita = dados["raio_orbita"] * TAMANHO_BLOCO

            self.angulo = math.radians(dados["angulo"])

            self.velocidade_angular = math.radians(dados["velocidade_angular"])

            self.posicao = pygame.Vector2()
            self.atualizar_posicao_circular()

        else:
            self.posicao = pygame.Vector2(
                origem_x + (dados["coluna"] + 0.5) * TAMANHO_BLOCO,
                origem_y + (dados["linha"] + 0.5) * TAMANHO_BLOCO,
            )

            self.velocidade = dados["velocidade"]
            self.direcao = dados["sentido"]

            if self.tipo == "horizontal":
                origem = origem_x
            else:
                origem = origem_y

            self.limite_inicial = (
                origem + (dados["limite_inicial"] + 0.5) * TAMANHO_BLOCO
            )

            self.limite_final = origem + (dados["limite_final"] + 0.5) * TAMANHO_BLOCO

    def atualizar_posicao_circular(self):
        """Calcula a posição da órbita usando o ângulo atual em radianos."""
        self.posicao.x = self.centro.x + self.raio_orbita * math.cos(self.angulo)

        self.posicao.y = self.centro.y + self.raio_orbita * math.sin(self.angulo)

    def atualizar(self, dt):
        """Avança a órbita ou o percurso linear usando dt em segundos."""
        if self.tipo == "circular":
            self.angulo += self.velocidade_angular * dt
            self.angulo %= 2 * math.pi

            self.atualizar_posicao_circular()

        else:
            deslocamento = self.velocidade * self.direcao * dt

            if self.tipo == "horizontal":
                self.posicao.x += deslocamento
                valor = self.posicao.x
            else:
                self.posicao.y += deslocamento
                valor = self.posicao.y

            if valor >= self.limite_final:
                valor = self.limite_final
                self.direcao = -1

            elif valor <= self.limite_inicial:
                valor = self.limite_inicial
                self.direcao = 1

            if self.tipo == "horizontal":
                self.posicao.x = valor
            else:
                self.posicao.y = valor

    def desenhar(self, tela):
        """Desenha a bola azul com o mesmo centro e raio usados nas colisões."""
        centro = (
            round(self.posicao.x),
            round(self.posicao.y),
        )

        pygame.draw.circle(tela, (0, 0, 255), centro, self.raio)

        pygame.draw.circle(tela, (0, 0, 0), centro, self.raio, 3)


class Moeda:
    """Representa uma atividade coletável e registra se já foi recolhida."""

    def __init__(self, x, y):
        """Cria uma moeda de raio 8 com centro em (x, y)."""
        self.posicao = pygame.Vector2(x, y)
        self.raio = 8
        self.coletada = False

    def tentar_coletar(self, jogador_rect):
        """Marca a moeda como coletada quando seu círculo toca o jogador."""
        if self.coletada:
            return
        ponto_x = max(jogador_rect.left, min(self.posicao.x, jogador_rect.right))
        ponto_y = max(jogador_rect.top, min(self.posicao.y, jogador_rect.bottom))

        distancia_x = self.posicao.x - ponto_x
        distancia_y = self.posicao.y - ponto_y

        if distancia_x**2 + distancia_y**2 <= self.raio**2:
            self.coletada = True

    def desenhar(self, tela):
        """Desenha a moeda arcade somente enquanto ela não foi coletada."""
        if not self.coletada:
            centro = (round(self.posicao.x), round(self.posicao.y))
            imagem = texturas.moeda(self.raio)
            tela.blit(imagem, imagem.get_rect(center=centro))
