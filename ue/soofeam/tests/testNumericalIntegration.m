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

ips = nsNumeric.NumInt.getNaturalIntegrationPoints('quad',3);

sum_weights = 0;
for i = 1:length(ips)
    ip = ips(i);
    fprintf('ip #%u:\n',i)
    disp(ip.natural_coordinates)
    disp(ip.weight)
    sum_weights = sum_weights + ip.weight;
end

disp('sum of weights:')
disp(sum_weights)
