classdef (Abstract) Material < handle
    
    properties ( SetAccess = protected )
        % two_dim_type is 'plane_stress' (ESZ) or 'plane_strain' (EVZ) for
        % 2d. Currently only EVZ is implemented.
        two_dim_type
        E_mod
        nu
        lambda
        mu
    end
    
    methods
        function self = Material(E_mod, nu, two_dim_type)
            if nargin < 3
                two_dim_type = {};
            end
            self.two_dim_type = two_dim_type;
            
            self.E_mod = E_mod;
            self.nu    = nu;
            self.calcLame();
        end
    end
    
    methods ( Access = private )
        function calcLame(self)
            self.lambda = self.E_mod * self.nu / ((1.0 + self.nu) * (1.0 - 2.0*self.nu));
            self.mu = self.E_mod / (2 * (1.0 + self.nu));
        end
    end    
end