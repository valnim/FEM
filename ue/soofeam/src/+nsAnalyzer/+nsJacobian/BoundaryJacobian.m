classdef BoundaryJacobian < nsAnalyzer.nsJacobian.Jacobian
    properties ( SetAccess = protected )
        a;
        b;
    end
    
    methods
        function self = BoundaryJacobian(node_container, int_point, configuration)
            self@nsAnalyzer.nsJacobian.Jacobian(node_container, int_point, configuration);
            self.calcTangentVectors();
        end
    end
    
    methods ( Access = private )
        function calcTangentVectors(self)
            J = self.J_inv;
            dimJ = size(J);
            
            if min(dimJ) == 2
                % In diesem Fall beschreibt die Jacobi-Matrix die
                % Transformation eines Faces: (x,y,z) -> (r,s)
                self.a = J(:,1);
                self.b = J(:,2);
            elseif min(dimJ) == 1
                % In diesem Fall beschreibt die Jacobi-Matrix die
                % Transformation eines Edges: (x,y) -> (r)
                self.a        = zeros(3,1);
                self.a(1:2,1) = J(:,1);
                self.b        = [0 0 1];
            else
                error('Error in Boundary Jacobian Dimension')
            end
        end
    end    
end