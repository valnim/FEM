%-------------------------------------------------------------------------%
% FE-Methods, SS 2020, 3. Unit
%
% Script for calculating the root of the function f(x) = x-exp(x) with the
% Newton-Raphson method
%-------------------------------------------------------------------------%

restoredefaultpath
clear
close all
clc

% Set the number of equations to solve
n_equations = 1;

format shortG

% In the scalar case, the function and its derivative can be implemented
% directly via function handles. For nonlinear equation systems, the
% functions are defined in files on their own.
f = @(arg) arg-exp(-arg);
df = @(arg) 1+exp(-arg);

% Setting the initial guess, the maximum number of iterations and the
% convergence criterion (same for increment and residuum)
x0 = -3;
max_iterations        = 15;
convergence_criterion = 1e-12;

% In the following array, the x-value of each iteration step is stored.
x_arr      = zeros(n_equations,max_iterations+1);
x_arr(:,1) = x0;

% In the following arrays, residuum and increment of each iteration step
% are stored.
convergence_residuum = ones(1,max_iterations+1);
convergence_dx       = ones(1,max_iterations+1);

for k = 1:max_iterations
    % Implementation of the Newton Raphson method
    x_k     = x_arr(:,k);
    delta_x = -df(x_k)\f(x_k);
    x_kp1   = x_k + delta_x;
    
    % The calculated value is stored
    x_arr(:,k+1) = x_kp1;
    
    % Residuum and increment are stored for the convergence check. The
    % values are normalized with respect to their initial values.
    convergence_residuum(k+1) = norm(f(x_kp1))/norm(f(x0));
    convergence_dx      (k+1) = norm(delta_x)/norm(x_arr(:,2)-x0);
    
    % Convergence is checked
    if convergence_residuum(k+1)<convergence_criterion && convergence_dx(k+1)<convergence_criterion
        % If both convergence criteria are fulfilled, we can stop the
        % iteration.
        fprintf('Newton method converged at step %u\n\n',k+1)
                
        format long
        disp('Converged solution:')
        disp(x_arr(:, k+1))
        
        break
    elseif k == max_iterations
        % If there is no convergence after max_iterations iterations, the 
        % calculation is aborted and an error is displayed.
        error('Max Iteration number was reached in Newton-Raphson procedure before convergence was reached')
    end
end

% output in the command window
fid = 1;
fprintf('n_iteration:\t')
fprintf(fid, [repmat('%10d   ', 1, max_iterations+1) '\n'], 0:max_iterations')
fprintf('residum:\t')
fprintf(fid, [repmat('%10.4d   ', 1, max_iterations+1) '\n'], convergence_residuum')
fprintf('delta_x:\t')
fprintf(fid, [repmat('%10.4d   ', 1, max_iterations+1) '\n'], convergence_dx')
