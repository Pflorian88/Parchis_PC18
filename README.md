# Juego de Parchís en Python 

Este es nuestro proyecto final para el curso de programación de computadores en Python.
Implementaré el juego de Parchís utilizando Python.

README – Proyecto Parqués UN-Grupo 14
Materia: Programación de Computadores
Universidad Nacional de Colombia — 2025-I
Docente: Gustavo Adolfo Mojica Perdigón

Integrantes:
- Ana Sofia Aponte Padilla – Ingeniería Mecánica
- Pedro Leon Florian Sanchez – Ingeniería Civil 
- Gabriel Jeronimo Laureano Navarro – Ingeniería Mecánica 

----------------------------------------
¿CÓMO EJECUTAR EL PROGRAMA?
----------------------------------------

1. Pre-requisitos:
   Asegúrate de tener instalado Python 3.9 o superior.
   Verifica la versión ejecutando el siguiente comando en la terminal:

   python --version

2. Clona o descarga el repositorio:
   Puedes clonar el repositorio con el siguiente comando:

   git clone https://github.com/usuario/parques-un.git

   O descarga el archivo .zip desde GitHub, descomprímelo y abre la carpeta.

3. Estructura de archivos esperada:

   parques-un/

   ├── main.py

   ├── Tablero.py

   ├── Logica.py

   ├── Interfaz.py

   └── README.txt

5. Ejecutar el programa:
   Abre una terminal o línea de comandos, navega hasta la carpeta del proyecto y ejecuta:

   python main.py

6. Modo de juego:
   - El programa solicita cuántos jugadores participarán (entre 2 y 4).
   - Cada jugador debe ingresar su nombre.
   - En cada turno, el programa lanza dos dados y muestra las posibles acciones.
   - Las reglas de Parqués se aplican (capturas, entrada a la meta, bonus, pares).
   - El juego finaliza cuando un jugador lleva todas sus fichas a la meta.

----------------------------------------
MODO DESARROLLADOR (OPCIONAL)
----------------------------------------

Puedes activar el modo desarrollador editando el archivo main.py
y cambiando la siguiente línea:

MODO_DESARROLLADOR = False

por:

MODO_DESARROLLADOR = True

Esto te permitirá ingresar manualmente los valores de los dados para probar casos específicos.

----------------------------------------
ENLACE AL VIDEO EXPLICATIVO
----------------------------------------

https://www.youtube.com/watch?v=7AuOWuBg_ZY
