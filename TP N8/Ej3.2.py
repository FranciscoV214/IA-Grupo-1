import numpy as np
import matplotlib.pyplot as plt

N_TOTAL = 23   #puntos totales
MIN_VALOR = 0.0
MAX_VALOR = 5.0
N_PUNTOS_KM = 20 #puntos para el K-means
N_CLUSTERS = 2  #cantidad de semillas

# Genera los 23 puntos
x_coords = np.random.uniform(low=MIN_VALOR, high=MAX_VALOR, size=N_TOTAL)
y_coords = np.random.uniform(low=MIN_VALOR, high=MAX_VALOR, size=N_TOTAL)
puntos_totales = np.column_stack((x_coords, y_coords))

plt.figure(figsize=(10,10)) 

plt.scatter(x_coords, y_coords, color='blue', marker='o', alpha=0.7, s=50)

# Añade etiquetas y título
plt.title(f'Distribución de {N_TOTAL} Puntos Aleatorios en $[{MIN_VALOR}, {MAX_VALOR}] \\times [{MIN_VALOR}, {MAX_VALOR}]$')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')

# Establece los límites de los ejes para que coincidan con el rango [0, 5] y un poco de margen
plt.xlim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)
plt.ylim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
# Selecciona los 20 puntos para K-Means
puntos_km = puntos_totales[:N_PUNTOS_KM]
puntos_knn = puntos_totales[N_PUNTOS_KM:]

# Inicializa los centroides con las 2 primeras semillas
centroides = puntos_km[:N_CLUSTERS].copy()
print(f"Centroides Iniciales (Semillas):\n{centroides}")

#  Implementación del Algoritmo K-Means

MAX_ITERACIONES = 20
TOLERANCIA = 1e-4 # tolerancia de variacion entre centroides para actualizar

# Función para calcular la distancia euclidiana al cuadrado
def distancia_cuadrada(punto_a, punto_b):
    return np.sum((punto_a - punto_b)**2)

# Bucle principal del algoritmo K-Means
for iteracion in range(MAX_ITERACIONES):
    # clasificacion, crea un array para almacenar la etiqueta (0 o 1) de cada punto
    etiquetas = np.empty(N_PUNTOS_KM, dtype=int)

    for i, punto in enumerate(puntos_km):
        distancias = [distancia_cuadrada(punto, centroide) for centroide in centroides]
        # Asigna el punto al centroide más cercano
        etiquetas[i] = np.argmin(distancias)

    # Guarda los centroides actuales para calcular la variación al final
    centroides_antiguos = centroides.copy()
    
    # Actualización (Ponderación para nuevo centroide)
    for k in range(N_CLUSTERS):
        # Filtra todos los puntos que pertenecen al cluster k
        puntos_en_cluster = puntos_km[etiquetas == k]
        
        if len(puntos_en_cluster) > 0:
            # Calcula el nuevo centroide como el promedio de todos los puntos del grupo
            centroides[k] = np.mean(puntos_en_cluster, axis=0)
        else:
            # Si un cluster está vacío, mantenemos el centroide donde estaba
            print(f"Advertencia: Cluster {k} vacío en la iteración {iteracion+1}")
            
    # Calcula la variación total (distancia entre los centroides antiguos y nuevos)
    variacion = np.sum([distancia_cuadrada(centroides[k], centroides_antiguos[k]) for k in range(N_CLUSTERS)])

    print(f"Iteración {iteracion+1}: Variación = {variacion:.6f}")

    if variacion < TOLERANCIA:
        print(f"\nConvergencia alcanzada en la iteración {iteracion + 1}.")
        break
else:
    print(f"\nAlgoritmo detenido después de alcanzar el máximo de {MAX_ITERACIONES} iteraciones.")

centroides_finales = centroides

# Graficar

plt.figure(figsize=(10, 10))

# los 20 puntos clasificados
colores = ['red', 'blue']
for i in range(N_CLUSTERS):
    puntos_grupo = puntos_km[etiquetas == i]
    plt.scatter(
        puntos_grupo[:, 0],
        puntos_grupo[:, 1],
        s=80,
        c=colores[i],
        marker='o',
        alpha=0.7,
        label=f'Grupo {i+1} ({len(puntos_grupo)} puntos)'
    )

# graficar los centroides finales
plt.scatter(
    centroides_finales[:, 0],
    centroides_finales[:, 1],
    s=300,
    c='black',
    marker='*',
    edgecolors='white',
    label='Centroides Finales'
)

# Graficar los 3 puntos no utilizados
puntos_no_usados = puntos_totales[N_PUNTOS_KM:]
if len(puntos_no_usados) > 0:
    plt.scatter(
        puntos_no_usados[:, 0],
        puntos_no_usados[:, 1],
        s=30,
        c='gray',
        marker='x',
        alpha=0.4,
        label='Puntos No Usados'
    )

# Configuración del gráfico
plt.title(f'K-Means con {iteracion+1} Iteraciones')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.xlim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)
plt.ylim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

#funcion knn 
def clasificar_knn_manual(punto_test, puntos_entrenamiento, etiquetas_entrenamiento, k_vecinos):
    """Clasifica un punto usando el voto de los K vecinos más cercanos."""
    # Reutilizamos distancia_cuadrada definida previamente
    distancias = np.array([distancia_cuadrada(punto_test, p) for p in puntos_entrenamiento])

    # Obtener los índices de los K vecinos más cercanos
    indices_vecinos = np.argsort(distancias)[:k_vecinos]

    # Obtener las etiquetas (grupos) de esos K vecinos
    etiquetas_vecinos = etiquetas_entrenamiento[indices_vecinos]

    # Contar la frecuencia de cada etiqueta (0 y 1)
    conteo_votos = np.bincount(etiquetas_vecinos, minlength=N_CLUSTERS)
    
    # Asignar la etiqueta con la mayoría de votos
    return np.argmax(conteo_votos)

# Solicitar el valor de K al usuario
while True:
    try:
        K_VECINOS = int(input("\nIngrese un valor impar para K (e.g., 3, 5, 7) para la clasificación KNN: "))
        if K_VECINOS % 2 != 0 and K_VECINOS > 0 and K_VECINOS <= N_PUNTOS_KM:
            break
        else:
            print(f"K={K_VECINOS} no es válido. Debe ser un número entero impar, positivo y menor o igual a {N_PUNTOS_KM}.")
    except ValueError:
        print("Entrada inválida. Ingrese un número.")

# Clasificar los 3 puntos restantes
etiquetas_knn = np.empty(len(puntos_knn), dtype=int)

for i, punto in enumerate(puntos_knn):
    etiquetas_knn[i] = clasificar_knn_manual(
        punto, puntos_km, etiquetas, K_VECINOS
    )
# Combinar todas las etiquetas para la Figura 3
etiquetas_finales = np.concatenate((etiquetas, etiquetas_knn))

plt.figure(figsize=(10, 10))

for i in range(N_CLUSTERS):
 # Graficamos los 23 puntos usando las etiquetas finales (K-Means + KNN)
 puntos_grupo = puntos_totales[etiquetas_finales == i]
 
 plt.scatter(
 puntos_grupo[:, 0],
 puntos_grupo[:, 1],
 s=80,
 c=colores[i],
 marker='o',
 alpha=0.7,
 label=f'Grupo {i+1} (Total: {len(puntos_grupo)} puntos)'
 )

# Graficar los centroides finales
plt.scatter(
 centroides_finales[:, 0],
 centroides_finales[:, 1],
 s=300,
 c='black',
 marker='*',
 edgecolors='white',
 label='Centroides Finales'
)

plt.title(f'Figura 3: Clasificación Final (K-Means + KNN con K={K_VECINOS})')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.xlim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)
plt.ylim(MIN_VALOR - 0.5, MAX_VALOR + 0.5)
plt.grid(True, linestyle='--', alpha=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.show() # Muestra la tercera figura
