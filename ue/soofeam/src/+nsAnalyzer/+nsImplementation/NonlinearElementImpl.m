classdef NonlinearElementImpl < nsAnalyzer.nsImplementation.ElementImpl
    methods
        function A = calcStiffness(self, element)
            % This function calculates the stiffness matrix of an element
            % using numerical integration.

            A_CC = nsNumeric.NumInt.methodIntegrate(@self.constitutiveComponentIntegrator, element.int_points, element );

            A_ISC = nsNumeric.NumInt.methodIntegrate(@self.initialStressComponentIntegrator, element.int_points, element );

            % Add up the two components of the stiffness matrix.
            A = A_CC + A_ISC;

        end

        function F = calcLoad(self, element)
            % This function calculates the force vector of an element using
            % numerical integration

            % internal Forces:
            F_int = nsNumeric.NumInt.methodIntegrate(@self.internalForcesIntegrator, element.int_points, element );

            % Currently, the there are no external forces (body or surface
            % forces) implemented. The minus is the sign on the RHS of the newton method in front of the residuum
            F = -F_int;
        end
    end

    methods ( Static, Access = private )
        function A_ISC = initialStressComponentIntegrator(int_point, element)
            dimension = element.node_list(1).dimension;
            number_of_nodes = element.getNumberOfNodes();
            dofs_per_element = number_of_nodes * dimension;

            % Calculate all relevant quantities.
            % F is not needed here, hence the tilde.
            [~, E, dN, J, J_det_inv] = nsAnalyzer.nsImplementation.NonlinearElementImpl.calcKinematics(element, int_point);

            % Calculation of PK2 tensor
            S = element.material.getSecondPK(E);

            % Kronecker-delta
            delta = eye(dimension);

            % Implementation of the initial stress component of the
            % stiffness matrix
            A_ISC = zeros(dimension,number_of_nodes,dimension,number_of_nodes);
            for i = 1:dimension
                for j = 1:number_of_nodes
                    for k = 1:dimension
                        for l = 1:number_of_nodes
                            for m = 1:dimension
                                for n = 1:dimension
                                    for o = 1:dimension
                                        for p = 1:dimension
                                            A_ISC(i,j,k,l) = A_ISC(i,j,k,l) + delta(i,k)*dN(l,m)*J(m,n)*S(n,o)*dN(j,p)*J(p,o)*J_det_inv;
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end

            % Reshaping the stiffness matrix from a 4th order matrix into a
            % 2nd order matrix
            A_ISC = reshape(A_ISC,[dofs_per_element dofs_per_element]);
        end

        function A_CC = constitutiveComponentIntegrator( int_point, element )
            dimension = element.node_list(1).dimension;
            number_of_nodes = element.getNumberOfNodes();
            dofs_per_element = number_of_nodes * dimension;

            % Calculate all relevant quantities.
            %[F, E, dN, J, J_det_inv] =

            % Calculate the material elasticity tensor
            % CC = element.material.

            % Implementation of the constitutive component of the stiffness
            % matrix
            % A_CC =

            % Reshaping the stiffness matrix from a 4th order matrix into a
            % 2nd order matrix
            % A_CC =
        end

        function F_int = internalForcesIntegrator(int_point, element)
            dimension = element.node_list(1).dimension;
            number_of_nodes = element.getNumberOfNodes();
            dofs_per_element = number_of_nodes * dimension;

            % Calculate all relevant quantities.
            %[F, E, dN, J, J_det_inv] =

            % Calculation of PK2 tensor
            % S = element.material.

            % Implementation of the internal forces
            % F_int =

            % Reshaping the internal forces vector from a 2nd order matrix
            % into a column vector.
            % F_int =
        end

        function [F, E, dN, J, J_det_inv] = calcKinematics(element, int_point)
            % The relevant kinematic quantities are calculated for the
            % given integration point.

            % The Jacobian of the undeformed element:
            jac_undeformed = nsAnalyzer.nsJacobian.Jacobian(element, int_point, 'undeformed');

            % The Jacobian of the deformed element:
            jac_deformed = nsAnalyzer.nsJacobian.Jacobian(element, int_point, 'spatial');

            % Identity tensor:
            I = eye(length(jac_undeformed.getMatrix()));

            % Kinematic quantities:
            F         = inv(jac_deformed.getMatrix()) * jac_undeformed.getMatrix();
            E         = 0.5*(F'*F-I);
            dN        = element.type.shape.getDerivativeArray(int_point.getNaturalCoordinates());
            J         = jac_undeformed.getMatrix();
            J_det_inv = jac_undeformed.getDetInv();
        end
    end
end
