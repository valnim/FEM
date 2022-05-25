classdef Lagrange < handle
    %LAGRANGE Class for one-dimensional Lagrange-Polynomials
    
    properties ( SetAccess = protected )
        node_positions
        order
    end
    
    methods
        function self=Lagrange(node_positions)
            % node_positions: List of interpolation points of the
            % polynomial
            self.node_positions = node_positions;
            self.order = length(self.node_positions) - 1;
        end
        
        function L = getValue(self, coordinate, index, top_index)
            % Returns the value of the lagrange polynomial with index
            % 'index' at position 'xi=coordinate'.
            % The parameter 'top_index' is needed for triangle elements.
            
            if nargin <= 3 % nargin == 2 is needed for 1d, quad and hex elements.
                high = self.order + 1;
            else %nargin == 3 is needed for triangle and tetraeder elements.
                high = top_index;
            end
            
            L = 1;            
            for i=1:high
                if i~=index
                    L = L*(coordinate-self.node_positions(i))/(self.node_positions(index)-self.node_positions(i));
                end
            end
        end
        
        function D = getDerivative(self, coordinate, index, top_index)
            % Returns the derivative of the lagrange polynomial with index
            % 'index' at position 'xi=coordinate'.
            % The parameter 'top_index' is needed for triangle elements.
            
            if nargin <= 3 % nargin == 2 is needed for 1d, quad and hex elements.
                high = self.order + 1;
            else %nargin == 3 is needed for triangle and tetraeder elements.
                high = top_index;
            end

            factor_1 = 1;
            for i=1:high
                if i~=index
                    factor_1 = factor_1/(self.node_positions(index) - self.node_positions(i));
                end
            end
            sum_i = 0;
            
            for i=1:high
                if i~=index
                    inner_factor = 1;
                    for j=1:self.order+1
                        if j~=index && j~=i
                            inner_factor = inner_factor * (coordinate - self.node_positions(j));
                        end
                    end
                    sum_i = sum_i + inner_factor;
                end
            end
            D = factor_1 * sum_i;
        end
    end
end