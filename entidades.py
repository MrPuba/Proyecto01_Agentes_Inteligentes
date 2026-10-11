"""
Lógica de IA, clases y representación gráfica adaptada a Día de Muertos con soporte de canvas y configuración.
"""
import heapq
import random
import pygame
import config
from config import COLS, FILAS, DIRS, MIEDO, TXT, CELDA, HUD

def cargar_mapa_desde_lineas(lineas):
    muros, puntos, poderes, jugador, fantasmas = set(), set(), set(), None, []
    for y, fila in enumerate(lineas):
        for x, c in enumerate(fila):
            if c == "#":
                muros.add((x, y))
            elif c == ".":
                puntos.add((x, y))
            elif c == "o":
                poderes.add((x, y))
            elif c == "P":
                jugador = (x, y)
            elif c == "G":
                fantasmas.append((x, y))
    if not jugador:
        jugador = (COLS // 2, FILAS // 2)
    return muros, puntos, poderes, jugador, fantasmas

def vecinos(pos, muros):
    res = []
    for dx, dy in DIRS:
        n = (pos[0] + dx, pos[1] + dy)
        if 0 <= n[0] < COLS and 0 <= n[1] < FILAS and n not in muros:
            res.append(n)
    return res

class Fantasma:
    def __init__(self, pos, color):
        self.pos = self.inicio = self.anterior = pos
        self.color = color

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(muros, ini, meta):
    abiertos = [(manhattan(ini, meta), 0, ini)]
    padre, g = {ini: None}, {ini: 0}
    while abiertos:
        _, costo, act = heapq.heappop(abiertos)
        if act == meta:
            camino = []
            while act is not None:
                camino.append(act)
                act = padre[act]
            return camino[::-1]
        for n in vecinos(act, muros):
            nc = costo + 1
            if n not in g or nc < g[n]:
                g[n], padre[n] = nc, act
                heapq.heappush(abiertos, (nc + manhattan(n, meta), nc, n))
    return [ini]

def decidir(f, i, dif, muros, jugador, dir_j, asustado):
    opciones = vecinos(f.pos, muros)
    if not opciones:
        return f.pos
    random.shuffle(opciones)
    sin_retro = [o for o in opciones if o != f.anterior] or opciones

    if asustado:
        return max(opciones, key=lambda o: manhattan(o, jugador))

    if dif == "Facil":
        return random.choice(sin_retro)

    if dif == "Medio":
        return min(opciones, key=lambda o: manhattan(o, jugador))

    meta = (jugador[0] + dir_j[0] * 2, jugador[1] + dir_j[1] * 2)
    if meta in muros or not (0 <= meta[0] < COLS and 0 <= meta[1] < FILAS):
        meta = jugador

    camino = astar(muros, f.pos, meta)
    if len(camino) < 2:
        camino = astar(muros, f.pos, jugador)
    return camino[1] if len(camino) > 1 else f.pos

def hay_colision(fantasmas, jugador, asustado):
    for f in fantasmas:
        if f.pos == jugador:
            if asustado > 0:
                f.pos = f.anterior = f.inicio
            else:
                return True
    return False

def centro(pos):
    return pos[0] * CELDA + CELDA // 2, HUD + pos[1] * CELDA + CELDA // 2

def dibujar_calavera(pos, superficie):
    cx, cy = centro(pos)
    r = 13
    pygame.draw.circle(superficie, (240, 240, 245), (cx, cy - 1), r - 2)
    pygame.draw.rect(superficie, (240, 240, 245), (cx - 5, cy + 4, 10, 6), border_radius=2)
    pygame.draw.circle(superficie, (20, 15, 30), (cx - 4, cy - 2), 2.5)
    pygame.draw.circle(superficie, (20, 15, 30), (cx + 4, cy - 2), 2.5)
    pygame.draw.polygon(superficie, (20, 15, 30), [(cx, cy + 1), (cx - 1.5, cy + 3.5), (cx + 1.5, cy + 3.5)])

def dibujar_fantasma_terrorifico(f, asustado, parpadeo, superficie):
    cx, cy = centro(f.pos)
    r = 13
    col = MIEDO if asustado else f.color
    if asustado and parpadeo:
        col = TXT

    pygame.draw.circle(superficie, col, (cx, cy - 2), r)
    pygame.draw.rect(superficie, col, (cx - r, cy - 2, 2 * r, r + 2))
    for gx in (cx - r + 3, cx, cx + r - 3):
        pygame.draw.circle(superficie, config.FONDO, (gx, cy + r), 3)

    for ex in (-4, 4):
        pygame.draw.circle(superficie, (255, 255, 255), (cx + ex, cy - 3), 3)
        pygame.draw.circle(superficie, (0, 0, 0), (cx + ex, cy - 3), 1)

def dibujar_flor_cempasuchil(pos, superficie):
    cx, cy = centro(pos)
    pygame.draw.circle(superficie, (255, 165, 0), (cx, cy), 5)
    pygame.draw.circle(superficie, (255, 215, 0), (cx, cy), 3)

def dibujar_altar(pos, superficie):
    cx, cy = centro(pos)
    pygame.draw.rect(superficie, (180, 70, 20), (cx - 8, cy - 4, 16, 9), border_radius=2)
    pygame.draw.rect(superficie, (255, 140, 0), (cx - 2, cy - 10, 4, 6))
    pygame.draw.circle(superficie, (255, 255, 0), (cx, cy - 11), 2)

def texto(t, fuente, color, pos, centrado=False, superficie=None):
    s = fuente.render(t, True, color)
    superficie.blit(s, (pos[0] - s.get_width() // 2, pos[1]) if centrado else pos)