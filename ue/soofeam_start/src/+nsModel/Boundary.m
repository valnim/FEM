classdef Boundary < nsModel.NodeContainer
    
    properties ( SetAccess = private )
        % This list contains all faces of the boundary.
        face_list = nsModel.Face.empty;
    end
    
    methods
        function self = Boundary( number )
            % The following lines are neccessary, because the boundaries
            % may be constructed unordered, e.g. 1-3-2-..
            % see: https://de.mathworks.com/help/matlab/matlab_oop/initialize-object-arrays.html
            if nargin == 0
                number = 0;
            end
            % The node_number_list is empty at the point of creation of the
            % boundary
            self@nsModel.NodeContainer( number, [] );
        end
        
        function addFace( self, new_face )
            % As this class is derived from soofea.model.NodeContainer, we have
            % to append the nodes of the new component and their numbers to the
            % nsModel.NodeContainer.node_number_list and the
            % nsModel.NodeContainer.node_list.
            
            % The component given to this function (nsModel.Face) is added
            % to the boundary
            self.face_list(end+1) = new_face;
            
            for new_node = new_face.node_list              
                % Add the new node only if it is not already contained and
                % if the current new_node is not empty.
                % (Why should it be empty?)
                if ~ismember(new_node, self.node_list) && ~isempty(new_node) 
                    self.node_list        = [self.node_list new_node];
                end
            end
        end
    end
end