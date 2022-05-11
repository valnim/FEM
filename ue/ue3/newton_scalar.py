# #-------------------------------------------------------------------------#
# # FE-Methods, SS 2020, 3. Unit
# #
# # Script for calculating the root of the function f(x) = x-exp(x) with the
# # Newton-Raphson method
# #-------------------------------------------------------------------------#
import numpy as np

# Set the number of equations to solve
n_equations = 1

# In the scalar case, the function and its derivative can be implemented
# directly via function handles. For nonlinear equation systems, the
# functions are defined in files on their own.
bsp = 1

if bsp == 0:
    # x - e^-x
    f = lambda x: x - np.exp(-x)
    df = lambda x: 1 + np.exp(-x)
    x0 = -3

elif bsp == 1:
    # atan(x)
    f = lambda x: np.arctan(x)
    df = lambda x: 1 / (1 + x**2)
    x0 = np.pi/3  # Good initial guess = pi/3 (converges), bad guess = pi/2 (does not converge, because of instability, overshoots)

elif bsp == 2:
    # 1/2*x^3-3/2*x^2-1
    f = lambda x: 0.5*x**3-1.5*x**2-1
    df = lambda x: 3/2*x**2-3*x
    x0 = 4  # Good Initial Guess = 4 (converges), Bad Initial Guess = 1 (gets stuck in local maximum)


# Setting the initial guess, the maximum number of iterations and the
# convergence criterion (same for increment and residuum)
max_iterations = 15
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
    delta_x = -np.linalg.inv(np.reshape(df(x_k), (n_equations, n_equations))) * np.reshape(f(x_k), (n_equations, n_equations))
    x_kp1 = x_k + delta_x
    
    # The calculated value is stored
    x_arr[:, k + 1] = x_kp1
    
    # Residuum and increment are stored for the convergence check. The
    # values are normalized with respect to their initial values.
    convergence_residuum[0, k + 1] = np.linalg.norm(f(x_kp1))/np.linalg.norm(f(x0))
    print(convergence_residuum[0, k + 1])
    convergence_dx[0, k + 1] = np.linalg.norm(delta_x)/np.linalg.norm(x_arr[:, 1]-x0)
    
    # Convergence is checked
    if convergence_residuum[0, k + 1] < convergence_criterion and convergence_dx[0, k + 1] < convergence_criterion:
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
        raise Exception('Max Iteration number was reached in Newton-Raphson procedure before convergence was reached')


# output in the command window
for i in range(k + 1):
    print('Iteration #', i, ':')
    print('x =', x_arr[:, i])
    print('Residuum =', convergence_residuum[0, i])
    print('Increment =', convergence_dx[0, i])
    print('')




