# #-------------------------------------------------------------------------#
# # FE-Methods, SS 2020, 3. Unit
# #
# # Script for calculating the root of the function f(x) = x-exp(x) with the
# # Newton-Raphson method
# #-------------------------------------------------------------------------#
import numpy as np
import matplotlib.pyplot as plt

# Set the number of equations to solve
n_equations = 1

# In the scalar case, the function and its derivative can be implemented
# directly via function handles. For nonlinear equation systems, the
# functions are defined in files on their own.
f = lambda x: x - np.exp(-x)
df = lambda x: 1 + np.exp(-x)

# Setting the initial guess, the maximum number of iterations and the
# convergence criterion (same for increment and residuum)
x0 = -3
max_iterations = 15
convergence_criterion = 1e-12

# In the following array, the x-value of each iteration step is stored.
x_arr = np.zeros((n_equations, max_iterations + 1))
x_arr[:, 0] = x0

# % x- and y values for the plot are calculated
# x = linspace(-3.5,1.5,1001);
# y = arrayfun(f,x);
x = np.linspace(-3.5, 1.5, 1001)
y = np.array([f(i) for i in x])

# x axis and initial guess are plotted.
plt.plot(x, y)
plt.plot(x0, f(x0), 'ro')
plt.plot([x[0], x[-1]], [0, 0], 'k-')
plt.plot([x0, x0], [0, f(x0)], 'r')
plt.legend(['f(x)'])

# In the following arrays, residuum and increment of each iteration step
# are stored.
convergence_residuum = np.ones((1, max_iterations + 1))
convergence_dx = np.ones((1, max_iterations + 1))

for k in range(max_iterations):
    # wait for key press
    #input("Press Enter to continue...")
    # Implementation of the Newton Raphson method
    x_k = x_arr[:, k]
    delta_x = -np.linalg.inv(np.reshape(df(x_k), (n_equations, n_equations))) * np.reshape(f(x_k), (n_equations, n_equations))
    x_kp1 = x_k + delta_x

    # The calculated value is stored
    x_arr[:, k + 1] = x_kp1

    # The calculated value is plotted
    plt.plot([x_k[0], x_kp1[0, 0]], [f(x_k)[0], 0], 'grey')
    plt.plot([x_kp1[0, 0], x_kp1[0, 0]], [0, f(x_kp1)[0, 0]], 'r')
    plt.plot(x_kp1[0, 0], f(x_kp1)[0, 0], 'r*')

plt.show()
