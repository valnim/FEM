%-------------------------------------------------------------------------%
% FE-Methods, SS 2020, 3. Unit
%
% Script for visualization of the Newton-Raphson method.
% This script is only for demonstration purposes.
% Convergence is not checked.
%-------------------------------------------------------------------------%

restoredefaultpath
clear
close all
clc

% In the scalar case, the function and its derivative can be implemented
% directly via function handles. For nonlinear equation systems, the
% functions are defined in files on their own.
f = @(arg) arg-exp(-arg);
df = @(arg) 1+exp(-arg);

% Setting the initial guess and the number of iterations
x0 = -3;
max_iterations = 10;

% In the following array, the x-value of each iteration step is stored.
x_arr    = zeros(1,max_iterations+1);
x_arr(1) = x0;

% x- and y values for the plot are calculated
x = linspace(-3.5,1.5,1001);
y = arrayfun(f,x);

figure(1)
hold on

% x axis and initial guess are plotted.
plot([x(1),x(end)], [0 0],'k');
p1 = plot(x,y,'Color','b');
plot(x0,f(x0),'r*','MarkerSize',8);
plot([x0, x0],[0 f(x0)],'r');

lgd = legend(p1,'x-exp(-x)','AutoUpdate','off');
lgd.FontSize = 30;

for k = 1:max_iterations
    pause
    
    % Implementation of the Newton Raphson method
    x_k = x_arr(k);
    delta_x = -f(x_k)/df(x_k);
    x_kp1 = x_k + delta_x;
    
    % The calculated value is stored
    x_arr(k+1) = x_kp1;
    
    % The calculated value is plotted
    plot([x_k x_kp1],[f(x_k) 0], 'Color', [0.5 0.5 0.5]);
    plot([x_kp1 x_kp1],[0 f(x_kp1)], 'r');
    plot(x_kp1, f(x_kp1), 'r*');
end