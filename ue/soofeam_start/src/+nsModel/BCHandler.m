classdef BCHandler < handle
    
    properties (SetAccess = protected)
        model
    end
    
    methods
        function self = BCHandler(model)
            self.model = model;
        end
    end
    
    methods (Abstract)
        % This method is implemented for each example seperately, and
        % specifies the boundary conditions for the specific geometry and
        % load case.
        incorporateBC(self)
    end
    
end