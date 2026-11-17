TAMANHO_BLOCO = 30
ORIGEM_MAPA = (0, 120)

# FASE 1
FASES = [
    {
        "nome": "Primeiros passos",

        "mapa": [
            "##############################",
            "##############################",
            "######------------------######",
            "######------------------######",
            "######------------------######",
            "##GGGG--------M---------FFFF##",
            "##GSGG------------------FFFF##",
            "######------------------######",
            "######------------------######",
            "######------------------######",
            "##############################",
            "##############################",
        ],

        "obstaculos": [],
    },
]

for i in range(12):
    if i % 2 == 0:
        linha_inicial = 3
        sentido = 1
    else:
        linha_inicial = 8
        sentido = -1

    obstaculo = {
        "tipo": "vertical",
        "coluna": 6.25 + i * 1.5,
        "linha": linha_inicial,
        "limite_inicial": 2,
        "limite_final": 9,
        "velocidade": 250,
        "sentido": sentido,
    }

    FASES[0]["obstaculos"].append(obstaculo)


# FASE 2
FASES.append(
    {
        "nome": "Espiral",

        "mapa": [
            "##############################",
            "##SG-----------------------C##",
            "##########################-###",
            "##########################-###",
            "##C---------------------##-###",
            "#####-#################-##-###",
            "#####-#################-##-###",
            "#####-##-----------FF##-##-###",
            "#####-##-##########FF##-##-###",
            "#####-##-##############-##-###",
            "#####-##----------------##-###",
            "#####-####################-###",
            "#####-####################-###",
            "#####----------------------###",
            "##############################",
        ],

        "obstaculos": [],
    }
)

for angulo in (15, 105, 195, 285):
    for raio_orbita in (1.5, 4.5, 7.5, 10.5, 13.5):
        obstaculo = {
            "tipo": "circular",
            "coluna_centro": 15.5,
            "linha_centro": 7,
            "raio_orbita": raio_orbita,
            "angulo": angulo,
            "velocidade_angular": 90,
        }

        FASES[1]["obstaculos"].append(obstaculo)

TOTAL_FASES = len(FASES)


TOTAL_FASES = len(FASES)