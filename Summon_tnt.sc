global_tnts = m();

__command() -> (
    posicion_tnt = [0.5, -60, 0.5];

    propiedades = {
        'Motion' -> [1, 0, 0]
    };

    nueva_tnt = spawn('tnt', posicion_tnt, propiedades);

    // 1. Extraemos el vector de velocidad exacta en el tick 0
    [v0x, v0y, v0z] = nueva_tnt ~ 'motion';
    
    // 2. Construimos el nombre dinámico. 
    // Usamos %.2f para limitar a 2 decimales en el título y mantenerlo legible.
    // Ejemplo de salida: tnt_v0_0.00_1.00_0.00
    nombre_archivo = str('tnt_v0_%.2f_%.2f_%.2f', v0x, v0y, v0z);

    historial_base = l('tick,x,y,z,vx,vy,vz,suelo');
    
    // 3. Guardamos el nombre_archivo al final de nuestra lista de datos
    put(global_tnts, nueva_tnt ~ 'id', [nueva_tnt, tick_time(), historial_base, nombre_archivo]);
    
    print(player(), format('g TNT invocada. Rastreando telemetría...'));
);

__on_tick() -> (
    for(keys(global_tnts),
        id = _;
        
        datos = get(global_tnts, id);
        entidad = get(datos, 0);
        tiempo_inicio = get(datos, 1);
        historial = get(datos, 2);
        nombre_archivo = get(datos, 3); // 4. Recuperamos el nombre del archivo
        
        if (entidad ~ 'removed',
            // --- FASE DE EXPLOSIÓN ---
            
            // Usamos la variable de nombre que creamos al inicio
            write_file(nombre_archivo, 'shared_text', historial);
            
            print(player('all'), format('a ¡Boom! Archivo guardado: ' + nombre_archivo + '.txt'));
            
            delete(global_tnts, id);
            
        , // --- FASE DE VUELO ---
            tick_relativo = tick_time() - tiempo_inicio;
            
            [px, py, pz] = entidad ~ 'pos';
            [vx, vy, vz] = entidad ~ 'motion';

            tocando_suelo = if(entidad ~ 'on_ground', 1, 0);
            
            linea_csv = str('%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d', 
                tick_relativo, px, py, pz, vx, vy, vz, tocando_suelo
            );
            
            put(historial, null, linea_csv);
        );
    );
);