% A linear St Venant Kirchhoff material is created.
material = nsModel.nsMaterial.LinearStVenantKirchhoffMaterial(210000, 0.3);

dimension = 3;


%---- Exercise 6a ----%

% Calculate the elasticity tensor using the object 'material'.
C = material.getElasticityTensor(dimension);

% Check all symmetries
for i = 1:dimension
    for j = 1:dimension
        for k = 1:dimension
            for l = 1:dimension
                assert(C(i,j,k,l)==C(j,i,k,l),'First minor symmetry not fulfilled!')
                assert(C(i,j,k,l)==C(i,j,l,k),'Second minor symmetry not fulfilled!')
                assert(C(i,j,k,l)==C(k,l,i,j),'Major symmetry not fulfilled!')
            end
        end
    end
end
disp('No assertions thrown, so everything seems to be fine.')
