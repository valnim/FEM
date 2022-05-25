classdef Shape < handle
    % Abstract base class for shape functions
    
    properties ( SetAccess = protected )
        order
        dimension
        lagrange
    end
    
    methods
        function self = Shape(order, dimension)
            self.order = order;
            self.dimension = dimension;
            self.lagrange = nsModel.nsShape.Lagrange(self.calcNodePositions());
        end
              
        function N = getArray(self, coordinates)
            % The interpolation matrix has the form
            %
            % N = [N1
            %      N2
            %       .
            %       .
            %       .
            %      Nn]
            %
            % where n is the number of nodes and Ni is the i-th shape
            % function
            n = self.calcNumberOfNodes;
            N = zeros(n,1);
            for node_number=1:n
                node_index = self.getNodeIndex(node_number);
                N(node_number) = self.getValue( coordinates, node_index  );
            end
        end
              
        function dN = getDerivativeArray(self, natural_coordinates)
            % The dN-matrix or derivative matrix has the form
            %
            % dN = [ dN1_dxi dN1_deta dN1_dzeta
            %        dN2_dxi dN2_deta dN2_dzeta
            %          .       .      .
            %          .       .      .
            %          .       .      .
            %
            %        dNn_dxi dNn_deta dNn_dzeta ]
            %
            % where n is the number of nodes and dN_i,j  is the derivative
            % of the i-th shape function in the j-th coordinate direction.
            %
            % IMPORTANT: The derivatives are with respect to the natural
            % coordinates! In order to calculate stiffness matrices, we
            % will need jacobians.
            n = self.calcNumberOfNodes;
            dN = zeros(n, self.dimension);
            for node_number=1:n
                node_index = self.getNodeIndex(node_number);
                for direction=1:self.dimension
                    dN(node_number, direction) = self.getDerivative( natural_coordinates, node_index, direction );
                end
            end
        end
        
        function number_of_nodes = getNumberOfNodes(self)
           number_of_nodes = self.calcNumberOfNodes;
        end
    end    
    
    methods (Abstract, Access = protected)
        getValue(self, natural_coordinates, node_index)
        getDerivative(self, natural_coordinates, node_index, derivative_direction)
        calcNodePositions(self)
        calcNumberOfNodes(self)
        getNodeIndex(local_node_number)
    end
end