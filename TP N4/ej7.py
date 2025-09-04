
import numpy as np

# Definimos los símbolos de la BC
symbols = ["a", "b", "c", "d", "e", "f", "g"]
idx = {s: i for i, s in enumerate(symbols)}

# Base de Conocimiento como lista de reglas (premisas, conclusion)
BC = [
    (["b", "c"], "a"),   # R1
    (["d", "e"], "b"),   # R2
    (["g", "e"], "b"),   # R3
    (["e"], "c"),        # R4
    ([], "d"),           # R5 (hecho)
    ([], "e"),           # R6 (hecho)
    (["a", "g"], "f")    # R7
]

# Vector de hechos conocidos (False = no probado, True = probado)
facts = np.zeros(len(symbols), dtype=bool)

# Inicializamos con los hechos dados (reglas sin premisas)
for premises, conclusion in BC:
    if len(premises) == 0:
        facts[idx[conclusion]] = True


def backward_chain_numpy(goal, bc, facts, visited=None):
    """
    Encadenamiento hacia atrás usando numpy
    """
    if visited is None:
        visited = set()

    g_idx = idx[goal]

    # Si ya está probado como hecho
    if facts[g_idx]:
        return True

    # Evitar ciclos
    if goal in visited:
        return False
    visited.add(goal)

    # Buscamos reglas que concluyen el objetivo
    applicable_rules = [rule for rule in bc if rule[1] == goal]

    if not applicable_rules:
        return False

    for premises, conclusion in applicable_rules:
        premises_ok = True
        for p in premises:
            if not backward_chain_numpy(p, bc, facts, visited):
                premises_ok = False
                break
        if premises_ok:
            facts[g_idx] = True
            return True

    return False


# -------------------------
# Probar con el ejercicio 3
# -------------------------
objetivo = "a"
resultado = backward_chain_numpy(objetivo, BC, facts.copy())

print(f"¿Se puede probar que {objetivo} = True?")
print("Resultado:", resultado)
print("Vector de hechos probados:", facts)
