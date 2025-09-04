import numpy as np


variables = ['a','b','c','d','e','f','g']
ind = {variables[i]: i for i in range(len(variables))} #me da los indices de las variables ind[a]=0, ind [b]=1..
n = len(variables) 
reglas = [
    ([ind['b'], ind['c']], ind['a'], 'R1: b ∧ c → a'),
    ([ind['d'], ind['e']], ind['b'], 'R2: d ∧ e → b'),
    ([ind['g'], ind['e']],ind['b'], 'R3: g ∧ e → b'),
    ([ind['e']],           ind['c'], 'R4: e → c'),
    ([],                  ind['d'], 'R5: d (True)'),
    ([],                  ind['e'], 'R6: e (True)'),
    ([ind['a'], ind['g']], ind['f'], 'R7: a ∧ g → f'),
]

known = np.zeros(n, dtype=bool)   # lo que vamos derivando 
neg = np.zeros(n, dtype=bool)     # supuestos negativos

neg[ind['a']] = True   #supuesto de que -a 

cambio = True
while cambio:
    cambio = False
    for ants, cons, name in reglas:  #recorremos reglas
        if not known[cons]: # comprueba que no se encuentre un derivado
            ok = True # si se encontro saltamos a la siguiente linea
            for a in ants:
                if not known[a]:  # si el antecedente no esta derivado no puedo disparar la regla
                    ok = False
                    break #salgo del for para no seguir comprobando esa linea
            if ok: 
                known[cons] = True #ponemos el consecuente derivado
                print(f"{name} disparó -> derivado '{variables[cons]}'")
                cambio = True #actualizo cambio a true para entrar de nuevo a while y repasar de nuevo Reglas
                # Verificamos contradicción
                if neg[cons]:
                    print(f"Contradicción detectada Se ha derivado '{variables[cons]}' mientras ¬{variables[cons]} estaba asumido.")
                    print(f"Resultado: BC ∪ {{¬a}} es inconsistente => por contradicción, 'a' es consecuencia de la BC.")
                    exit()