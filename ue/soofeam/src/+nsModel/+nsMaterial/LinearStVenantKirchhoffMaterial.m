classdef LinearStVenantKirchhoffMaterial < nsModel.nsMaterial.LinearElasticMaterial
    
    methods
        function self = LinearStVenantKirchhoffMaterial(E_mod, nu, two_dim_type)
            if nargin < 3
                two_dim_type = {};
            end
            
            self@nsModel.nsMaterial.LinearElasticMaterial(E_mod, nu, two_dim_type);
        end
        
        function C = getElasticityTensor(self,dimension)
            C = zeros(dimension, dimension, dimension, dimension);
            
            delta = eye(dimension);
            
            for i = 1:dimension
                for j = 1:dimension
                    for k = 1:dimension
                        for l = 1:dimension
                            C(i,j,k,l) = self.lambda*delta(i,j)*delta(k,l) + self.mu*(delta(i,k)*delta(j,l) + delta(i,l)*delta(j,k));
                        end
                    end
                end
            end
        end
    end
end

