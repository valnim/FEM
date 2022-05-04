classdef Face < nsModel.NodeContainer
    
    methods
        function self = Face( number, node_number_list )
            self@nsModel.NodeContainer( number, node_number_list );
        end
    end
end