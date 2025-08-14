import numpy as np
import time
import matplotlib.pyplot as plt

# Parámetros
filas, columnas = 50, 50
tablero = np.zeros((filas, columnas))
simulando = False

def dibujar_tablero(ax, tablero, titulo):
    """Función auxiliar para dibujar el tablero con cuadrícula."""
    ax.cla()
    ax.imshow(tablero, cmap='binary')
    ax.set_title(titulo)
    
    # Dibuja la cuadrícula
    ax.set_xticks(np.arange(-.5, columnas, 1), minor=True)
    ax.set_yticks(np.arange(-.5, filas, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)
    
    # Ajusta los límites y oculta las etiquetas de los ejes
    ax.set_xlim(-0.5, columnas - 0.5)
    ax.set_ylim(-0.5, filas - 0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

def jugar_vida_conway(tablero_inicial, num_iteraciones):
    """
    Simula el Juego de la Vida de Conway.
    """
    tablero = tablero_inicial.copy()
    
    for _ in range(num_iteraciones):
        nuevo_tablero = tablero.copy()
        
        for i in range(tablero.shape[0]):
            for j in range(tablero.shape[1]):
                vecinos_vivos = np.sum(tablero[max(0, i-1):min(tablero.shape[0], i+2),
                                               max(0, j-1):min(tablero.shape[1], j+2)]) - tablero[i, j]
                
                if tablero[i, j] == 1:
                    if vecinos_vivos < 2 or vecinos_vivos > 3:
                        nuevo_tablero[i, j] = 0
                else:
                    if vecinos_vivos == 3:
                        nuevo_tablero[i, j] = 1
        
        tablero = nuevo_tablero
        yield tablero

def on_click(event):
    """Función para manejar los clics del ratón."""
    global tablero, simulando
    if not simulando and event.xdata is not None and event.ydata is not None:
        # Redondeamos los valores para que el clic caiga en el centro de la celda
        x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
        if 0 <= x < columnas and 0 <= y < filas:
            tablero[y, x] = 1 - tablero[y, x]  # Alternar estado (0 a 1 o 1 a 0)
            dibujar_tablero(ax, tablero, "Modo Edición: Clic para crear celdas. Presiona 'Enter' para iniciar.")
            plt.draw()

def on_key(event):
    """Función para manejar la tecla 'Enter'."""
    global simulando
    if not simulando and event.key == 'enter':
        simulando = True
        print("Simulación iniciada...")
        
        # Ocultamos la barra de herramientas al iniciar la simulación
        try:
            fig.canvas.toolbar.pack_forget()
        except AttributeError:
            pass # Para versiones de Matplotlib sin barra de herramientas

        # Bucle de la simulación
        for i, estado in enumerate(jugar_vida_conway(tablero, 150)):
            dibujar_tablero(ax, estado, f'Iteración: {i + 1}')
            plt.draw()
            plt.pause(0.01)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    dibujar_tablero(ax, tablero, "Modo Edición: Clic para crear celdas. Presiona 'Enter' para iniciar.")
    plt.show()