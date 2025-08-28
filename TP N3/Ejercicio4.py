import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Definir la función
f = lambda x: np.sin(x) / (x + 0.1)

# Parámetros
x_min, x_max = -10, -6
x0 = -9.5   # punto inicial
step = 0.5
min_step = 0.1

# Hill climbing paso a paso
def hill_climb_step(x, step):
    candidates = [x - step, x + step]
    candidates = [c for c in candidates if x_min <= c <= x_max]
    if not candidates:
        return x, step
    fvals = [f(c) for c in candidates]
    best_idx = np.argmax(fvals)
    if fvals[best_idx] > f(x):
        return candidates[best_idx], step
    else:
        return x, step / 2  # reducir paso si no mejora

# Preparar la figura
xs = np.linspace(x_min, x_max, 1000)
ys = f(xs)

fig, ax = plt.subplots()
ax.plot(xs, ys, label="f(x) = sin(x)/(x+0.1)")
point, = ax.plot([], [], 'ro', markersize=8)
ax.set_title("Hill Climbing en acción")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()

# Estado global de la animación
state = {"x": x0, "step": step}

# Inicialización del punto en la animación
def init():
    point.set_data([], [])
    return point,

# Función de actualización de cada frame
def update(frame):
    x, step = state["x"], state["step"]
    if step >= min_step:
        new_x, new_step = hill_climb_step(x, step)
        state["x"], state["step"] = new_x, new_step
    point.set_data([state["x"]], [f(state["x"])] )
    return point,

# Animación
ani = animation.FuncAnimation(fig, update, frames=200, init_func=init,
                              blit=True, interval=500, repeat=False)

plt.show()
