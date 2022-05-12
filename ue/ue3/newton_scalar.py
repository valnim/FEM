# #-------------------------------------------------------------------------#
# # FE-Methods, SS 2020, 3. Unit
# #
# # Script for calculating the root of the function f(x) = x-exp(x) with the
# # Newton-Raphson method
# #-------------------------------------------------------------------------#
import numpy as np

# The different Examples are defined in the following functions
bsp = 3

if bsp == 0:
    n_equations = 1
    # x - e^-x
    f = lambda x: x - np.exp(-x)
    df = lambda x: 1 + np.exp(-x)
    x0 = -3

elif bsp == 1:
    n_equations = 1
    # atan(x)
    f = lambda x: np.arctan(x)
    df = lambda x: 1 / (1 + x**2)
    x0 = np.pi/3  # Good initial guess = pi/3 (converges), bad guess = pi/2 (does not converge, because of instability, overshoots)

elif bsp == 2:
    n_equations = 1
    # 1/2*x^3-3/2*x^2-1
    f = lambda x: 0.5*x**3-1.5*x**2-1
    df = lambda x: 3/2*x**2-3*x
    x0 = 4  # Good Initial Guess = 4 (converges), Bad Initial Guess = 1 (gets stuck in local maximum)

elif bsp == 3:
    n_equations = 4
    # Exercise 2

    def f(x: np.array([4, ])):
        y = np.zeros([4, ])
        y[0] = x[0] + x[1] - 2
        y[1] = x[0] * x[2] + x[1] * x[3]
        y[2] = x[0] * x[2]**2 + x[1] * x[3]**2 - 2/3
        y[3] = x[0] * x[2]**3 + x[1] * x[3]**3
        return y

    def df(x: np.array([4, ])):
        y = np.zeros([4, 4])
        y[0, 0] = 1
        y[0, 1] = 1
        y[1, 0] = x[2]
        y[1, 1] = x[3]
        y[1, 2] = x[0]
        y[1, 3] = x[1]
        y[2, 0] = x[2]**2
        y[2, 1] = x[3]**2
        y[2, 2] = x[0] * x[2] * 2
        y[2, 3] = x[1] * x[3] * 2
        y[3, 0] = x[2]**3
        y[3, 1] = x[3]**3
        y[3, 2] = x[0] * x[2]**2 * 3
        y[3, 3] = x[1] * x[3]**2 * 3
        return y

    x0 = np.array([2, 3, 1, -1])
    # 1, 3, 4, 5 needs 158 iterations to converge
    # 2 ,3 1, -1 needs 6 iterations to converge
    # 2, 2, 2, 2 does not converge because of singularity in the calculation of the inverse




# Setting the initial guess, the maximum number of iterations and the
# convergence criterion (same for increment and residuum)
max_iterations = 300
convergence_criterion = 1e-12

# In the following array, the x-value of each iteration step is stored.
x_arr = np.zeros((n_equations, max_iterations + 1))
x_arr[:, 0] = x0

# In the following arrays, residuum and increment of each iteration step
# are stored.
convergence_residuum = np.ones((1, max_iterations + 1))
convergence_dx = np.ones((1, max_iterations + 1))

for k in range(max_iterations):
    # Implementation of the Newton Raphson method
    x_k = x_arr[:, k]
    delta_x = np.matmul(-np.linalg.inv(np.reshape(df(x_k), (n_equations, n_equations))), np.reshape(f(x_k), (n_equations, 1)))
    x_kp1 = np.reshape(x_k, (n_equations, 1)) + delta_x
    
    # The calculated value is stored
    x_arr[:, k + 1] = x_kp1[:, 0]
    
    # Residuum and increment are stored for the convergence check. The
    # values are normalized with respect to their initial values.
    convergence_residuum[:, k + 1] = np.linalg.norm(f(x_kp1))/np.linalg.norm(f(x0))
    convergence_dx[:, k + 1] = np.linalg.norm(delta_x)/np.linalg.norm(x_arr[:, 1]-x0)
    
    # Convergence is checked
    if convergence_residuum[:, k + 1] < convergence_criterion and convergence_dx[:, k + 1] < convergence_criterion:
        # If both convergence criteria are fulfilled, we can stop the
        # iteration.
        print('Newton method converged at step ', k)
        print('Converged solution:')
        print(x_arr[:, k + 1])
        print('')
        
        break
    elif k + 1 == max_iterations:
        # If there is no convergence after max_iterations iterations, the
        # calculation is aborted and an error is displayed.
        # error('Max Iteration number was reached in Newton-Raphson procedure before convergence was reached')
        for i in range(k + 1):
            print('Iteration #', i, ':')
            print('x =', x_arr[:, i])
            print('Residuum =', convergence_residuum[0, i])
            print('Increment =', convergence_dx[0, i])
            print('')
        raise Exception('Max Iteration number was reached in Newton-Raphson procedure before convergence was reached')


# output in the command window
for i in range(k + 1):
    print('Iteration #', i, ':')
    print('x =', x_arr[:, i])
    print('Residuum =', convergence_residuum[0, i])
    print('Increment =', convergence_dx[0, i])
    print('')


print('finished')



