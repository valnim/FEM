import os
import sys
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import soofea.model.shape
import soofea.numeric.num_int
from soofea.numeric.num_int import methodIntegrate
from soofea.analyzer.jacobian import ElementJacobian
from soofea.model.material import LinearStVenantKirchhoffMaterial
from soofea.model.model import Model
from soofea.model.model import Node
from soofea.model.model import Element
from soofea.model.type import ElementType
from soofea.analyzer.implementation import LinearElementImpl

# Exercise 1
print("### Excercise 1 ###")
ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plateQuads"))
if ex_path not in sys.path:
    sys.path.append(ex_path)

import plateQuads

model, analysis = plateQuads.read()

# for node in model._node_dict.values():
#     print(f"Node {node.number:3}: {node.coordinates}")

print(f"Coordinates of Node 89: {model._node_dict[89].undeformed_coordinates}")
print(f"Nodes of Element 23: {model._element_dict[23+40].node_number_list}")
print(f"Coordinates of Element 23: {model._element_dict[23+40].getCoordinateArray()}")
print(f"No. of Faces on Boundary 3: {len(model._boundary_dict[3].component_list)}")

# Exercise 2
print("\n### Excercise 2 ###")
shape = soofea.model.shape.QuadShape(1)
edges = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
print(f"N{edges[0]}:\n{shape.getArray(edges[0])}\n"
      f"N{edges[1]}:\n{shape.getArray(edges[1])}\n"
      f"N{edges[2]}:\n{shape.getArray(edges[2])}\n"
      f"N{edges[3]}:\n{shape.getArray(edges[3])}\n")

position = [0.75, 0.15]
print(f"dN{position}:\n{shape.getDerivativeArray(position)}\n")
print(f"dN3{position}:\n{shape.getDerivativeArray(position)[2]}")

# Exercise 3
print("\n### Excercise 3 ###")
integration_points = soofea.numeric.num_int.getIntPoints('quad', [3, 3])

print("Integration Points:")
data = pd.DataFrame(columns=['x', 'y', 'weight'])
for ip in integration_points:
    print(f"IP: natural coordinates: {np.round(ip.natural_coordinates, 5)}, weight: {np.round(ip.weight, 5)}")
    data.loc[len(data)] = [ip.natural_coordinates[0], ip.natural_coordinates[1], ip.weight]

# Please note that the weight and coordinates can be found in the tooltip of the IP's
fig = go.Figure()
fig.add_trace(go.Scatter(x=np.hstack([edges[:, 0], edges[0, 0]]), y=np.hstack([edges[:, 1], edges[0, 1]]),
                         name="reference quad element"))
fig.add_trace(go.Scatter(x=data['x'], y=data['y'], mode='markers', name="integration points",
                         hovertemplate='x: %{x}' + '<br>y: %{y}<br>' + '%{text}',
                         text=['weight {}'.format(w) for w in data['weight']]))
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
  )
fig.show()

print(f"Sum of all weights: {data['weight'].sum()}")
# The sum of all weights must be the area of the reference quad, because the gauss quadratur in this case is
# A = integral(f(x, y) * weight * dx * dy). Since f(x, y) = 1 the integral is basically a sum of the weights.

# Exercise 4
print("\n### Excercise 4 ###")
# Create empty 2D model
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

# Test element creation
print(f"Element coordinates:\n{element.getCoordinateArray()}")

# Create Type and output it for testing purposes
# Note: The first parameter to ElementType is an integer number, since
#       the types of the model are numbered in Python.
# Note: The number of IPs must be given in a list per coordinate direction
el_type_number = 1
order = 1
geom = 'quad'
n_int = [2, 2]

el_type = ElementType(el_type_number, order, geom, n_int)

# Bring together element and its type
element.setType(el_type)

# Output integration point coordinates
print("\nIntegration point natural coordinates:")
for ip in element.int_points:
    print(f"{ip.getNaturalCoordinates()}")

print("\nIntegration point coordinates:")
for ip in element.int_points:
    print(f"{ip._coordinates}")

# Exercise 5
print("\n### Excercise 5 ###")

def fun(element, ip, parameters=None):
    jacobian = ElementJacobian(element, ip)
    return jacobian.getDet()

area = methodIntegrate(fun, element, element.int_points)
print(f"\nFlächeninhalt des Elements: {area}")

# Exercise 6
print("\n### Excercise 6 ###")

number = 1
E_mod = 210000
nu = 0.3
dim = 3

material = LinearStVenantKirchhoffMaterial(number, E_mod, nu)
C = material.getElasticityMatrix(dim)

broken = False
# Überprüfen Sie hier die 3 Symmetrien des Elastizitätstensors
for i in range(3):
    for j in range(3):
        if not np.array_equal(C[i, j, :, :], C[j, i, :, :]):
            print(f"minor symmetry broken for i={i}, j={j}")
            broken = True

for k in range(3):
    for l in range(3):
        if not np.array_equal(C[:, :, k, l], C[:, :, l, k]):
            print(f"minor symmetry broken for k={k}, l={l}")
            broken = True

for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                if not np.array_equal(C[i, j, k, l], C[k, l, i, j]):
                    print(f"minor symmetry broken for i={i}, j={j}, k={k}, l={l}")
                    broken = True

if not broken:
    print("Major symmetry fulfilled.")

# Exercise 6b
print("\n### Excercise 6b ###")
# Define function to be integrated
def fun(element: Element, ip, parameters=None):
    dimension = element.node_list[0].getDimension()
    number_of_nodes = element.getNumberOfNodes()

    dN = element.type.shape.getDerivativeArray(ip.getNaturalCoordinates())
    jacobian = ElementJacobian(element, ip)
    J = jacobian.getInv()
    J_det = jacobian.getDet()

    E_mod = 210000
    nu = 0.3
    lam = nu * E_mod / ((1 + nu) * (1 - 2 * nu))
    mu = E_mod / (2 * (1 + nu))
    delta = np.identity(dimension)

    C = np.zeros([dimension, dimension, dimension, dimension])
    for i in range(dimension):
        for j in range(dimension):
            for k in range(dimension):
                for l in range(dimension):
                    C[i, j, k, l] = lam * delta[i, j] * delta[k, l] + mu * (
                            delta[i, k] * delta[j, l] + delta[j, k] * delta[i, l])

    A = np.zeros([number_of_nodes, dimension, number_of_nodes, dimension])
    for idx in range(number_of_nodes):
        for jdx in range(dimension):
            for kdx in range(number_of_nodes):
                for ldx in range(dimension):
                    for mdx in range(dimension):
                        for ndx in range(dimension):
                            for odx in range(dimension):
                                for pdx in range(dimension):
                                    A[idx, jdx, kdx, ldx] = A[idx, jdx, kdx, ldx] + C[mdx, ldx, ndx, jdx] \
                                                            * dN[idx, odx] * J[odx, ndx] \
                                                            * dN[kdx, pdx] * J[pdx, mdx] * J_det

    return A


# Use methodIntegrate to integrate the function numerically.
stiffness_matrix = methodIntegrate(fun, element, element.int_points)
stiffness_matrix_reshaped = stiffness_matrix.reshape((8, 8), order='F')
# the reshape does not reshape it so that it looks like the matrix in the assignment, since the display is only a
# convention and the variable stiffness_matrix will be used for all calculations anyways, this is not an issue
print(f"Elementsteifigkeitsmatrix:\n{stiffness_matrix_reshaped}")

# Exercise 6c
print("\n### Excercise 6c ###")
element.type.height = 1.0

number = 1
E_mod = 210000
nu = 0.3
material = LinearStVenantKirchhoffMaterial(number, E_mod, nu, 'plane_strain')
element.material = material

implementation = LinearElementImpl()
element.type.implementation = implementation

K_elem = element.type.implementation.calcStiffness(element)

print(K_elem)
