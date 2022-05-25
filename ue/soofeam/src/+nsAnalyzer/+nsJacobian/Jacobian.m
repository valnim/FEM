classdef Jacobian < handle
    properties ( SetAccess = protected )
        J_inv
    end
    
    methods
        function self = Jacobian(node_container, int_point, configuration)
            self.calc(node_container, int_point, configuration);
        end
        
        function J = getMatrix(self)
            % The Jacobian is needed in order to transform the derivatives
            % with respect to the global (x,y) coordinates into derivatives
            % with respect to the reference (xi,eta) coordinates.
            J = inv(self.J_inv);
        end
        
        function Det = getDetInv(self)
            % The determinant of the inverse Jacobian is needed in order to
            % transform the integral from the real element on the reference
            % element.
            Ji = self.J_inv;
            dimJi = size(Ji);
            if dimJi(1) == dimJi(2)
                % In this case the Jacobian describes the transformation of
                % an element.
                Det = det(Ji);
            elseif min(dimJ) == 2
                % In this case the Jacobian describes the transformation of
                % a 2d face: (x,y,z) -> (xi,eta).
                % Hence it is not a square matrix.
                Det = norm(cross(Ji(:,1), Ji(:,2)));
            elseif min(dimJi) == 1
                % In this case the Jacobian describes the transformation of
                % a 1d face: (x,y) -> (xi)
                % Hence it is not a square matrix.
                Det = norm(Ji(:,1));
            else
                error('Error in Jacobian-dimensions!');
            end
        end
    end
    
    methods ( Access = private )
        function calc(self, node_container, int_point, configuration)
        % This method is called in the constructor and calculates the
        % Jacobian matrix of the integration point.
            dN = node_container.type.shape.getDerivativeArray(int_point.getNaturalCoordinates());
            x  = node_container.getCoordinateArray(configuration);
            
            self.J_inv = x*dN;
        end
    end    
end