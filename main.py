"""
Archivo principal completo y corregido: Renderizado sobre canvas, centrado y Día de Muertos.
"""
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import config
from config import *
from entidades import (
    cargar_mapa_desde_lineas, decidir, hay_colision, 
    dibujar_calavera, dibujar_fantasma_terrorifico, 
    dibujar_flor_cempasuchil, dibujar_altar, 
    texto, centro, Fantasma
)
from generador import generar_mapa_aleatorio
from controles import obtener_direccion_jugador, manejar_navegacion_menu

pygame.init()
pygame.mixer.init()

pygame.joystick.init()
mando = None
if pygame.joystick.get_count() > 0:
    mando = pygame.joystick.Joystick(0)
    mando.init()

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
CARPETA_SOUNDS = os.path.join(DIRECTORIO_BASE, "sounds")

try:
    SONIDO_COMER = pygame.mixer.Sound(os.path.join(CARPETA_SOUNDS, "eat.mp3"))
    SONIDO_PODER = pygame.mixer.Sound(os.path.join(CARPETA_SOUNDS, "drink.mp3"))
    SONIDO_GHOST = pygame.mixer.Sound(os.path.join(CARPETA_SOUNDS, "ghost.mp3"))
    SONIDO_COMER.set_volume(0.8)
    SONIDO_PODER.set_volume(0.8)
    SONIDO_GHOST.set_volume(0.8)
except:
    SONIDO_COMER = SONIDO_PODER = SONIDO_GHOST = None

config.V = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("Ofrenda de la Calavera - Día de Muertos")
canvas = pygame.Surface((ANCHO, ALTO))

RELOJ = pygame.time.Clock()
BOTON_MENU = pygame.Rect(ANCHO - 110, 18, 94, 32)

def reproducir_musica(nombre_archivo, repetir=-1):
    try:
        ruta = os.path.join(CARPETA_SOUNDS, nombre_archivo)
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(repetir)
        pygame.mixer.music.set_volume(0.5)
    except pygame.error as e:
        print(f"Error al cargar música ({nombre_archivo}): {e}")

def actualizar_pantalla_centrada(superficie_destino, superficie_origen):
    v_ancho, v_alto = superficie_destino.get_size()
    escala = min(v_ancho / ANCHO, v_alto / ALTO)
    nuevo_ancho = int(ANCHO * escala)
    nuevo_alto = int(ALTO * escala)
    
    superficie_escalada = pygame.transform.scale(superficie_origen, (nuevo_ancho, nuevo_alto))
    pos_x = (v_ancho - nuevo_ancho) // 2
    pos_y = (v_alto - nuevo_alto) // 2
    
    superficie_destino.fill((10, 5, 15))
    superficie_destino.blit(superficie_escalada, (pos_x, pos_y))
    pygame.display.flip()

def seleccionar_control():
    reproducir_musica("menu.mp3", -1)
    rects = [
        pygame.Rect(70, 180, ANCHO - 140, 64),
        pygame.Rect(70, 260, ANCHO - 140, 64),
        pygame.Rect(70, 340, ANCHO - 140, 64)
    ]
    opciones = ["TECLADO", "MOUSE", "MANDO"]
    seleccion = 0
    
    while True:
        RELOJ.tick(60)
        canvas.fill(FONDO)
        texto("☠ MÉTODO DE CONTROL ☠", F_T, (255, 165, 0), (ANCHO // 2, 60), True, superficie=canvas)
        texto("Usa W-S y Enter o Mando", F_M, TXT_SUAVE, (ANCHO // 2, 115), True, superficie=canvas)
        
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.VIDEORESIZE:
                config.V = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)

        seleccion, confirmado = manejar_navegacion_menu(eventos, seleccion, len(opciones), mando)
        
        v_ancho, v_alto = config.V.get_size()
        escala = min(v_ancho / ANCHO, v_alto / ALTO)
        pos_x = (v_ancho - int(ANCHO * escala)) // 2
        pos_y = (v_alto - int(ALTO * escala)) // 2
        mouse_pos = pygame.mouse.get_pos()
        mouse_en_canvas = ((mouse_pos[0] - pos_x) / escala, (mouse_pos[1] - pos_y) / escala)

        for i, opt in enumerate(opciones):
            r = rects[i]
            hover = r.collidepoint(mouse_en_canvas) or (seleccion == i)
            pygame.draw.rect(canvas, (60, 30, 20) if hover else (30, 16, 25), r, border_radius=12)
            pygame.draw.rect(canvas, (255, 165, 0) if hover else (120, 60, 30), r, 2, border_radius=12)
            texto(f"• {opt}", F_M, TXT, (r.x + 24, r.y + 18), superficie=canvas)
            
            if r.collidepoint(mouse_en_canvas) and any(ev.type == pygame.MOUSEBUTTONDOWN for ev in eventos):
                return opciones[i]

        if confirmado:
            return opciones[seleccion]

        actualizar_pantalla_centrada(config.V, canvas)

def menu():
    reproducir_musica("menu.mp3", -1)
    claves = ["Facil", "Medio", "Dificil"]
    rects = [pygame.Rect(70, 170 + i * 95, ANCHO - 140, 76) for i in range(3)]
    seleccion = 0
    
    while True:
        RELOJ.tick(60)
        canvas.fill(FONDO)
        
        texto("☠ OFRENDA DE LA CALAVERA ☠", F_T, (255, 165, 0), (ANCHO // 2, 50), True, superficie=canvas)
        texto("Selecciona la dificultad", F_M, TXT_SUAVE, (ANCHO // 2, 105), True, superficie=canvas)
        
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.VIDEORESIZE:
                config.V = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    return claves[e.key - pygame.K_1]

        seleccion, confirmado = manejar_navegacion_menu(eventos, seleccion, len(claves), mando)
        
        v_ancho, v_alto = config.V.get_size()
        escala = min(v_ancho / ANCHO, v_alto / ALTO)
        pos_x = (v_ancho - int(ANCHO * escala)) // 2
        pos_y = (v_alto - int(ALTO * escala)) // 2
        mouse = pygame.mouse.get_pos()
        mouse_en_canvas = ((mouse[0] - pos_x) / escala, (mouse[1] - pos_y) / escala)

        for i, k in enumerate(claves):
            cfg, r = DIFICULTADES[k], rects[i]
            hover = r.collidepoint(mouse_en_canvas) or (seleccion == i)
            pygame.draw.rect(canvas, (60, 30, 20) if hover else (30, 16, 25), r, border_radius=14)
            pygame.draw.rect(canvas, cfg["color"] if hover else (120, 60, 30), r, 2, border_radius=14)
            
            texto(f"{i + 1}. {cfg['nombre']}", F_M, cfg["color"], (r.x + 20, r.y + 10), superficie=canvas)
            texto(cfg["tecnica"], F_S, TXT_SUAVE, (r.x + 20, r.y + 46), superficie=canvas)

            if r.collidepoint(mouse_en_canvas) and any(ev.type == pygame.MOUSEBUTTONDOWN for ev in eventos):
                return claves[i]

        if confirmado:
            return claves[seleccion]

        actualizar_pantalla_centrada(config.V, canvas)

def jugar(dif, metodo_control):
    reproducir_musica("game.mp3", -1)
    cfg = DIFICULTADES[dif]
    lineas_mapa = generar_mapa_aleatorio(cfg["n_fantasmas"])
    muros, puntos, poderes, jug, inicios = cargar_mapa_desde_lineas(lineas_mapa)
    
    fant = [Fantasma(p, cfg["colores"][i]) for i, p in enumerate(inicios)]
    dir_j, asustado = (0, 0), 0
    fin = None
    pausa = False
    msg = "¡Recolecta flores y altares!"

    t_jugador = 0
    t_fantasma = 0
    VELOCIDAD_JUGADOR = 130  
    VELOCIDAD_FANTASMA = 280 

    while True:
        ahora = pygame.time.get_ticks()
        RELOJ.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.VIDEORESIZE:
                config.V = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.MOUSEBUTTONDOWN:
                v_ancho, v_alto = config.V.get_size()
                escala = min(v_ancho / ANCHO, v_alto / ALTO)
                pos_x = (v_ancho - int(ANCHO * escala)) // 2
                pos_y = (v_alto - int(ALTO * escala)) // 2
                mx = (e.pos[0] - pos_x) / escala
                my = (e.pos[1] - pos_y) / escala
                if BOTON_MENU.collidepoint((mx, my)):
                    return
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_m, pygame.K_ESCAPE):
                    return
                if e.key == pygame.K_p:
                    pausa = not pausa
                if fin and e.key == pygame.K_r:
                    return
            if e.type == pygame.JOYBUTTONDOWN and mando:
                if e.button == 7: pausa = not pausa
                if e.button == 1: return

        if pausa:
            canvas.fill((20, 10, 30))
            texto("☠ CAMINO PAUSADO", F_T, (255, 165, 0), (ANCHO // 2, ALTO // 2 - 30), True, superficie=canvas)
            texto("Presiona 'P' o Start para continuar", F_S, TXT, (ANCHO // 2, ALTO // 2 + 20), True, superficie=canvas)
            actualizar_pantalla_centrada(config.V, canvas)
            continue

        nuevo_dir = obtener_direccion_jugador(metodo_control, jug, dir_j, mando)

        if not fin and nuevo_dir != (0, 0) and ahora - t_jugador >= VELOCIDAD_JUGADOR:
            siguiente_pos = (jug[0] + nuevo_dir[0], jug[1] + nuevo_dir[1])
            if siguiente_pos not in muros:
                jug = siguiente_pos
                dir_j = nuevo_dir
                t_jugador = ahora
                
                if jug in puntos:
                    puntos.discard(jug)
                    if SONIDO_COMER: SONIDO_COMER.play()
                if jug in poderes:
                    poderes.discard(jug)
                    asustado = 15
                    if SONIDO_PODER: SONIDO_PODER.play()

        if not fin and ahora - t_fantasma >= VELOCIDAD_FANTASMA:
            for i, f in enumerate(fant):
                nuevo = decidir(f, i, dif, muros, jug, dir_j, asustado > 0)
                f.anterior, f.pos = f.pos, nuevo
            t_fantasma = ahora
            if asustado > 0:
                asustado = max(0, asustado - 1)

        for i, f in enumerate(fant):
            if f.pos == jug:
                if asustado > 0:
                    if SONIDO_GHOST: SONIDO_GHOST.play()
                    f.pos = inicios[i]
                    msg = "¡Alma espantada!"
                else:
                    fin = "PERDISTE"

        if not puntos and not poderes:
            fin = "GANASTE"

        canvas.fill(FONDO)
        for ry in range(FILAS):
            for rx in range(COLS):
                if (rx, ry) not in muros:
                    rect_suelo = pygame.Rect(rx * CELDA, HUD + ry * CELDA, CELDA, CELDA)
                    pygame.draw.rect(canvas, PISO_JARDIN, rect_suelo)
                    pygame.draw.rect(canvas, (35, 20, 10), rect_suelo, 1)

        for (x, y) in muros:
            pygame.draw.rect(canvas, MURO, (x * CELDA + 2, HUD + y * CELDA + 2, CELDA - 4, CELDA - 4), border_radius=6)
            pygame.draw.rect(canvas, MURO_BORDE, (x * CELDA + 2, HUD + y * CELDA + 2, CELDA - 4, CELDA - 4), 1, border_radius=6)
            
        for p in puntos:
            dibujar_flor_cempasuchil(p, canvas)
            
        for p in poderes:
            dibujar_altar(p, canvas)

        dibujar_calavera(jug, canvas)
        parpadeo = asustado <= 3 and (ahora // 200) % 2 == 0
        for f in fant:
            dibujar_fantasma_terrorifico(f, asustado > 0, parpadeo, canvas)

        texto(f"Nivel {cfg['nombre']} ({metodo_control})", F_M, cfg["color"], (16, 8), superficie=canvas)
        texto(f"Ofrendas restantes: {len(puntos) + len(poderes)}", F_S, TXT_SUAVE, (16, 42), superficie=canvas)
        
        pygame.draw.rect(canvas, (60, 30, 20), BOTON_MENU, border_radius=10)
        pygame.draw.rect(canvas, TXT_SUAVE, BOTON_MENU, 1, border_radius=10)
        texto("Menú (M)", F_S, TXT, (BOTON_MENU.centerx, BOTON_MENU.y + 6), True, superficie=canvas)
        
        texto(msg, F_S, TXT_SUAVE, (16, HUD + FILAS * CELDA + 8), superficie=canvas)

        if fin:
            velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo.fill((10, 5, 15, 220))
            canvas.blit(velo, (0, 0))
            texto("¡TE ALCANZARON LAS ALMAS!" if fin == "PERDISTE" else "¡COMPLETA TU OFRENDA!", F_T,
                  VERDE_OK if fin == "GANASTE" else ROJO_X, (ANCHO // 2, ALTO // 2 - 40), True, superficie=canvas)
            texto("Presiona R para reintentar o Menú", F_S, TXT, (ANCHO // 2, ALTO // 2 + 10), True, superficie=canvas)
            
        actualizar_pantalla_centrada(config.V, canvas)

if __name__ == "__main__":
    while True:
        control = seleccionar_control()
        dificultad = menu()
        jugar(dificultad, control)