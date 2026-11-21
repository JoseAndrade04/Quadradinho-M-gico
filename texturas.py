"""Texturas em PNG e detalhes desenhados com Pygame, sem alterar a geometria da fase.

Implementação desenvolvida com auxílio do ChatGPT.
"""

from functools import lru_cache
import pygame


@lru_cache(maxsize=None)
def imagem_original(nome):
    """Carrega cada PNG uma única vez após pygame.display.set_mode."""
    from pathlib import Path

    caminho = Path(__file__).resolve().parent / "assets" / "texturas" / nome
    return pygame.image.load(str(caminho)).convert_alpha()


@lru_cache(maxsize=None)
def piso(tamanho, variante):
    """Ajusta a imagem ao bloco, sem suavizar os pixels."""
    return pygame.transform.scale(imagem_original("piso.png"), (tamanho, tamanho))


@lru_cache(maxsize=None)
def mesa(largura, altura):
    """Tampo liso e um caderno: poucas cores e nenhum veio de madeira."""
    arte = pygame.Surface((largura, altura))
    arte.fill((44, 42, 46))
    pygame.draw.rect(arte, (191, 154, 111), (3, 3, largura - 6, altura - 6))
    livro = pygame.Rect(largura - 17, 9, 9, min(15, altura - 15))
    pygame.draw.rect(arte, (92, 31, 40), livro)
    pygame.draw.rect(arte, (184, 37, 52), livro.inflate(-2, -2))
    # Lombada escura e páginas claras distinguem o caderno do tampo.
    pygame.draw.line(
        arte,
        (92, 31, 40),
        (livro.left + 2, livro.top + 1),
        (livro.left + 2, livro.bottom - 2),
        1,
    )
    pygame.draw.line(
        arte,
        (242, 226, 194),
        (livro.left + 3, livro.bottom - 2),
        (livro.right - 2, livro.bottom - 2),
        1,
    )
    return arte


def desenhar_mesas(tela, blocos):
    """Une o desenho dos blocos vizinhos sem modificar seus retângulos."""
    for origem, imagem in camada_mesas(tuple(tuple(b) for b in blocos)):
        tela.blit(imagem, origem)


@lru_cache(maxsize=None)
def camada_mesas(blocos):
    """Prepara uma imagem para cada grupo de blocos contíguos de mesa.

    O desenho é recortado pelos blocos originais para respeitar formatos
    irregulares. O resultado fica em cache e não altera as colisões.
    """
    pendentes = set(blocos)
    desenhos = []
    while pendentes:
        primeiro = pendentes.pop()
        grupo = [pygame.Rect(primeiro)]
        fila = [primeiro]
        while fila:
            x, y, w, h = fila.pop()
            for vizinho in (
                (x - w, y, w, h),
                (x + w, y, w, h),
                (x, y - h, w, h),
                (x, y + h, w, h),
            ):
                if vizinho in pendentes:
                    pendentes.remove(vizinho)
                    fila.append(vizinho)
                    grupo.append(pygame.Rect(vizinho))
        limite = grupo[0].unionall(grupo)
        arte = mesa(limite.width, limite.height)
        imagem = pygame.Surface(limite.size, pygame.SRCALPHA)
        # Recorta o desenho nos blocos existentes, inclusive em formatos irregulares.
        for bloco in grupo:
            local = bloco.move(-limite.x, -limite.y)
            imagem.blit(arte, local, local)
        desenhos.append((limite.topleft, imagem))
    return desenhos


@lru_cache(maxsize=None)
def moeda(raio):
    """Moeda arcade com três cores chapadas, mantendo o raio original."""
    arte = pygame.Surface((raio * 2 + 1, raio * 2 + 1), pygame.SRCALPHA)
    pygame.draw.circle(arte, (48, 39, 25), (raio, raio), raio)
    pygame.draw.circle(arte, (250, 199, 42), (raio, raio), raio - 2)
    pygame.draw.line(arte, (183, 121, 21), (raio, raio - 3), (raio, raio + 3), 2)
    return arte


def desenhar_saidas(tela, blocos):
    """Desenha cada saída contínua; os blocos de vitória não são alterados."""
    for origem, imagem in camada_saidas(tuple(tuple(b) for b in blocos)):
        tela.blit(imagem, origem)


@lru_cache(maxsize=None)
def camada_saidas(blocos):
    """Prepara uma imagem por área conectada de saída apenas uma vez."""
    pendentes = set(blocos)
    imagens = []
    while pendentes:
        primeiro = pendentes.pop()
        grupo = {primeiro}
        fila = [primeiro]
        while fila:
            x, y, w, h = fila.pop()
            for vizinho in (
                (x - w, y, w, h),
                (x + w, y, w, h),
                (x, y - h, w, h),
                (x, y + h, w, h),
            ):
                if vizinho in pendentes:
                    pendentes.remove(vizinho)
                    grupo.add(vizinho)
                    fila.append(vizinho)
        retangulos = [pygame.Rect(b) for b in grupo]
        limite = retangulos[0].unionall(retangulos)
        imagem = pygame.Surface(limite.size, pygame.SRCALPHA)
        for x, y, w, h in grupo:
            local = pygame.Rect(x - limite.x, y - limite.y, w, h)
            pygame.draw.rect(imagem, (53, 147, 77), local)
            # Desenha bordas apenas onde não há outro bloco de saída.
            for vizinho, inicio, fim in (
                (
                    (x - w, y, w, h),
                    (local.left + 1, local.top),
                    (local.left + 1, local.bottom),
                ),
                (
                    (x + w, y, w, h),
                    (local.right - 2, local.top),
                    (local.right - 2, local.bottom),
                ),
                (
                    (x, y - h, w, h),
                    (local.left, local.top + 1),
                    (local.right, local.top + 1),
                ),
                (
                    (x, y + h, w, h),
                    (local.left, local.bottom - 2),
                    (local.right, local.bottom - 2),
                ),
            ):
                if vizinho not in grupo:
                    pygame.draw.line(imagem, (207, 241, 194), inicio, fim, 2)
        imagens.append((limite.topleft, imagem))
    return imagens


@lru_cache(maxsize=None)
def estudante(largura, altura):
    """Estudante quadrado desenhado em uma grade simples de 24 pixels."""
    arte = pygame.Surface((24, 24), pygame.SRCALPHA)
    escuro = (40, 35, 40)
    pygame.draw.rect(arte, escuro, (0, 0, 24, 24))
    pygame.draw.rect(arte, (211, 157, 112), (3, 5, 18, 10))
    pygame.draw.rect(arte, (80, 49, 37), (2, 2, 20, 5))
    pygame.draw.rect(arte, (80, 49, 37), (3, 6, 5, 3))
    pygame.draw.rect(arte, escuro, (7, 10, 2, 2))
    pygame.draw.rect(arte, escuro, (15, 10, 2, 2))
    pygame.draw.rect(arte, (185, 27, 47), (2, 15, 20, 7))
    pygame.draw.rect(arte, escuro, (5, 15, 2, 7))
    pygame.draw.rect(arte, escuro, (17, 15, 2, 7))
    return pygame.transform.scale(arte, (largura, altura))


@lru_cache(maxsize=None)
def puff(largura, altura, ativo):
    """Almofada de descanso; só a cor muda quando o checkpoint é salvo."""
    arte = pygame.Surface((30, 30), pygame.SRCALPHA)
    borda = (39, 54, 58)
    tecido = (77, 145, 163) if not ativo else (73, 165, 98)
    claro = (127, 187, 196) if not ativo else (131, 203, 143)
    escuro = (54, 108, 125) if not ativo else (46, 120, 68)
    pygame.draw.rect(arte, borda, (0, 0, 30, 30), border_radius=7)
    pygame.draw.rect(arte, escuro, (2, 2, 26, 26), border_radius=6)
    pygame.draw.rect(arte, tecido, (2, 2, 26, 23), border_radius=6)
    pygame.draw.line(arte, claro, (7, 5), (22, 5), 2)
    # Costura simples: indica um assento macio sem acrescentar ruído visual.
    pygame.draw.line(arte, escuro, (7, 19), (11, 22), 1)
    pygame.draw.line(arte, escuro, (18, 22), (22, 19), 1)
    return pygame.transform.scale(arte, (largura, altura))
