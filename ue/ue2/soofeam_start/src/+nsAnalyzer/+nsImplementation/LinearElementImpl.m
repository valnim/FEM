classdef LinearElementImpl < nsAnalyzer.nsImplementation.ElementImpl
    properties
    end
    
    methods
        function K_C = calcStiffness(self, element)
            K_C = nsNumeric.NumInt.methodIntegrate(@self.stiffnessMatrixIntegrator, element.int_points, element);
        end
    end
    
    methods ( Static )
        function stiffness = stiffnessMatrixIntegrator( int_point, element )
            
            dimension = element.node_list(1).dimension;
            number_of_nodes = element.getNumberOfNodes();
            dofs_per_element = number_of_nodes * dimension;
            
            % Calculate the jacobian of the undeformed configuration
            jacobian = nsAnalyzer.nsJacobian.Jacobian(element, int_point, 'undeformed');
            
            % Calculate the derivatives of the shape functions
            dN        = element.type.shape.getDerivativeArray(int_point.getNaturalCoordinates());
            J         = jacobian.getMatrix();
            J_inv_det = jacobian.getDetInv();
            
            % Calculate the elasticity tensor
            C = element.material.getElasticityTensor(dimension);
            
            % We use a lot of loops to calculate the stiffness matrix. This
            % is not the fastest method, but this way the implementation
            % looks exactly like the theory.
            A = zeros(dimension,number_of_nodes,dimension,number_of_nodes);
            for i = 1:dimension
                for j = 1:number_of_nodes
                    for k = 1:dimension
                        for l = 1:number_of_nodes
                            for m = 1:dimension
                                for n = 1:dimension
                                    for o = 1:dimension
                                        for p = 1:dimension
                                            A(i,j,k,l) = A(i,j,k,l) + C(i,m,k,n)*dN(l,o)*J(o,n)*dN(j,p)*J(p,m)*J_inv_det;
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end

            stiffness = reshape(A,[dofs_per_element dofs_per_element]);
        end
    end
end
