import numpy as np

from soofea.analyzer.implementation import NonLinearElementImpl
from soofea.model.material import HyperelasticStVenantKirchhoffMaterial
from soofea.model.model import Model
from soofea.model.model import Node
from soofea.model.model import Element
from soofea.model.type import ElementType

### Exercise 1 ###
number = 1
E_mod = 210000
nu = 0.3

material = HyperelasticStVenantKirchhoffMaterial(number, E_mod, nu)
dim = 2
F_undeformed = np.identity(dim)
E_green = 1/2 * (F_undeformed.T @ F_undeformed - np.identity(dim))
S_undeformed = material.getSecondPK(E_green)
print(f"S_undeformed:\n{S_undeformed}")
C = material.getElasticityMatrix(E_green)
print(f"\nC:\n{np.reshape(C, (dim**2, dim**2), 'F')}")

### Exercise 2 ###
dimension = 2
my_model = Model(dimension)

# Create nodes and add them to model
node_number_list = [1, 2, 3, 4]
node_coord_list = np.array([[1, 2],
                            [4, 1],
                            [4, 5],
                            [1, 3]])
for node_number, node_coord in zip(node_number_list, node_coord_list):
    my_model.addNode(Node(node_number, node_coord))

# Create element and add it to model
element_number = 1
element_node_numbers = [1, 2, 3, 4]
element = Element(element_number, element_node_numbers)
my_model.addElement(element)

el_type_number = 1
order = 1
geom = 'quad'
n_int = [2, 2]
el_type = ElementType(el_type_number, order, geom, n_int)
element.setType(el_type)

element_implementation = NonLinearElementImpl()
element.type.implementation = element_implementation

number = 1
E_mod = 210000
nu = 0.3
material = HyperelasticStVenantKirchhoffMaterial(number, E_mod, nu)
element.material = material

print(f"\nA = 1e5 *\n{element.type.implementation.calcStiffness(element) / 1e5}")
print(f"\nF_int =\n{element.type.implementation.calcLoad(element)}")
