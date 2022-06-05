classdef LinearElasticMaterial < nsModel.nsMaterial.Material
    % Linear elastic material for small deformations
    
    properties ( SetAccess = private )
    end
    
    methods
        function self = LinearElasticMaterial(E_mod, nu, two_dim_type)
            if nargin < 3
                two_dim_type = {};
            end
            
            self@nsModel.nsMaterial.Material(E_mod, nu, two_dim_type);
        end
    end
    
    methods ( Abstract )
        getElasticityTensor(self, dimension)
    end
end

