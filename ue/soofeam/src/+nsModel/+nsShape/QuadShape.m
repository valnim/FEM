classdef QuadShape < nsModel.nsShape.Shape
    % Class for 2d-shape functions on the reference element.
    
    methods
        function self = QuadShape(order)
            % The dimension of a quadrangle is 2.
            dimension = 2;
            
            self@nsModel.nsShape.Shape(order, dimension)
        end
    end
    
    methods ( Access = protected )
        function val = getValue(self, natural_coordinates, node_index)
            % The function value according to the theory:
            % h[i,j](xi,eta) = h_i(xi)*h_j(eta)
            val = self.lagrange.getValue(natural_coordinates(1), node_index(1)) * ...
                self.lagrange.getValue(natural_coordinates(2), node_index(2));
        end
        
        function der = getDerivative(self, natural_coordinates, node_index, derivative_direction)
            % The value of the derivative is calculated according to the
            % theory. You have to specifiy the direction of the derivative:
            % with respect to xi->1 or w.r.t eta->2
            if derivative_direction == 1
                der = self.lagrange.getDerivative(natural_coordinates(1), node_index(1)) * ...
                    self.lagrange.getValue(natural_coordinates(2), node_index(2));
            elseif derivative_direction == 2
                der = self.lagrange.getValue(natural_coordinates(1), node_index(1)) * ...
                    self.lagrange.getDerivative(natural_coordinates(2), node_index(2));
            end
        end
        
        function node_positions = calcNodePositions(self)
            % It suffices to give the position of the nodes in one
            % coordinate direction.
            nodes_per_side = self.order+1;
            node_positions = linspace(0,1,nodes_per_side);
        end
        
        function number_of_nodes = calcNumberOfNodes(self)
            % total number of nodes
            number_of_nodes = (self.order + 1)^2;
        end
        
        function node_index = getNodeIndex(self, local_node_number)
            if self.order == 1
                % eta
                % ^
                % |
                % 4-----------3
                % |           |
                % |           |
                % |           |
                % |           |
                % |           |
                % 1-----------2--->xi
                switch local_node_number
                    case 1
                        node_index = [1,1];
                    case 2
                        node_index = [2,1];
                    case 3
                        node_index = [2,2];
                    case 4
                        node_index = [1,2];
                    otherwise
                        error('local node number out of range')
                end
            elseif self.order == 2
                % eta
                % ^
                % |
                % 4-----7-----3
                % |           |
                % |           |
                % 8     9     6 
                % |           |
                % |           |
                % 1-----5-----2---> xi
                switch local_node_number
                    case 1
                        node_index = [1,1];
                    case 2
                        node_index = [3,1];
                    case 3
                        node_index = [3,3];
                    case 4
                        node_index = [1,3];
                    case 5
                        node_index = [2,1];
                    case 6
                        node_index = [3,2];
                    case 7
                        node_index = [2,3];
                    case 8
                        node_index = [1,2];
                    case 9
                        node_index = [2,2];
                    otherwise
                        error('local node number out of range')
                end
            else
                error('QuadShape only implemented for order <= 2')
            end
        end
    end
end
