import random

# ---------------------
# DATOS
# ---------------------
precios = [100, 50, 115, 25, 200, 30, 40, 100, 100, 100]
pesos   = [300, 200, 450, 145, 664, 90, 150, 355, 401, 395]
C = 1000
n = len(precios)

# ---------------------
# AUXILIARES
# ---------------------
def peso_total(ind):
    return sum(pesos[i] * ind[i] for i in range(n))

def precio_total(ind):
    return sum(precios[i] * ind[i] for i in range(n))

def fitness(ind):
    return precio_total(ind)

# ---------------------
# CREAR POBLACIÓN
# ---------------------
def crear_individuo():
    while True:
        ind = [random.randint(0,1) for _ in range(n)]
        if peso_total(ind) <= C:
            return ind

def crear_poblacion(N=20):
    return [crear_individuo() for _ in range(N)]

# ---------------------
# SELECCIÓN RULETA (ÍNDICE)
# ---------------------
def seleccion_ruleta_index(poblacion):
    fits = [fitness(ind) for ind in poblacion]
    total = sum(fits)
    if total == 0:
        return random.randrange(len(poblacion))
    pick = random.uniform(0, total)
    acum = 0.0
    for idx, val in enumerate(fits):
        acum += val
        if acum >= pick:
            return idx
    return len(poblacion)-1

# ---------------------
# OPERADORES GENÉTICOS
# ---------------------
def cruce(p1, p2):
    punto = random.randint(1, n-1)
    return (p1[:punto] + p2[punto:], p2[:punto] + p1[punto:])

def mutacion(ind, prob=0.2):
    ind = ind.copy()
    for i in range(n):
        if random.random() < prob:
            ind[i] = 1 - ind[i]
    return ind

def reparar(ind):
    ind = ind.copy()
    while peso_total(ind) > C:
        idx = random.choice([i for i, g in enumerate(ind) if g == 1])
        ind[idx] = 0
    return ind

# ---------------------
# ALGORITMO GENÉTICO
# ---------------------
def algoritmo_genetico(N=20, generaciones=100, prob_mut=0.2):
    poblacion = crear_poblacion(N)
    idx0 = max(range(len(poblacion)), key=lambda i: fitness(poblacion[i]))
    mejor_global = poblacion[idx0].copy()

    for _ in range(generaciones):
        nueva_pob = []
        for _ in range(N//2):
            i1 = seleccion_ruleta_index(poblacion)
            i2 = seleccion_ruleta_index(poblacion)
            while i2 == i1:
                i2 = seleccion_ruleta_index(poblacion)
            p1, p2 = poblacion[i1], poblacion[i2]
            h1, h2 = cruce(p1, p2)
            h1 = reparar(mutacion(h1, prob_mut))
            h2 = reparar(mutacion(h2, prob_mut))
            nueva_pob.extend([h1, h2])
        poblacion = nueva_pob
        mejor_gen = max(poblacion, key=fitness)
        if fitness(mejor_gen) > fitness(mejor_global):
            mejor_global = mejor_gen.copy()

    print("\n=== RESULTADO FINAL ===")
    print(f"Mejor individuo: {mejor_global}")
    print(f"Peso total: {peso_total(mejor_global)}")
    print(f"Precio total: {precio_total(mejor_global)}")

# Ejecutar
algoritmo_genetico(N=20, generaciones=100)
