import numpy as np
import random as rd

# GERAR GRID ALEATÓRIO
def Gera_Problema_Grid_Ale(nx, ny, qtd):
    mapa = np.zeros((nx, ny), int)
    k = 0
    while k < qtd:
        i = rd.randrange(0, nx)
        j = rd.randrange(0, ny)
        if mapa[i][j] == 0:
            mapa[i][j] = 1  # obstáculo
            k += 1
    return mapa, nx, ny


# GERAR GRID A PARTIR DE ARQUIVO
def Gera_Problema_Grid_Fixo(arquivo):
    mapa = []
    with open(arquivo) as file:
        for line in file:
            linha = list(map(int, line.strip().split(",")))
            mapa.append(linha)

    nx = len(mapa)
    ny = len(mapa[0])
    return mapa, nx, ny


def imprimeCaminho(texto, caminho):
    print("\n*****", texto, "*****")
    print("Caminho:", caminho)
    print("Custo:", len(caminho) - 1)