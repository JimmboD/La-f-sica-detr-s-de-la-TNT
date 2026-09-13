import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches

# Importamos tu motor cinemático
from trayectoria import predecir_trayectoria_tnt

plt.style.use('dark_background')

# 1. Definición del Entorno Físico Dinámico
mapa_laboratorio = {}
parches_visuales = {} # Nuevo diccionario para rastrear los rectángulos dibujados

# Generamos un suelo base inicial
for i in range(0, 20):
    mapa_laboratorio[(i, -61, 0)] = True

x0_base, y0_base, z0_base = 0.5, -60.0, 0.5
vx_init, vy_init = 0.8, 0.6

# 2. Configuración del Lienzo
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(bottom=0.25) 

# Función auxiliar para dibujar un bloque y guardarlo en pantalla
def dibujar_bloque_visual(bx, by, bz):
    bloque = patches.Rectangle(
        (bx, by), 1, 1, 
        linewidth=1, edgecolor='#111111', facecolor='#666666', zorder=0
    )
    ax.add_patch(bloque)
    parches_visuales[(bx, by, bz)] = bloque

# Dibujar el suelo base inicial
for (bx, by, bz) in mapa_laboratorio.copy():
    dibujar_bloque_visual(bx, by, bz)

# 3. Generar Objetos Visuales Iniciales
datos_crudos = predecir_trayectoria_tnt(mapa_laboratorio, x0_base, y0_base, z0_base, vx_init, vy_init, 0.0, 80)
matriz = np.array(datos_crudos)

linea_trayectoria, = ax.plot(matriz[:, 1], matriz[:, 2], color='#aaaaaa', linestyle='--', linewidth=1.5, zorder=1)
puntos_tnt = ax.scatter(matriz[:, 1], matriz[:, 2], color='red', s=45, zorder=2)

# 4. Estética de la Cuadrícula
ax.set_title('Laboratorio Interactivo: Haz clic en la cuadrícula para añadir/quitar muros', fontsize=14, pad=15)
ax.set_xlabel('Eje X (Bloques)')
ax.set_ylabel('Eje Y (Bloques)')
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.grid(True, color='#222222', linestyle='-', linewidth=1, zorder=-1)

ax.set_xlim(0, 20)
ax.set_ylim(-61, -48)
ax.set_aspect('equal', adjustable='box')

# 5. Sliders de Velocidad
ax_slider_vx = plt.axes([0.15, 0.10, 0.7, 0.03])
ax_slider_vy = plt.axes([0.15, 0.05, 0.7, 0.03])
slider_vx = Slider(ax_slider_vx, 'Vx', 0.0, 2.0, valinit=vx_init, color='#3498db')
slider_vy = Slider(ax_slider_vy, 'Vy', -1.0, 2.0, valinit=vy_init, color='#e74c3c')

# 6. Lógica de Actualización Centralizada
def actualizar(val=None):
    # Recalcular física con el mapa actual y velocidades actuales
    nuevos_datos = predecir_trayectoria_tnt(
        mapa_laboratorio, x0_base, y0_base, z0_base, slider_vx.val, slider_vy.val, 0.0, 80
    )
    nueva_matriz = np.array(nuevos_datos)
    
    # Actualizar gráfica
    linea_trayectoria.set_data(nueva_matriz[:, 1], nueva_matriz[:, 2])
    puntos_tnt.set_offsets(np.c_[nueva_matriz[:, 1], nueva_matriz[:, 2]])
    fig.canvas.draw_idle()

slider_vx.on_changed(actualizar)
slider_vy.on_changed(actualizar)

# 7. EL MOTOR DE INTERACTIVIDAD (Clics y Arrastre de Cámara)

# Diccionario de estado para rastrear la cámara
estado_camara = {'arrastrando': False, 'x_ref': 0, 'y_ref': 0}

def al_presionar_raton(event):
    if event.inaxes != ax:
        return
        
    # --- Clic Izquierdo: Construir y Destruir Bloques ---
    if event.button == 1: 
        bx = math.floor(event.xdata)
        by = math.floor(event.ydata)
        coord = (bx, by, 0)
        
        if coord in mapa_laboratorio:
            del mapa_laboratorio[coord]
            parche = parches_visuales.pop(coord)
            parche.remove()
        else:
            mapa_laboratorio[coord] = True
            dibujar_bloque_visual(bx, by, 0)
            
        actualizar()
        
    # --- Clic Rueda (Middle Click): Iniciar anclaje de cámara ---
    elif event.button == 2:
        estado_camara['arrastrando'] = True
        # Guardamos la coordenada matemática exacta en la que el usuario hizo clic
        estado_camara['x_ref'] = event.xdata
        estado_camara['y_ref'] = event.ydata

def al_mover_raton(event):
    # Si estamos arrastrando la rueda y el puntero sigue en la gráfica
    if estado_camara['arrastrando'] and event.inaxes == ax:
        
        # Calculamos la diferencia entre nuestro punto de anclaje original y la posición actual del ratón
        dx = estado_camara['x_ref'] - event.xdata
        dy = estado_camara['y_ref'] - event.ydata
        
        # Obtenemos los límites de la cámara y los desplazamos
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        
        ax.set_xlim(xmin + dx, xmax + dx)
        ax.set_ylim(ymin + dy, ymax + dy)
        
        # Redibujar la ventana (draw_idle es eficiente, no congela la interfaz)
        fig.canvas.draw_idle()

def al_soltar_raton(event):
    # Si soltamos la rueda, apagamos el motor de paneo
    if event.button == 2:
        estado_camara['arrastrando'] = False

# Conectamos las tres funciones al sistema central de Matplotlib
fig.canvas.mpl_connect('button_press_event', al_presionar_raton)
fig.canvas.mpl_connect('motion_notify_event', al_mover_raton)
fig.canvas.mpl_connect('button_release_event', al_soltar_raton)

plt.show()