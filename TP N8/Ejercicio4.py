import numpy as np

# Número de salas
n_states = 6  

# Matriz de recompensas R
R = np.array([
    [0, 0, -1, -1, -1, -1],
    [0, 0, 0, -1, -1, -1],
    [-1, 0, 0, 0, -1, 100],
    [0, -1, 0, 0, 0, -1],
    [-1, -1, -1, 0, 0, 100],
    [-1, -1, 0, -1, 0, 100]
])

# Matriz Q inicializada en ceros
Q = np.zeros((n_states, n_states))

# Parámetros
gamma = 0.9   # factor de descuento
alpha = 0.1   # tasa de aprendizaje
epochs = 10000

# Q-Learning
for _ in range(epochs):
    # elegir estado inicial aleatorio
    state = np.random.randint(0, n_states) # estado inicial aleatorio, me posiciono en un elemento de la matriz aleatorio.
    
    # encontrar acciones posibles
    possible_actions = np.where(R[state] >= 0)[0] #desde el estado inicial, se fija a donde puede ir, elige números mayores o iguales a 0 (pueden ser 100 o 0)
    
    action = np.random.choice(possible_actions) #elige alguno de los caminos a los que puede ir aleatoriamente.
    
    next_state = action #el camino elegido es el próximo estado.
    
    # actualizar Q
    Q[state, action] = Q[state, action] + alpha * (R[state, action] + gamma * (np.max(Q[next_state]) - Q[state, action]))

# Configuración para que NumPy muestre todas las filas y columnas sin cortar
np.set_printoptions(suppress=True, linewidth=150, precision=2)
print("Matriz de Recompensas R:")
print(R)
print("\n")

print("Matriz Q entrenada:")
print(Q)
print("\n")

# Normalización para interpretar mejor
print("\nMatriz Q normalizada:")
print(Q / np.max(Q))