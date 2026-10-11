"""
Generador procedural de laberintos con spawn seguro para el jugador.
"""
import random
from config import COLS, FILAS

def generar_mapa_aleatorio(n_fantasmas):
    mapa = [["#" for _ in range(COLS)] for _ in range(FILAS)]
    filas_gen = FILAS if FILAS % 2 != 0 else FILAS - 1
    cols_gen = COLS if COLS % 2 != 0 else COLS - 1

    inicio_x, inicio_y = 1, 1
    mapa[inicio_y][inicio_x] = "."
    pila = [(inicio_x, inicio_y)]

    while pila:
        x, y = pila[-1]
        vecinos = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < cols_gen and 0 < ny < filas_gen and mapa[ny][nx] == "#":
                vecinos.append((nx, ny, dx // 2, dy // 2))

        if vecinos:
            nx, ny, pdx, pdy = random.choice(vecinos)
            mapa[y + pdy][x + pdx] = "."
            mapa[ny][nx] = "."
            pila.append((nx, ny))
        else:
            pila.pop()

    for _ in range((COLS * FILAS) // 8):
        rx = random.randint(1, COLS - 2)
        ry = random.randint(1, FILAS - 2)
        mapa[ry][rx] = "."

    jug_x, jug_y = COLS // 2, FILAS - 2
    mapa[jug_y][jug_x] = "P"

    esquinas = [(1, 1), (COLS - 2, 1), (1, FILAS - 2), (COLS - 2, FILAS - 2)]
    for ex, ey in esquinas:
        if 0 <= ex < COLS and 0 <= ey < FILAS:
            mapa[ey][ex] = "o"

    fantasmas_colocados = 0
    while fantasmas_colocados < n_fantasmas:
        gx = random.randint(1, COLS - 2)
        gy = random.randint(1, FILAS - 2)
        distancia = abs(gx - jug_x) + abs(gy - jug_y)
        if mapa[gy][gx] == "." and distancia >= 3:
            mapa[gy][gx] = "G"
            fantasmas_colocados += 1

    return ["".join(fila) for fila in mapa]