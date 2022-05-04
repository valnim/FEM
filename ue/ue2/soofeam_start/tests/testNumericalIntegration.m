f = @(x) 4*x^3 - 3*x^2 + 1;

order = 2;
int_points = nsNumeric.NumInt.getNaturalIntegrationPoints('linear',order);
result = nsNumeric.NumInt.integrate(f,int_points);

disp('Numerical Integration:')
disp(result)

disp('Exakt result:')
exact = 1.0;
disp(exact)



%---- Exercise 3 ----%
