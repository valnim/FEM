classdef NodeContainer < nsModel.NumberedObject
    %NODECONTAINER Contains Nodes - superclass for Face, Element and
    %Boundary
    
    properties ( SetAccess = protected )
        node_list
        type
        int_points
    end
    
    methods
        function self = NodeContainer(number, node_list)
            self@nsModel.NumberedObject( number );
            
            % An array containing the node references. It is important to
            % note that the nodes inside the 'node_list' are sorted
            % regarding their local node numbers.
            self.node_list = node_list;
            
            % Containing the model.Type of this
            % object
            self.type = [];
            
            % Containing all the soofea.model.RealIntegrationPoint of this
            % object. This list is initialized by self.setType as soon as a
            % type is assigned.
            self.int_points = [];
        end
               
        function number_of_nodes = getNumberOfNodes(self)
            number_of_nodes = length(self.node_list);
        end
        
        function coordinate_array = getCoordinateArray( self, configuration )
            % returns an array in the format:
            %
            %   [ x1 x2 ... xn
            %     y1 y2 ... yn
            %     z1 z2 ... zn ]
            %
            % where 'n' is the number of nodes of the node container.
            number_of_nodes = self.getNumberOfNodes();
            dimension = self.node_list(1).dimension;
            
            % coordinate_array is an ( number_of_nodes x dimension ) array.
            coordinate_array = zeros( dimension, number_of_nodes );
            
            if strcmp(configuration, 'undeformed')
                for i = 1:number_of_nodes
                    coordinate_array(:,i) = self.node_list(i).undeformed_coordinates;
                end
            elseif strcmp(configuration, 'spatial')
                for i = 1:number_of_nodes
                    coordinate_array(:,i) = self.node_list(i).spatial_coordinates;
                end
            else
                error('Configuration needs to be string ''undeformed'' or ''spatial''!')
            end
        end
        
        function displacement_array = getDisplacementArray( self )
            % returns displacements of nodes of the node container in the
            % format
            %
            %   [ u1 u2 ... un
            %     v1 v2 ... vn
            %     w1 w2 ... wn ]
            %
            number_of_nodes = self.getNumberOfNodes();
            dimension = self.node_list(1).dimension;
            
            % displacement_array is an ( number_of_nodes x dimension ) array.
            displacement_array = zeros( dimension, number_of_nodes );
            for i = 1:number_of_nodes
                displacement_array(:,i) = self.node_list(i).dof.displacement;
            end
        end
        
        function setType( self, the_type )
            % This method not only sets the type but also initiates the list of all
            % soofea.model.RealIntegrationPoint objects. This is done by
            % iterating of the mathematical integration points soofea.numeric.NaturalIntegrationPoint inside
            % the class soofea.model.Type.
            
            % the_type: The actual nsModel.nsType.Type of this object
            % (e.g. linear quad with two integration points per coordinate direction)
            self.type = the_type;
            natural_int_points = the_type.natural_int_points;
            
            for int_point = natural_int_points
                X = self.getCoordinateArray('undeformed');                        % returns array with coordinates of node points
                N = self.type.shape.getArray( int_point.natural_coordinates );  % returns value of interpolation functions on the integration point on the reference cell
                coords = X*N;                                                   % calculates the coordinates of the RealIntegrationPoint with the isoparametric concept: x = X*N, just like u = U*N
                self.int_points = [self.int_points nsModel.RealIntegrationPoint( int_point, coords )];
            end
        end       
    end
end

