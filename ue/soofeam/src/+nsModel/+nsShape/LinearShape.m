classdef LinearShape < nsModel.nsShape.Shape
    % Class for 1d shape functions on the reference element
    
    properties
    end
    
    methods
        function self = LinearShape(order)
            % The dimension of 1d shape elements is 1.
            dimension = 1;
           
            self@nsModel.nsShape.Shape(order, dimension)
        end
    end
    
    methods ( Access = protected )
        function val = getValue(self, natural_coordinate, node_index)
            % The value is just the value of the lagrange polynomial.
            val = self.lagrange.getValue(natural_coordinate, node_index);
        end
        
        function der = getDerivative(self, natural_coordinate, node_index, ~)
            % The derivative is the derivative of the lagrange polynomial.
            % In the 1d case, you dont need the last parameter (direction
            % of derivative).
            der = self.lagrange.getDerivative(natural_coordinate, node_index);
        end
        
        function node_positions = calcNodePositions(self)
            % The nodes are distributed equally spaced along the interval
            % [0 1]
            n = self.calcNumberOfNodes;
            node_positions = linspace(0,1,n);
        end
        
        function number_of_nodes = calcNumberOfNodes(self)
            % Number of nodes for 1d element
            number_of_nodes = self.order + 1;
        end

        function nodeindex = getNodeIndex(self, local_node_number)
            if self.order == 1
                nodeindex = local_node_number;
            elseif self.order == 2
                switch local_node_number
                    case 1
                        nodeindex = 1;
                    case 2
                        nodeindex = 3;
                    case 3
                        nodeindex = 2;
                end
            else
                error('LinearShape only implemented for order <= 2')
            end
        end
    end
end
