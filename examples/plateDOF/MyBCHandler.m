classdef MyBCHandler < nsModel.BCHandler
    methods
        function self = MyBCHandler(model)
            self@nsModel.BCHandler(model)
        end
    end
    
    methods
        function incorporateBC(self)
            
            %===========================
            % DISPLACEMENT BC
            %===========================
                        
            % The bottom boundary is fixed
            bottom_boundary = 1;
            for node = self.model.boundary_dict(bottom_boundary).node_list
                node.setBCDisplacement('x',0);
                node.setBCDisplacement('y',0);
            end
            
            % the top boundary is dragged in vertical direction
            top_boundary = 3;
            top_y_value = 0.1;
            
            for node = self.model.boundary_dict(top_boundary).node_list
                node.setBCDisplacement('y', top_y_value);
            end
        end
    end
end