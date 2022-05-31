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
                node.setBCIncrement('z',0);
            end
            
            % top boundary is twisted (transistor).
            top_boundary = 2;
            
            alpha_total = 2*pi;
            delta_alpha = alpha_total/(length(self.model.time_bar)-1);
            
            for node = self.model.boundary_dict(top_boundary).node_list
                
                
                coords_old = node.spatial_coordinates;
                x_old = coords_old(1);
                y_old = coords_old(2);
                
                r_old = sqrt(x_old^2+y_old^2);
                j_old = atan2(y_old,x_old);
                
                r_new = r_old;
                j_new = j_old + delta_alpha;
                
                x_new = r_new*cos(j_new);
                y_new = r_new*sin(j_new);
                
                dx = x_new - x_old;
                dy = y_new - y_old;
                
                node.setBCIncrement('x', dx);
                node.setBCIncrement('y', dy);
            end
        end
    end
end
