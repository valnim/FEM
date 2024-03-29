classdef IPData
    % Die folgende Klasse enth�lt Lage und Gewichte f�r Integrationspunkte
    % auf verschiedenen Elementtypen (Gerade, Dreieck, Tetraeder) und dient
    % als Datenbank.
    
    properties
    end
    
    methods(Static)
        % Gau� integration points on the interval [-1,1]
        function ip_data = getLinearIPData(number_of_int_points)
            if number_of_int_points == 1
                ip_data = {{0.5, 1}};
            elseif number_of_int_points == 2
                ip_data = {{0.211324865405187, 0.5},...
                    {0.788675134594813, 0.5}};
            elseif number_of_int_points == 3
                ip_data = {{0.112701665379259, 0.277777777777778},...
                    {0.5, 0.444444444444444},...
                    {0.887298334620741, 0.277777777777778}};
            elseif number_of_int_points == 4
                ip_data = {{0.069431844202524, 0.173927422568727},...
                    {0.330009478207572, 0.326072577431273},...
                    {0.669990521792428, 0.326072577431273},...
                    {0.930568155797477, 0.173927422568727}};
            else
                error('number of integration points not implemented')
            end
        end
        
        % Gau� integration points on the reference triangle
        function ip_data = getTriangleIPData(number_of_int_points)
            if number_of_int_points == 1
                ip_data = {{[1/3,1/3],1/2}};
            elseif number_of_int_points == 3
                ip_data = {{[2/3,1/6],1/6},...
                      {[1/6,2/3],1/6},...
                      {[1/6,1/6],1/6}};
            elseif number_of_int_points == 4
                ip_data = {{[1/3,1/3],-9/32},...
                      {[6/10,2/10],25/96},...
                      {[2/10,6/10],25/96},...
                      {[2/10,2/10],25/96}};
            elseif number_of_int_points == 6
                ip_data = {{[0.816847572980459,0.091576213509771],0.109951743655322/2},...
                      {[0.091576213509771,0.816847572980459],0.109951743655322/2},...
                      {[0.091576213509771,0.091576213509771],0.109951743655322/2},...
                      {[0.108103018168070,0.445948490915965],0.223381589678011/2},...
                      {[0.445948490915965,0.108103018168070],0.223381589678011/2},...
                      {[0.108103018168070,0.108103018168070],0.223381589678011/2}};
            elseif number_of_int_points == 7
                ip_data = {{[1./3,1./3],0.225},...
                      {[0.797426985353087,0.101286507323456],0.125939150844827/2},...
                      {[0.101286507323456,0.797426985353087],0.125939150844827/2},...
                      {[0.101286507323456,0.101286507323456],0.125939150844827/2},...
                      {[0.059715871789770,0.470142064105115],0.132394152788506/2},...
                      {[0.470142064105115,0.059715871789770],0.132394152788506/2},...
                      {[0.470142064105115,0.470142064105115],0.132394152788506/2}};
            else
                error('number of integration points not implemented')                  
            end
        end        
        
        % Gau� integration points on the reference tetraeder
        function ip_data = getTetraIPData(number_of_int_points)
            a = (5 + 3*sqrt(5))/20;
            b = (5 - sqrt(5))/20;
            c = (1 + sqrt(5/14))/4;
            d = (1 - sqrt(5/14))/4;
            if number_of_int_points == 1
                ip_data = {{[1/4,1/4,1/4],1.6}};
            elseif number_of_int_points == 4
                ip_data = {{[a,b,b],1/24},...
                      {[b,a,b],1/24},...
                      {[b,b,a],1/24},...
                      {[b,b,b],1/24}};
            elseif number_of_int_points == 5
                ip_data = {{[1/4,1/4,1/4],-4/30},...
                      {[1/2,1/6,1/6],9/120},...
                      {[1/6,1/2,1/6],9/120},...
                      {[1/6,1/6,1/2],9/120},...
                      {[1/6,1/6,1/6],9/120}};
            elseif number_of_int_points == 11
                ip_data = {{[1/4,1/4,1/4],-74/5625},...
                       {[11/14,1/14,1/14],343/45000},...
                       {[1/14,11/14,1/14],343/45000},...
                       {[1/14,1/14,11/14],343/45000},...
                       {[1/14,1/14,1/14],343/45000},...
                       {[c,c,d],56/2250},...
                       {[c,d,c],56/2250},...
                       {[c,d,d],56/2250},...
                       {[d,c,c],56/2250},...
                       {[d,c,d],56/2250},...
                       {[d,d,c],56/2250}};
            else
                error('number of integration points not implemented')                   
            end
        end        
    end
end

