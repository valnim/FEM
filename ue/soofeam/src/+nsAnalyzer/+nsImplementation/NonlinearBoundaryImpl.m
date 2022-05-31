classdef NonlinearBoundaryImpl < nsAnalyzer.nsImplementation.BoundaryImpl
    properties
    end
    
    methods
        function A = calcStiffness(self, face)
            A_p = nsNumeric.NumInt.methodIntegrate(@self.pressureStiffnessIntegrator, face.int_points, face );
            
            A = A_p;
        end
        
        function F = calcLoad(self, face)
            % external Forces:
            F_p = nsNumeric.NumInt.methodIntegrate(@self.pressureForcesIntegrator, face.int_points, face);
            
            F = -F_p;
        end
    end
    
    methods ( Static, Access = private)
        function A_p = pressureStiffnessIntegrator(int_point, face)
            dimension = face.node_list(1).dimension;
            number_of_nodes = face.getNumberOfNodes();
            dofs_per_face = number_of_nodes * dimension;

            [p, N, dN, levi, a, b] = nsAnalyzer.nsImplementation.NonlinearBoundaryImpl.calcStuff(face, int_point);
            
            % in 2D, derivatives with respect to eta have to be added
            % artificially.
            if dimension == 2
                dN(:,2) = zeros(length(dN),1);
            end
            
            delta = eye(3);

            % We calculate the 3D case, irrespective of the actual
            % dimension of our problem. In the 2D case, we extract the
            % relevant components afterwards.
            A_p = zeros(3, number_of_nodes, 3, number_of_nodes);
            for i = 1:3
                for j = 1:number_of_nodes
                    for k = 1:3
                        for l = 1:number_of_nodes
                            for m = 1:3
                                for n = 1:3
                                    A_p(i,j,k,l) = A_p(i,j,k,l) + p*N(j)*levi(i,m,n)*( dN(l,1)*b(n)*delta(k,m)+dN(l,2)*a(m)*delta(k,n) );
                                end
                            end
                        end
                    end
                end
            end
            
            A_p = A_p(1:dimension, :, 1:dimension, :);
            
            A_p = reshape(A_p, dofs_per_face, dofs_per_face);
        end
        
        function F_p = pressureForcesIntegrator(int_point, face)
            dimension = face.node_list(1).dimension;
            number_of_nodes = face.getNumberOfNodes();
            dofs_per_face = number_of_nodes * dimension;            
            
            [p, N, ~, levi, a, b] = nsAnalyzer.nsImplementation.NonlinearBoundaryImpl.calcStuff(face, int_point);
            
            % We calculate the 3D case, irrespective of the actual
            % dimension of our problem. In the 2D case, we extract the
            % relevant components afterwards.
            F_p = zeros(3, number_of_nodes);            
            for i = 1:3
                for j = 1:number_of_nodes
                    for k = 1:3
                        for l = 1:3
                            F_p(i,j) = F_p(i,j) + p*N(j)*levi(i,k,l)*a(k)*b(l);
                        end
                    end
                end
            end
            
            F_p = F_p(1:dimension,:);
            
            F_p = reshape(F_p, dofs_per_face, 1);
        end

        function [p, N, dN, levi, a, b] = calcStuff(face, int_point)
            % This function calculates all quantities we need for the
            % residuum (force vector) and tangent (stiffness matrix) of a
            % surface element with pressure boundary conditions.
            
            % Create the spatial Jacobian matrix
            jac = nsAnalyzer.nsJacobian.BoundaryJacobian(face, int_point, 'spatial');
            
            % Create the Levi-Civselfita permutation tensor
            levi = nsAnalyzer.nsImplementation.NonlinearBoundaryImpl.makeLeviCivita();

            % Create the two tangent vectors
            a = jac.a;
            b = jac.b;
            
            % Create the interpolation array and derivative array
            N = face.type.shape.getArray(int_point.natural_int_point.natural_coordinates);
            dN = face.type.shape.getDerivativeArray(int_point.natural_int_point.natural_coordinates);
            
            % Query the pressure
            p = int_point.pressure;            
        end
        
        function levi = makeLeviCivita()
            % This function creates the 3D Levi-Civita tensor used for
            % calculating the cross product in index notation.
            
            levi = zeros(3,3,3);
            
            for i = 1:3
                for j = 1:3
                    for k = 1:3
                        if (i==1 && j==2 && k == 3) || (i==2 && j==3 && k == 1) || (i==3 && j==1 && k == 2)
                            levi(i,j,k) = 1;
                        elseif (i==1 && j==3 && k == 2) || (i==2 && j==1 && k == 3) || (i==3 && j==2 && k == 1)
                            levi(i,j,k) = -1;
                        end
                    end
                end
            end
        end
    end
end