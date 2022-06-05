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
K = element.type.implementation.calcStiffness(element);
disp(K)