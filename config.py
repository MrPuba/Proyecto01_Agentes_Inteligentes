"""
Configuración global del juego estilo Día de Muertos y dimensiones dinámicas.
"""
import os
import pygame

pygame.init()

# ---- Tamaño de la Mansión / Ofrenda
COLS, FILAS = 15, 13
CELDA = 36
HUD, PIE = 70, 36
ANCHO = COLS * CELDA
ALTO = HUD + FILAS * CELDA + PIE
FPS = 60

# ---- Paleta de Colores: Día de Muertos
FONDO = (18, 12, 28)          # Noche profunda mística
MURO = (45, 25, 40)           # Paredes de tono terracota oscuro
MURO_BORDE = (90, 45, 70)
PISO_JARDIN = (24, 30, 22)    # Fondo de camino de ofrenda
PUNTO = (255, 165, 0)         # Flor de Cempasúchil
PODER = (255, 100, 0)         # Altar sagrado con veladora

TXT, TXT_SUAVE = (245, 240, 255), (170, 150, 200)
VERDE_OK, ROJO_X = (100, 240, 140), (255, 80, 90)
MIEDO = (50, 120, 220)        # Color azul fantasmal de ánimas asustadas

F_T = pygame.font.SysFont("Arial", 34, bold=True)
F_M = pygame.font.SysFont("Arial", 24)
F_S = pygame.font.SysFont("Arial", 16)

DIFICULTADES = {
    "Facil": {
        "nombre": "Fácil", 
        "color": (130, 230, 150), 
        "colores": [(255, 100, 100)],
        "n_fantasmas": 1, 
        "tecnica": "Ánima errante · 1 Fantasma"
    },
    "Medio": {
        "nombre": "Medio", 
        "color": (255, 200, 100), 
        "colores": [(255, 100, 100), (255, 150, 50)],
        "n_fantasmas": 2, 
        "tecnica": "Ánimas voraces · 2 Fantasmas"
    },
    "Dificil": {
        "nombre": "Difícil", 
        "color": (255, 90, 120), 
        "colores": [(255, 100, 100), (200, 50, 255)],
        "n_fantasmas": 2, 
        "tecnica": "Ánimas con A* Predictivo · 2 Fantasmas"
    },
}

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
V = None