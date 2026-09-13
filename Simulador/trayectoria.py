import math

def predecir_trayectoria_tnt(mundo_solido, x0, y0, z0, v0x, v0y, v0z, limite_ticks=80):
    """
    Simula la trayectoria de una TNT aplicando la cinemática discreta de Java
    y evitación estricta de colisiones AABB por ejes independientes.
    """
    # 1. Constantes Físicas Oficiales
    g = 0.04
    d_aire = 0.98
    p_suelo = 0.7
    d_suelo = d_aire * p_suelo # 0.686
    
    # Dimensiones de la Caja de Colisión (AABB)
    radio = 0.49   # Semi-ancho horizontal
    altura = 0.98  # Altura vertical
    
    # 2. Inicialización de Vectores
    x, y, z = x0, y0, z0
    vx, vy, vz = v0x, v0y, v0z
    
    # Registrar el Tick 0 (Origen)
    telemetria = [[0, x, y, z, vx, vy, vz, 0]]
    
    limite = max(0, min(80, limite_ticks))
    
    for tick in range(1, limite + 1):
        
        # --- PASO 1: GRAVEDAD ---
        vy -= g
        en_suelo = False
        
        # --- PASO 2: EJE Y (Vertical) ---
        y_nuevo = y + vy
        # Evaluamos según la dirección del movimiento vertical
        if vy < 0: # Cayendo (Evaluamos la base inferior de la TNT: y)
            voxel_base_y = math.floor(y_nuevo)
            # Verificamos los 4 puntos de las esquinas de la base en X y Z
            if ((math.floor(x - radio), voxel_base_y, math.floor(z - radio)) in mundo_solido or
                (math.floor(x + radio), voxel_base_y, math.floor(z - radio)) in mundo_solido or
                (math.floor(x - radio), voxel_base_y, math.floor(z + radio)) in mundo_solido or
                (math.floor(x + radio), voxel_base_y, math.floor(z + radio)) in mundo_solido):
                
                y = float(voxel_base_y + 1.0)
                vy = 0.0
                en_suelo = True
            else:
                y = y_nuevo
        elif vy > 0: # Subiendo (Evaluamos la cabeza superior de la TNT: y + altura)
            voxel_top_y = math.floor(y_nuevo + altura)
            if ((math.floor(x - radio), voxel_top_y, math.floor(z - radio)) in mundo_solido or
                (math.floor(x + radio), voxel_top_y, math.floor(z - radio)) in mundo_solido or
                (math.floor(x - radio), voxel_top_y, math.floor(z + radio)) in mundo_solido or
                (math.floor(x + radio), voxel_top_y, math.floor(z + radio)) in mundo_solido):
                
                y = float(voxel_top_y) - altura
                vy = 0.0
            else:
                y = y_nuevo
        else:
            y = y_nuevo

        # --- PASO 3: EJE X (Horizontal) ---
        x_nuevo = x + vx
        if vx > 0: # Moviéndose a la derecha (+X) -> Evaluamos el borde delantero (x + radio)
            voxel_delantero_x = math.floor(x_nuevo + radio)
            if ((voxel_delantero_x, math.floor(y), math.floor(z - radio)) in mundo_solido or
                (voxel_delantero_x, math.floor(y), math.floor(z + radio)) in mundo_solido or
                (voxel_delantero_x, math.floor(y + altura), math.floor(z - radio)) in mundo_solido or
                (voxel_delantero_x, math.floor(y + altura), math.floor(z + radio)) in mundo_solido):
                
                x = float(voxel_delantero_x) - radio
                vx = 0.0
            else:
                x = x_nuevo
        elif vx < 0: # Moviéndose a la izquierda (-X) -> Evaluamos el borde trasero (x - radio)
            voxel_trasero_x = math.floor(x_nuevo - radio)
            if ((voxel_trasero_x, math.floor(y), math.floor(z - radio)) in mundo_solido or
                (voxel_trasero_x, math.floor(y), math.floor(z + radio)) in mundo_solido or
                (voxel_trasero_x, math.floor(y + altura), math.floor(z - radio)) in mundo_solido or
                (voxel_trasero_x, math.floor(y + altura), math.floor(z + radio)) in mundo_solido):
                
                x = float(voxel_trasero_x + 1.0) + radio
                vx = 0.0
            else:
                x = x_nuevo
        else:
            x = x_nuevo

        # --- PASO 4: EJE Z (Profundidad) ---
        z_nuevo = z + vz
        if vz > 0:
            voxel_sur_z = math.floor(z_nuevo + radio)
            if (math.floor(x - radio), math.floor(y), voxel_sur_z) in mundo_solido or \
               (math.floor(x + radio), math.floor(y), voxel_sur_z) in mundo_solido:
                z = float(voxel_sur_z) - radio
                vz = 0.0
            else:
                z = z_nuevo
        elif vz < 0:
            voxel_norte_z = math.floor(z_nuevo - radio)
            if (math.floor(x - radio), math.floor(y), voxel_norte_z) in mundo_solido or \
               (math.floor(x + radio), math.floor(y), voxel_norte_z) in mundo_solido:
                z = float(voxel_norte_z + 1.0) + radio
                vz = 0.0
            else:
                z = z_nuevo
        else:
            z = z_nuevo

        # --- PASO 5: FRICCIÓN (DRAG) ---
        if en_suelo:
            vx *= d_suelo
            vz *= d_suelo
        else:
            vx *= d_aire
            vy *= d_aire
            vz *= d_aire
            
        # 6. Guardar estado del tick
        telemetria.append([tick, x, y, z, vx, vy, vz, int(en_suelo)])
        
    return telemetria