classdef MyBCHandler < nsModel.BCHandler
    methods
        function self = MyBCHandler(model)
            self@nsModel.BCHandler(model)
        end
    end
    
    methods
        function incorporateBC(self, ~)
            
            %===========================
            % DISPLACEMENT BC
            %===========================
                        
            % bottom boundary is fixed in both directions
            bottom_boundary = 1;
            
            for node = self.model.boundary_dict(bottom_boundary).node_list
                node.setBCIncrement('x',0);
                node.setBCIncrement('y',0);
            end
            
            % top boundary is pulled up by a constant displacement.
            top_boundary = 3;
            top_y_value = 10/(length(self.model.time_bar)-1);
            
            for node = self.model.boundary_dict(top_boundary).node_list
                node.setBCIncrement('y', top_y_value);
            end
        end
    end
end