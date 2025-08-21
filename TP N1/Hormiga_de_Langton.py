import matplotlib.pyplot as plt
from collections import defaultdict
import random

# Parámetros
N_PASOS = 12000
NEGRO, BLANCO = 1, 0
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Las 4 direcciones posibles de la hormiga en el instante inicial
REFRESH = 50
VENTANA = 50  # medio tamaño del área visible

# Posición inicial aleatoria
x = random.randint(-50, 50)
y = random.randint(-50, 50)
d = random.randrange(4)

# Tablero disperso
grid = defaultdict(int)

# Configuración de la ventana
plt.ion()
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-VENTANA, VENTANA)
ax.set_ylim(-VENTANA, VENTANA)
ax.set_title("Hormiga de Langton - Vista fija")

# Simulación
for paso in range(1, N_PASOS + 1):
    col = grid[(x, y)]
    grid[(x, y)] = BLANCO if col == NEGRO else NEGRO

    if col == BLANCO:
        d = (d + 1) % 4
    else:
        d = (d - 1) % 4

    dx, dy = DIRS[d]
    x += dx
    y += dy

    if paso % REFRESH == 0 or paso == N_PASOS:
        ax.clear()
        ax.set_aspect('equal')
        ax.set_xlim(-VENTANA, VENTANA)
        ax.set_ylim(-VENTANA, VENTANA)
        ax.set_title(f"Hormiga de Langton - Paso {paso}")

        # Celdas negras
        negros = [(i, j) for (i, j), c in grid.items() if c == NEGRO]
        if negros:
            xs, ys = zip(*negros)
            ax.scatter(xs, ys, c='black', marker='s', s=10)

        # Hormiga
        ax.scatter([x], [y], c='red', marker='o', s=30)
        plt.draw()
        plt.pause(0.001)

plt.ioff()
plt.show()
