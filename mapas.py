TAMANHO_BLOCO = 30
ORIGEM_MAPA = (0, 120)

# LEGENDA:
# # = parede
# D = mesa
# - = chão
# S = início
# G = área segura
# M = atividade/moeda
# C = checkpoint
# F = saída
#
# As cores continuam sendo definidas no arquivo fases.py.


# Esta função apenas evita repetir os mesmos campos
# na configuração de cada bola.
def bola(tipo, coluna, linha, inicio, fim, velocidade, sentido=1):
    return {
        "tipo": tipo,
        "coluna": coluna,
        "linha": linha,
        "limite_inicial": inicio,
        "limite_final": fim,
        "velocidade": velocidade,
        "sentido": sentido,
    }


FASES = [
    # =====================================================
    # FASE 1 — ATRAVESSAR NO MOMENTO CERTO
    #
    # As bolas percorrem corredores entre as mesas.
    # As atividades exigem sair da rota central.
    # =====================================================
    {
        "nome": "Sala 101 - Fora do horario",

        "mapa": [
            "##############################",
            "#----------------------------#",
            "#-------M------------M-------#",
            "#----DD----DD----DD----DD----#",
            "#----DD----DD----DD----DD----#",
            "#GGG----------------------FFF#",
            "#GSG----------------------FFF#",
            "#GGG----------------------FFF#",
            "#----------------------------#",
            "#----DD----DD----DD----DD----#",
            "#----DD----DD----DD----DD----#",
            "#-------M------------M-------#",
            "#----------------------------#",
            "#----------------------------#",
            "##############################",
        ],

        "obstaculos": [
            # tipo, coluna, linha, início, fim, velocidade, sentido

            # Corredores verticais entre as mesas.
            bola("vertical", 9, 2, 1, 13, 185, 1),
            bola("vertical", 14, 12, 1, 13, 185, -1),
            bola("vertical", 19, 2, 1, 13, 185, 1),
            bola("vertical", 25, 12, 1, 13, 185, -1),

            # Cruzamentos no centro da sala.
            bola("horizontal", 5, 5, 4, 25, 170, 1),
            bola("horizontal", 24, 8, 4, 25, 170, -1),
        ],
    },

    # =====================================================
    # FASE 2 — DUAS PASSAGENS OBRIGATÓRIAS
    #
    # Atravessar a primeira abertura, explorar o setor
    # central e alcançar a segunda abertura.
    # =====================================================
    {
        "nome": "Laboratorio - Entrega sob pressao",

        "mapa": [
            "##############################",
            "#GGG-------------------------#",
            "#GSG----------------------M--#",
            "#GGG--DD----------DD---------#",
            "#-----DD----------DD---------#",
            "##########----################",
            "#----------------------------#",
            "#--M-----------C----------M--#",
            "#-----DD----------DD---------#",
            "#-----DD----------DD---------#",
            "######################----####",
            "#FFF-------------------------#",
            "#FFF---------M---------------#",
            "#FFF-------------------------#",
            "##############################",
        ],

        "obstaculos": [
            # Primeiro setor.
            bola("horizontal", 8, 2, 4, 28, 195, 1),
            bola("vertical", 24, 4, 1, 4, 145, -1),

            # Guarda da primeira passagem.
            bola("horizontal", 10, 5, 10, 13, 125, 1),

            # Duas bolas em sentidos opostos.
            bola("horizontal", 4, 7, 1, 28, 185, 1),
            bola("horizontal", 25, 7, 1, 28, 185, -1),
            bola("vertical", 24, 6, 6, 9, 155, 1),

            # Guarda da segunda passagem.
            bola("horizontal", 25, 10, 22, 25, 135, -1),

            # Travessia final em etapas.
            bola("vertical", 20, 11, 11, 13, 115, 1),
            bola("vertical", 16, 13, 11, 13, 115, -1),
            bola("vertical", 10, 11, 11, 13, 115, 1),
            bola("vertical", 6, 13, 11, 13, 115, -1),
        ],
    },

    # =====================================================
    # FASE 3 — PERCURSO EM ZIGUE-ZAGUE
    #
    # As aberturas alternam entre direita e esquerda.
    # O checkpoint fica no meio do percurso.
    # =====================================================
    {
        "nome": "Corredores - Troca de sala",

        "mapa": [
            "##############################",
            "#GGG-------------------------#",
            "#GSG----------M--------------#",
            "#GGG-------------------------#",
            "########################---###",
            "#----------------------------#",
            "#----M------------------M----#",
            "#-------------C--------------#",
            "###---########################",
            "#----------------------------#",
            "#------------M---------------#",
            "#----------------------------#",
            "########################---###",
            "#FFF-------------------------#",
            "##############################",
        ],

        "obstaculos": [
            # Primeiro corredor: quatro barreiras móveis.
            bola("vertical", 8, 1, 1, 3, 110, 1),
            bola("vertical", 13, 3, 1, 3, 110, -1),
            bola("vertical", 18, 1, 1, 3, 110, 1),
            bola("vertical", 23, 3, 1, 3, 110, -1),

            # Primeira abertura: colunas 24 a 26.
            bola("horizontal", 24, 4, 24, 26, 95, 1),

            # Segundo corredor: sentidos alternados.
            bola("vertical", 8, 5, 5, 7, 120, 1),
            bola("vertical", 12, 7, 5, 7, 120, -1),
            bola("vertical", 19, 5, 5, 7, 120, 1),
            bola("vertical", 23, 7, 5, 7, 120, -1),

            # Segunda abertura: colunas 3 a 5.
            bola("horizontal", 5, 8, 3, 5, 100, -1),

            # Terceiro corredor.
            bola("vertical", 8, 9, 9, 11, 130, 1),
            bola("vertical", 13, 11, 9, 11, 130, -1),
            bola("vertical", 18, 9, 9, 11, 130, 1),
            bola("vertical", 23, 11, 9, 11, 130, -1),

            # Última abertura. O corredor de saída é livre.
            bola("horizontal", 24, 12, 24, 26, 105, 1),
        ],
    },

    # =====================================================
    # FASE 4 — BUSCAR E VOLTAR
    #
    # A saída fica perto da entrada, mas as atividades
    # estão nos setores inferiores. É preciso retornar.
    # =====================================================
    {
        "nome": "Biblioteca - Atividades pendentes",

        "mapa": [
            "##############################",
            "#GGG----------------------FFF#",
            "#GSG----------------------FFF#",
            "#GGG----------------------FFF#",
            "######---############---######",
            "#----------------------------#",
            "#----DD----DD----DD----DD----#",
            "#----DD----DD----DD----DD----#",
            "#--M----------C-----------M--#",
            "#----------------------------#",
            "##############---#############",
            "#----------------------------#",
            "#--M----------------------M--#",
            "#----------------------------#",
            "##############################",
        ],

        "obstaculos": [
            # Travessia superior.
            bola("vertical", 11, 1, 1, 3, 120, 1),
            bola("vertical", 17, 3, 1, 3, 120, -1),
            bola("vertical", 23, 1, 1, 3, 120, 1),

            # Duas entradas para a biblioteca.
            bola("horizontal", 6, 4, 6, 8, 105, 1),
            bola("horizontal", 23, 4, 21, 23, 105, -1),

            # Corredor acima das mesas.
            bola("horizontal", 3, 5, 1, 28, 210, 1),
            bola("horizontal", 26, 5, 1, 28, 210, -1),

            # Corredores entre as mesas.
            bola("vertical", 9, 5, 5, 9, 165, 1),
            bola("vertical", 19, 9, 5, 9, 165, -1),

            # Faixa das atividades e checkpoint.
            bola("horizontal", 4, 8, 1, 28, 185, 1),

            # Acesso ao setor inferior.
            bola("horizontal", 14, 10, 14, 16, 100, 1),

            # Atividades nos dois extremos do setor inferior.
            bola("vertical", 7, 11, 11, 13, 125, 1),
            bola("vertical", 11, 13, 11, 13, 125, -1),
            bola("vertical", 20, 11, 11, 13, 125, 1),
            bola("vertical", 24, 13, 11, 13, 125, -1),
        ],
    },

    # =====================================================
    # FASE 5 — DESAFIO FINAL
    #
    # Combina cruzamentos, passagens e uma travessia
    # inferior. As atividades exigem explorar cada setor.
    # =====================================================
    {
        "nome": "Projeto final - Ultimo prazo",

        "mapa": [
            "##############################",
            "#GGG-------------------------#",
            "#GSG---M------------------M--#",
            "#GGG--DD----------DD---------#",
            "#-----DD----------DD---------#",
            "######################----####",
            "#----------------------------#",
            "#--M----------C-----------M--#",
            "#-----DD----------DD---------#",
            "#-----DD----------DD---------#",
            "####----######################",
            "#-------------------------FFF#",
            "#-----------M-------------FFF#",
            "#-------------------------FFF#",
            "##############################",
        ],

        "obstaculos": [
            # Setor superior: cruzamentos.
            bola("horizontal", 5, 2, 4, 28, 225, 1),
            bola("horizontal", 26, 2, 4, 28, 225, -1),

            bola("vertical", 11, 1, 1, 4, 165, 1),
            bola("vertical", 15, 4, 1, 4, 165, -1),
            bola("vertical", 24, 1, 1, 4, 165, 1),

            # Primeira passagem.
            bola("horizontal", 22, 5, 22, 25, 150, 1),

            # Setor central.
            bola("horizontal", 3, 7, 1, 28, 220, 1),
            bola("horizontal", 26, 7, 1, 28, 220, -1),

            bola("vertical", 10, 6, 6, 9, 175, 1),
            bola("vertical", 22, 9, 6, 9, 175, -1),

            # Segunda passagem.
            bola("horizontal", 7, 10, 4, 7, 145, -1),

            # Sequência final com ritmos alternados.
            bola("vertical", 9, 11, 11, 13, 120, 1),
            bola("vertical", 13, 13, 11, 13, 135, -1),
            bola("vertical", 17, 11, 11, 13, 120, 1),
            bola("vertical", 21, 13, 11, 13, 135, -1),
            bola("vertical", 25, 11, 11, 13, 120, 1),
        ],
    },
]

TOTAL_FASES = len(FASES)