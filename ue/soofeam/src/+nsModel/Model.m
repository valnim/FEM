classdef Model < handle
    %MODEL The model of the finite element problem
    properties ( SetAccess = private )
        dimension
        bc_handler = [];
        
        node_dict = nsModel.Node.empty
        element_dict = nsModel.Element.empty
        face_dict = nsModel.Face.empty
        boundary_dict = nsModel.Boundary.empty
        
        element_type
        boundary_type
        
        material
        
        time_bar = nsModel.TimeStamp.empty;
    end
    
    methods
        function self = Model(dim)
            self.dimension = dim;
            self.time_bar(1) = nsModel.TimeStamp(0, 0.0);
        end
        
        function addTimeStep(self, time)
            new_index = self.time_bar(end).index + 1;
            self.time_bar = [self.time_bar nsModel.TimeStamp(new_index, time)];
        end
        
        function setBCHandler( self, bc_handler )
            self.bc_handler = bc_handler;
        end
                
        function n_nodes = getNumberOfNodes(self)
            n_nodes = length(self.node_dict);
        end
        
        function addNode(self, new_node)
            self.node_dict(new_node.number) = new_node;
        end
        
        function addElement(self, new_element)
            self.element_dict(new_element.number) = new_element;

            new_element.setType( self.element_type );
            new_element.setMaterial( self.material );
        end
                
        function addFace( self, new_face )
            self.face_dict(new_face.number) = new_face;
          
            new_face.setType( self.boundary_type );
        end
        
        function setElementType( self, element_type )
            self.element_type = element_type;
        end
              
        function setBoundaryType( self, boundary_type )
            self.boundary_type = boundary_type;
        end
        
        function setMaterial( self, new_material )
            self.material = new_material;
        end
        
        function number_of_unknowns = getNumberOfUnknowns(self)
           % Works only for a one-field-formulation
           number_of_unknowns = self.dimension * numel(self.node_dict);
        end
               
        function appendFaceToBoundary( self, boundary_number, face_number)
            
            % The following condition is fulfilled for the first boundary.
            % The second one checks wether the current boundary number
            % already exists in the boundary dict.
            if isempty(self.boundary_dict) || ~ismember(boundary_number ,[self.boundary_dict.number])
                self.boundary_dict(boundary_number) = nsModel.Boundary(boundary_number);
            end
            
            % add component to the boundary
            boundary = findobj(self.boundary_dict, 'number', boundary_number);
            
            new_face = self.face_dict(face_number);
            
            boundary.addFace( new_face );
        end
    end
end