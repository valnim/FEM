classdef RealIntegrationPoint < handle
    % Each nsModel.NodeContainer gets its own set of
    % soofeaM.nsModel.RealIntegrationPoint objects
    
    % set-functions need to be implemented!
    properties % ( SetAccess = protected )
        % Each Integration point has an associated natural integration
        % point on the reference cell.
        natural_int_point
        
        % For a Lagrangian formulation, it suffices to know the undeformed
        % coordinates of each integration point.
        undeformed_coordinates = []
    end
    
    methods
        function self = RealIntegrationPoint( natural_int_point, undeformed_coordinates )
            self.natural_int_point = natural_int_point;
            self.undeformed_coordinates = undeformed_coordinates;
        end
        
        function weight = getWeight(self)
            weight = self.natural_int_point.weight;
        end
        
        function natural_coords = getNaturalCoordinates(self)
            natural_coords = self.natural_int_point.natural_coordinates;
        end
    end
end
