import heapq, math
from collections import defaultdict

graph = { 
    #Casillas a las que puede moverse
    'A': ['B','C'],
    'B': ['D','A'],
    'C': ['A','K'],
    'D': ['B','K'],
    'E': ['N'],
    'F': ['M'],
    'G': ['I','P'],
    'I': ['G','Q','W'],
    'K': ['W','M','T'],
    'M': ['K','D','N','F'],
    'N': ['M','E'],
    'P': ['G','Q'],
    'Q': ['I','P','R'],
    'R': ['Q','T'],
    'T': ['K','R'],
    'W': ['I','K'],
}

# costo por ENTRAR a la casilla (W=30, resto=1)
costs = defaultdict(lambda: 1)
costs['W'] = 30

# coordenadas para Manhattan (según el tablero)
coords = {
    'A': (0,1), 'B': (0,2),
    'C': (1,1), 'D': (1,2), 'E': (1,3),
    'G': (2,0), 'I': (2,1), 'W': (2,2), 'K': (2,3), 'M': (2,4), 'N': (2,5),
    'P': (3,0), 'Q': (3,1), 'R': (3,2), 'T': (3,3), 'F': (3,4)
}
def h(n, goal='F'):
    x1,y1 = coords[n]; x2,y2 = coords[goal]
    return abs(x1-x2) + abs(y1-y2)

start, goal = 'I', 'F'

# 1) DFS (stack LIFO). Para desempate alfabético: push en orden inverso.
def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in visited: continue
        visited.add(node)
        for nb in sorted(graph[node], reverse=True):
            stack.append((nb, path+[nb]))
    return None

# 2) Greedy Best-First (solo heurística)
def greedy(start, goal):
    pq = [(h(start,goal), [start])]
    visited = set()
    while pq:
        _, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal: return path
        if node in visited: continue
        visited.add(node)
        for nb in sorted(graph[node]):  # En caso de empate se maneja por alfabeto
            heapq.heappush(pq, (h(nb,goal), path+[nb]))
    return None

# 3) A* (f=g+h) con costos (W=30)
def astar(start, goal):
    pq = [(h(start,goal), 0, [start])]
    best_g = {start: 0}
    while pq:
        f, g, path = heapq.heappop(pq)
        node = path[-1]
        if node == goal: return path, g
        if g > best_g.get(node, math.inf): continue
        for nb in sorted(graph[node]):  # en caso de empate se maneja por alfabeto
            ng = g + costs[nb]
            if ng < best_g.get(nb, math.inf):
                best_g[nb] = ng
                heapq.heappush(pq, (ng + h(nb,goal), ng, path+[nb]))
    return None, None
print("\n")
print("DFS   :", dfs(start, goal)," \nElige el camino por profundidad y en caso de empate por alfabeto\n")
print("Greedy:", greedy(start, goal),"\nBusqueda heuristica, prioriza el camino mas corto, en caso de empate elige por alfabeto\n")
path, cost = astar(start, goal)
print("A*    :", path, "\nCada casilla tiene un costo Real, prioriza el menor costo, en caso de empate elige por alfabeto""costo:", cost)
