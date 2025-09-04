import numpy as np

# ---------------------------------------------------
# Mapeo de símbolos a índices
# a=0, b=1, c=2, d=3, e=4, f=5, g=6
n = 7  

# Hechos iniciales (d=3, e=4 verdaderos)
hechos = np.array([0, 0, 0, 1, 1, 0, 0], dtype=bool)

# Reglas del ejercicio 3
# Antecedentes
premisas = np.array([
    [0, 1, 1, 0, 0, 0, 0],  # R1: b ∧ c
    [0, 0, 0, 1, 1, 0, 0],  # R2: d ∧ e
    [0, 0, 0, 0, 1, 0, 1],  # R3: g ∧ e
    [0, 0, 0, 0, 1, 0, 0],  # R4: e
    [1, 0, 0, 0, 0, 0, 1],  # R7: a ∧ g
], dtype=bool)

# Conclusiones
conclusiones = np.array([
    [1, 0, 0, 0, 0, 0, 0],  # R1 → a
    [0, 1, 0, 0, 0, 0, 0],  # R2 → b
    [0, 1, 0, 0, 0, 0, 0],  # R3 → b
    [0, 0, 1, 0, 0, 0, 0],  # R4 → c
    [0, 0, 0, 0, 0, 1, 0],  # R7 → f
], dtype=bool)

nombres = ["a", "b", "c", "d", "e", "f", "g"]

# ---------------------------------------------------
# Encadenamiento hacia adelante con traza
def encadenar(hechos, premisas, conclusiones, nombres):
    hechos = hechos.copy()
    cambio = True
    paso = 1
    while cambio:
        cambio = False
        for i in range(len(premisas)):
            if np.all(hechos[premisas[i]]):
                nuevos = conclusiones[i] & ~hechos
                if np.any(nuevos):
                    hechos = hechos | nuevos
                    concl = [nombres[j] for j in range(len(hechos)) if nuevos[j]]
                    print(f"Paso {paso}: dispara R{i+1}, se agrega {concl}")
                    paso += 1
                    cambio = True
    print("\nHechos finales:", [nombres[i] for i, v in enumerate(hechos) if v])

# ---------------------------------------------------
# Prueba 1: hechos iniciales {d, e}
print("PRUEBA 1: hechos iniciales {d, e}")
encadenar(np.array([0,0,0,1,1,0,0], dtype=bool), premisas, conclusiones, nombres)

# Prueba 2: hechos iniciales {d, e, g}
print("\nPRUEBA 2: hechos iniciales {d, e, g}")
encadenar(np.array([0,0,0,1,1,0,1], dtype=bool), premisas, conclusiones, nombres)