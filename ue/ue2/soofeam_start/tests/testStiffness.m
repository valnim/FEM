% The element is created with the script from Exercises 4.
% This element has the following node coordinates:
% x1 = (1/2)
% x2 = (4/1)
% x3 = (4/5)
% x4 = (1/3)
testElementType

% An object with type nsAnalyzer.nsImplentation.LinearElementImpl is
% created.
% This object is assigned to the type of the element.
element_implementation = nsAnalyzer.nsImplementation.LinearElementImpl();
element.type.setImplementation(element_implementation);

% The material is created with E = 210000 and nu = 0.3 (plane strain)
% Then the material is assigned to the element.
material = nsModel.nsMaterial.LinearStVenantKirchhoffMaterial(210000, 0.3, 'plane_strain');
element.setMaterial(material);

% The element stiffness matrix is calculated according to the linear
% theory.
A = nsNumeric.NumInt.methodIntegrate(@stiffnessMatrixIntegrator, element.int_points, element);

% The stiffness matrix is displayed in the command window
disp(A)

function stiffness = stiffnessMatrixIntegrator(int_point, element)

% Dimension, number of nodes per element and number of DOFs per element are
% calculated.
dimension        = element.node_list(1).dimension;
number_of_nodes  = element.getNumberOfNodes();
dofs_per_element = number_of_nodes * dimension;

% Create the Jacobian object from type nsAnalyzer.nsJacobian.Jacobian and
% the dN matrix at the position of the integration point.
% jacobian =
% J        = jacobian.getMatrix();

% dN = element.type.shape.

% Calculate the elasticity tensor
% C = element.material.

% Calculate the determinant of the inverse Jacobian.
% J_inv_det = jacobian.

% After calculating all components, you can caluculate the stiffness matrix
% itself:
A = zeros(dimension,number_of_nodes,dimension,number_of_nodes);
for i = 1:dimension
    for j = 1:number_of_nodes
        for k = 1:dimension
            for l = 1:number_of_nodes
                for m = 1:dimension
                    for n = 1:dimension
                        for o = 1:dimension
                            for p = 1:dimension
                                % A(i,j,k,l) = A(i,j,k,l) + ...
                            end
                        end
                    end
                end
            end
        end
    end
end

% The four dimensional stiffness matrix (4 Indices) is reshaped into an
% ordinary matrix.
stiffness = reshape(A,[dofs_per_element dofs_per_element]);

end
