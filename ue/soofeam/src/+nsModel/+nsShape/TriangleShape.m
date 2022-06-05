classdef TriangleShape < nsModel.nsShape.Shape
    %Class for triangle shape functions
        
    methods
        function self = TriangleShape( order )
            % The dimension of triangles is 2.
            dimension = 2;
            
            self@nsModel.nsShape.Shape( order, dimension );
        end
    end
    
    methods ( Access = protected )
        function val = getValue( self, natural_coordinates, node_index )
            % The value and derivative arrays are a bit more complicated
            % for triangles. See pySoofea documentation
            I = node_index(1);
            J = node_index(2);
            K = ( self.order - ( node_index(1)-1 + node_index(2)-1 ) ) + 1;
            L_1 = natural_coordinates(1);
            L_2 = natural_coordinates(2);
            L_3 = 1 - natural_coordinates(1) - natural_coordinates(2);
            
            val = self.lagrange.getValue( L_1 , I , I ) *...
                  self.lagrange.getValue( L_2 , J , J ) *...
                  self.lagrange.getValue( L_3 , K , K );
        end
        
        function der = getDerivative( self, coord, node_index, direction )
            % The value and derivative arrays are a bit more complicated
            % for triangles. See pySoofea documentation
            K = ( self.order - ( node_index(1)-1 + node_index(2)-1 ) ) + 1;
            L_3 = 1-coord(1)-coord(2);
            
            switch( direction )
                case 1
                    i = 1;
                    j = 2;
                case 2
                    i = 2;
                    j = 1;
            end
            
            der = self.lagrange.getDerivative( coord(i) , node_index(i) , node_index(i) ) * ...
                self.lagrange.getValue( coord(j) , node_index(j) , node_index(j) ) * ...
                self.lagrange.getValue( L_3 , K , K ) - ...
                self.lagrange.getValue( coord(i) , node_index(i) , node_index(i) ) * ...
                self.lagrange.getValue( coord(j) , node_index(j) , node_index(j) ) * ...
                self.lagrange.getDerivative( L_3 , K , K );
        end
        
        function node_positions = calcNodePositions(self)
            % For the tetraeder, cooridantes go from 0 to 1.
            nodes_per_side = self.order+1;
            node_positions = linspace(0,1,nodes_per_side);
        end
        
        function number_of_nodes = calcNumberOfNodes(self)
            % Total number of nodes.
            number_of_nodes = (self.order + 1)*(self.order + 2)/2;
        end
        
        function nodeindex = getNodeIndex( self, local_node_number )
            if self.order == 1
                % eta
                % ^
                % |
                % 3
                % |`\
                % |  `\
                % |    `\
                % |      `\
                % |        `\
                % 1----------2 --> xi
                switch local_node_number
                    case 1
                        nodeindex = [1,1];
                    case 2
                        nodeindex = [2,1];
                    case 3
                        nodeindex = [1,2];
                    otherwise
                        error('local node number out of range')
                end
            elseif self.order == 2
                % eta
                % ^
                % |
                % 3
                % |`\
                % |  `\
                % 6    5
                % |     `\
                % |       `\
                % 1----4----2 --> xi
                switch local_node_number
                    case 1
                        nodeindex = [1,1];
                    case 2
                        nodeindex = [3,1];
                    case 3
                        nodeindex = [1,3];
                    case 4
                        nodeindex = [2,1];
                    case 5
                        nodeindex = [2,2];
                    case 6
                        nodeindex = [1,2];                        
                    otherwise
                        error('local node number out of range')
                end
            else
                error('Triangle only implemented for order <= 2')
            end
        end
    end    
end