import random
import math

# --- Generar vecino ---
def generar_vecino(S, jugador):
    Svecino = S.copy()
    vacias = [i for i, v in enumerate(Svecino) if v == 0]
    if vacias:
        pos = random.choice(vacias)
        Svecino[pos] = jugador
    return Svecino

# --- Función de energía ---
def energia(S):
    lineas = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    
    for linea in lineas:
        valores = [S[i] for i in linea]
        if sum(valores) == 3:   # jugador gana
            return 100
        elif sum(valores) == -3: # computadora gana
            return -100
    
    energia_val = 0
    for linea in lineas:
        valores = [S[i] for i in linea]
        if valores.count(1) > 0 and valores.count(-1) == 0:
            energia_val += valores.count(1)
        elif valores.count(-1) > 0 and valores.count(1) == 0:
            energia_val -= valores.count(-1)
    return energia_val

# --- Computadora hace un movimiento usando recocido simulado ---
def computadora_mueve(S, T0=10, Tf=0.1, alfa=0.9):
    S_actual = S.copy()
    T = T0
    mejor = S_actual.copy()
    
    while T >= Tf:
        vecino = generar_vecino(S_actual, -1)
        dE = energia(vecino) - energia(S_actual)
        if dE < 0 or random.random() < math.exp(-dE / T):
            S_actual = vecino
        if energia(S_actual) < energia(mejor):
            mejor = S_actual.copy()
        T *= alfa
    
    # Solo aplicar un movimiento de diferencia
    for i in range(9):
        if S[i] == 0 and mejor[i] == -1:
            S[i] = -1
            break
    return S

# --- Mostrar tablero ---
def mostrar_tablero(S):
    simbolos = {0: " ", 1: "X", -1: "O"}
    print(f"{simbolos[S[0]]}|{simbolos[S[1]]}|{simbolos[S[2]]}")
    print("-+-+-")
    print(f"{simbolos[S[3]]}|{simbolos[S[4]]}|{simbolos[S[5]]}")
    print("-+-+-")
    print(f"{simbolos[S[6]]}|{simbolos[S[7]]}|{simbolos[S[8]]}")
    print()

# --- Mostrar instrucciones ---
def mostrar_instrucciones():
    print("¡Bienvenido al Tatetí!")
    print("Jugarás con X, la computadora con O.")
    print("El tablero se numera así:")
    print("0 | 1 | 2")
    print("---------")
    print("3 | 4 | 5")
    print("---------")
    print("6 | 7 | 8")
    print("Para hacer tu jugada, ingresa el número de la casilla deseada.\n")

# --- Verificar ganador ---
def ganador(S):
    lineas = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for linea in lineas:
        valores = [S[i] for i in linea]
        if sum(valores) == 3:
            return 1  # jugador gana
        elif sum(valores) == -3:
            return -1  # computadora gana
    if 0 not in S:
        return 0  # empate
    return None  # nadie gana todavía

# --- Juego interactivo ---
def jugar():
    mostrar_instrucciones()
    S = [0]*9
    turno_jugador = True
    
    while True:
        mostrar_tablero(S)
        
        if turno_jugador:
            try:
                jugada = int(input("Introduce tu jugada (0-8): "))
                if S[jugada] != 0:
                    print("Casilla ocupada, elige otra.\n")
                    continue
                S[jugada] = 1
            except (ValueError, IndexError):
                print("Entrada inválida. Debe ser un número del 0 al 8.\n")
                continue
        else:
            print("Turno de la computadora...")
            S = computadora_mueve(S)
        
        resultado = ganador(S)
        if resultado is not None:
            mostrar_tablero(S)
            if resultado == 1:
                print("¡Felicidades, ganaste!")
            elif resultado == -1:
                print("La computadora ganó.")
            else:
                print("Empate.")
            break
        
        turno_jugador = not turno_jugador

# --- Iniciar juego ---
if __name__ == "__main__":
    jugar()
