# La física detrás de la TNT
Video relacionado a este proyecto: https://youtu.be/94O8wDkyr68

Para usar el script que invoca las TNT´s debes ir a la carpeta donde está Minecraft (%appdata% generalmente), buscar el mundo donde te interesa correr el script y colocarlo en la subcarpeta de Sripts (saves/mundo/scrips), desde luego cuando lances el juego debes estar seguro o segura de tener instalado el carpet mod y la versión correspondiente de fabric.
Si deseas modificar la posición donde se invoca la TNT solo debes modificar las coordenadas en la linea
``` Carpet
posicion_tnt = [x, y, z];
```
y si deseas modificar las velocidades iniciales
``` Carpet
'Motion' -> [1, 0, 0]
```

Para el simulador solo basta con que se ejecute el script de gráfica, para agregar bloques basta con que hagas click en la cuadrícula, si haces click sobre un bloque existente lo borras. Si presionas la rueda del ratón podrás desplazar la gráfica
