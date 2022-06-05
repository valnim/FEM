classdef Element < nsModel.NodeContainer

    properties ( SetAccess = private )
        material
    end
    
    methods
        function self = Element(number, node_number_list)
            self@nsModel.NodeContainer(number, node_number_list);
        end
        
        function setMaterial( self, material )
            self.material = material;
        end
    end
end

