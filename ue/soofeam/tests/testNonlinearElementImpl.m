# The element is created using an existing script.
# It has the following node coordinates:
# x1 = (1/2)
# x2 = (4/1)
# x3 = (4/5)
# x4 = (1/3)
testElementType

# An object of type nsAnalyzer.nsImplentation.NonlinearElementImpl is
# created.
# This object is assigned to the type of the element:
element_implementation = nsAnalyzer.nsImplementation.NonlinearElementImpl();
element.type.setImplementation(element_implementation);

# The material is created with the material parameters E_mod = 210000 und
# nu = 0.3 for plane strain.
# Then the material is assigned to the element.
material = nsModel.nsMaterial.HyperelasticStVenantKirchhoffMaterial(210000, 0.3, 'plane_strain');
element.setMaterial(material);

# The element stiffness matrix is calculated according to the nonlinear
# theory:
disp('A =')
A = element.type.implementation.calcStiffness(element);
disp(A)

# The element force vector is calculated according to the nonlinear theory:
disp('F_int = ')
F_int = element.type.implementation.calcLoad(element);
disp(F_int);