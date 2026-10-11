"""
Módulo de gestión de entradas con control de retardo para evitar rebotes y movimiento fluido con mouse.
"""
import pygame
from config import CELDA, HUD

_ultimo_movimiento_mando = 0
_bloqueo_boton_mando = True

def obtener_direccion_jugador(metodo_control, jug, dir_j, mando):
    nuevo_dir = dir_j
    if metodo_control == "TECLADO":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: nuevo_dir = (-1, 0)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: nuevo_dir = (1, 0)
        elif teclas[pygame.K_UP] or teclas[pygame.K_w]: nuevo_dir = (0, -1)
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]: nuevo_dir = (0, 1)
    
    elif metodo_control == "MOUSE":
        if pygame.mouse.get_pressed()[0]:
            m_pos = pygame.mouse.get_pos()
            
            # Obtener el tamaño actual de la ventana y escala para adaptar la posición del mouse al canvas
            v_ancho, v_alto = pygame.display.get_surface().get_size()
            from config import ANCHO, ALTO
            escala = min(v_ancho / ANCHO, v_alto / ALTO)
            pos_x = (v_ancho - int(ANCHO * escala)) // 2
            pos_y = (v_alto - int(ALTO * escala)) // 2
            
            # Convertir coordenadas de pantalla física a coordenadas del canvas de juego
            if escala > 0:
                mx = int((m_pos[0] - pos_x) / escala) // CELDA
                my = int((m_pos[1] - pos_y) / escala - HUD) // CELDA
                
                diff_x = mx - jug[0]
                diff_y = my - jug[1]
                
                # Evaluar correctamente el eje con mayor distancia o cambio de dirección libre
                if abs(diff_x) > abs(diff_y):
                    if diff_x > 0: nuevo_dir = (1, 0)
                    elif diff_x < 0: nuevo_dir = (-1, 0)
                elif abs(diff_y) > 0:
                    if diff_y > 0: nuevo_dir = (0, 1)
                    elif diff_y < 0: nuevo_dir = (0, -1)

    elif metodo_control == "MANDO" and mando:
        e_x = mando.get_axis(0)
        e_y = mando.get_axis(1)
        if e_x < -0.5: nuevo_dir = (-1, 0)
        elif e_x > 0.5: nuevo_dir = (1, 0)
        elif e_y < -0.5: nuevo_dir = (0, -1)
        elif e_y > 0.5: nuevo_dir = (0, 1)

    return nuevo_dir

def manejar_navegacion_menu(eventos, seleccion_actual, total_opciones, mando):
    global _ultimo_movimiento_mando, _bloqueo_boton_mando
    ahora = pygame.time.get_ticks()
    nueva_sel = seleccion_actual
    accion_confirmar = False

    if mando:
        boton_presionado = False
        for b in range(mando.get_numbuttons()):
            if mando.get_button(b):
                boton_presionado = True
                break
        if not boton_presionado and abs(mando.get_axis(1)) < 0.2:
            _bloqueo_boton_mando = False

    for e in eventos:
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_DOWN, pygame.K_s):
                nueva_sel = (seleccion_actual + 1) % total_opciones
            elif e.key in (pygame.K_UP, pygame.K_w):
                nueva_sel = (seleccion_actual - 1) % total_opciones
            elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                accion_confirmar = True
        elif e.type == pygame.MOUSEBUTTONDOWN:
            accion_confirmar = True

    if mando and not _bloqueo_boton_mando and ahora - _ultimo_movimiento_mando > 300:
        e_y = mando.get_axis(1)
        if e_y > 0.6:
            nueva_sel = (seleccion_actual + 1) % total_opciones
            _ultimo_movimiento_mando = ahora
        elif e_y < -0.6:
            nueva_sel = (seleccion_actual - 1) % total_opciones
            _ultimo_movimiento_mando = ahora
        
        if mando.get_button(0):
            accion_confirmar = True
            _bloqueo_boton_mando = True

    return nueva_sel, accion_confirmar