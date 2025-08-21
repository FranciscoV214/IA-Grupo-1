import matplotlib.pyplot as plt
import heapq

# --- Definimos la grilla ---
grid = [[0]*20 for _ in range(20)]

# Dibujamos la pared (forma de L)
grid[3][8] = 1
grid[2][9] = 1
for y in range(4, 13):
    grid[y][7] = 1
for x in range(7, 11):
    grid[12][x] = 1

# --- Función para mostrar la grilla y elegir puntos ---
def elegir_puntos():
    while True:
        fig, ax = plt.subplots(figsize=(6,6))
        ax.set_xticks(range(len(grid[0])))
        ax.set_yticks(range(len(grid)))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True)

        # Dibujar paredes
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color="black"))

        plt.gca().invert_yaxis()
        plt.title("Click en la grilla: primero inicio (azul), luego fin (amarillo)")
        plt.draw()

        pts = plt.ginput(2)  # usuario elige 2 puntos
        plt.close()

        start = (int(pts[0][1]), int(pts[0][0]))
        goal  = (int(pts[1][1]), int(pts[1][0]))

        # Validación: no puede estar sobre paredes
        if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
            print("¡Elegiste una celda ocupada por una pared! Probá de nuevo.")
        else:
            return start, goal

# Elegir puntos válidos
start, goal = elegir_puntos()

# --- A* ---
moves = [(-1,0), (1,0), (0,-1), (0,1)]

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan

def astar(grid, start, goal):
    filas, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (heuristic(start,goal), 0, start, [start]))
    visitados = set()

    while open_set:
        f, g, nodo, path = heapq.heappop(open_set)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        if nodo == goal:
            return path
        for dx, dy in moves:
            nx, ny = nodo[0]+dx, nodo[1]+dy
            if 0 <= nx < filas and 0 <= ny < cols and grid[nx][ny] == 0:
                heapq.heappush(open_set, (g+1+heuristic((nx,ny), goal), g+1, (nx,ny), path+[(nx,ny)]))
    return None

camino = astar(grid, start, goal)

# --- Dibujar resultado ---
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xticks(range(len(grid[0])))
ax.set_yticks(range(len(grid)))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 1:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color="black"))

# Dibujar inicio y fin
ax.add_patch(plt.Rectangle((start[1], start[0]), 1, 1, color="blue"))
ax.add_patch(plt.Rectangle((goal[1], goal[0]), 1, 1, color="yellow"))

# Dibujar camino con g(n), h(n), f(n)
if camino:
    print("\nCamino encontrado con A*:")
    for paso, nodo in enumerate(camino):
        g = paso
        h = heuristic(nodo, goal)
        f = g + h
        print(f"nodo={nodo} | g(n)={g} | h(n)={h} | f(n)={f}")

        # Colorear el camino
        ax.add_patch(plt.Rectangle((nodo[1], nodo[0]), 1, 1, color="cyan", alpha=0.5))
        # Escribir g,h dentro de la celda
        ax.text(nodo[1]+0.5, nodo[0]+0.3, f"g={g}", ha="center", va="center", fontsize=6, color="black")
        ax.text(nodo[1]+0.5, nodo[0]+0.7, f"h={h}", ha="center", va="center", fontsize=6, color="red")

    print(f"\nCosto total del camino (g): {len(camino)-1}")
else:
    print("No se encontró un camino posible.")

plt.gca().invert_yaxis()
plt.title("Camino encontrado con A* (con g(n) y h(n))")
plt.show()
