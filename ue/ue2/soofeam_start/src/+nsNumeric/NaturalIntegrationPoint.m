classdef NaturalIntegrationPoint
    %Integration Point on the reference element
    
    properties ( SetAccess = protected )
        weight
        natural_coordinates
    end
    
    methods
        function self = NaturalIntegrationPoint(weight, natural_coordinates)
            self.weight = weight;
            self.natural_coordinates = natural_coordinates;
        end
    end
end
