import numpy as np
import plotly.express as px


def newton_raphson(f, df, x0):
    # solver parameters
    max_iter = 100
    convergence_criterion = 1e-12
    convergence_residuum = np.zeros((max_iter + 1))
    convergence_dx = np.zeros((max_iter + 1))

    x_arr = np.zeros((x0.shape[0], max_iter + 1))
    x_arr[:, 0] = x0
    for idx in range(max_iter):
        x_k = x_arr[:, idx]
        delta_x = np.linalg.lstsq(-df(x_k), f(x_k), rcond=None)[0]
        x_kp1 = x_k + delta_x

        x_arr[:, idx + 1] = x_kp1

        convergence_residuum[idx + 1] = np.linalg.norm(f(x_kp1)) / np.linalg.norm(f(x_arr[:, 0]))
        convergence_dx[idx + 1] = np.linalg.norm(delta_x) / np.linalg.norm(x_arr[:, 1] - x0)

        if convergence_residuum[idx + 1] < convergence_criterion and convergence_dx[idx + 1] < convergence_criterion:
            print(f"Solution found at f({x_arr[:, idx + 1]}) = {f(x_arr[:, idx + 1])}")
            break
        elif idx == max_iter - 1:
            print(f"Max iterations reached. Aborting at idx = {idx}.")
            break


### Exercise 1:
# a) converges only if x0 is approx. below 1.3 otherwise it leads to an overflow
x0_1 = np.array([1.3])
f_1 = lambda x: np.array([np.arctan(x)])
df_1 = lambda x: np.array([1 / (x**2 + 1)])
newton_raphson(f_1, df_1, x0_1)

# x_1_linspace = np.linspace(-10.0, 10.0, 10000)
# fig = px.line(x=x_1_linspace, y=f_1(x_1_linspace))
# fig.show()

# b) converges very easily, except when x0 is set in an are where the function is very flat, as the derivative will be
# extremly large (for example at x0 = 2)
x0_2 = np.array([10])
f_2 = lambda x: np.array([1/2 * x**3 - 3/2 * x**2 - 1])
df_2 = lambda x: np.array([3/2 * x**2 - 3 * x])
newton_raphson(f_2, df_2, x0_2)

# x_2_linspace = np.linspace(-5.0, 5.0, 10000)
# fig = px.line(x=x_2_linspace, y=f_2(x_2_linspace))
# fig.show()

### Exercise 2:
x0_3 = np.array([10, 10, 10, 10])
f_3 = lambda x: np.array([
    x[0] + x[1] - 2,
    x[2] * x[0] + x[3] * x[1],
    x[2]**2 * x[0] + x[3]**2 * x[1] - 2/3,
    x[2]**3 * x[0] + x[3]**3 * x[1]
])
df_3 = lambda x: np.array([
    [1, 1, 0, 0],
    [x[2], x[3], x[0], x[1]],
    [x[2]**2, x[3]**2, 2 * x[2] * x[0], 2 * x[3] * x[1]],
    [x[2]**3, x[3]**3, 3 * x[2]**2 * x[0], 2 * x[3]**2 * x[1]]
])
newton_raphson(f_3, df_3, x0_3)

# good intitial guess: [1, 1, 1, 1]
# bad intial guess: [10, 10, 10, 10] (if it gets too big)

