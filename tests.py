#! /usr/bin/env python3
""" ------------------------------------------------------------------
This file is part of SOOFEA Python.

SOOFEA - Software for Object Oriented Finite Element Analysis

SOOFEA is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
------------------------------------------------------------------ """

import sys, os
from soofea.io.output_handler import VTKOutputHandler

src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)


def tests():
    # Entfernen Sie das Kommentarzeichen vor dem jeweiligen unit-test.
    #    test_node()
    #    test_model()
    # test_input_plate()
    #    test_input_corner()
    #    test_input_circle()
    #    test_linear_shape()
    #    test_quad_shape_interpolation()
    #    test_numerical_integration()
    #    test_numint_2d()
    #    test_material()
    #    test_implementation()
    #    test_new_implementation()
    test_plateQuads()


def test_plateQuads():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plateQuads"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import plateQuads

    model, analysis = plateQuads.read()

    print('Node Nr. 89: ' + str(model._node_dict[89].coordinates) + '\n')
    print('Element Nr. 23: ' + str(model._edge_dict[23].node_number_list) + '\n')
    print('Node Nr. 24: ' + str(model._node_dict[24].coordinates) + '\n')
    print('Node Nr. 25: ' + str(model._node_dict[25].coordinates) + '\n')
    print('Boundary Nr. 3: ' + str(len(model._boundary_dict[3].component_list)) + '\n')
    print('wait')


def test_node():
    import numpy as np
    from soofea.model.model import Node

    # Koordinaten des Knotens
    n1_coords = np.array([3, 5.5])
    n1_number = 1

    # Erstellen Sie hier ein Objekt der Klasse Node
    n1 = Node(n1_number, n1_coords)
    print(n1)


def test_model():
    import numpy as np
    from soofea.model.model import Model
    from soofea.model.model import Node
    from soofea.model.model import Element
    from soofea.model.model import Edge

    dimension = 2

    my_model = Model(dimension)

    node_number_list = [1, 2, 3, 4, 5]
    node_coord_list = np.array([[0.0, 0.0],
                                [0.5, 0.0],
                                [0.5, 0.5],
                                [0.0, 0.5],
                                [1.0, 0.0]])
    for node_number, node_coord in zip(node_number_list, node_coord_list):
        my_model.addNode(Node(node_number, node_coord))

    element_number_list = [1]
    element_node_numbers_list = [[1, 2, 3, 4]]
    for element_number, element_node_numbers in zip(element_number_list,
                                                    element_node_numbers_list):
        my_model.addElement(Element(element_number, element_node_numbers))

    print(my_model._element_dict[1].getCoordinateArray())

    edge_number_list = [1, 2]
    edge_node_numbers_list = [[1, 2], [2, 5]]
    edge_boundary_number_list = [1, 1]
    for edge_number, edge_node_numbers, edge_boundary_number in \
            zip(edge_number_list, edge_node_numbers_list,
                edge_boundary_number_list):
        my_model.addEdge(Edge(edge_number, edge_node_numbers))
        my_model.appendComponentToBoundary(edge_boundary_number, edge_number,
                                           'edge')

    # Das Ausgeben des Modells im Terminal funktioniert nicht so wie ich mir das
    # vorgestellt habe - wer will, kann dem auf den Grund gehen.
    print(my_model)


def test_input_plate():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plate2d"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import plate2d

    model, analysis = plate2d.read()

    for node in model._node_dict.values():
        print(f"Node {node.number:3}: {node.coordinates}")

    analysis.run()


def test_input_corner():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/corner2d"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import corner2d

    model, analysis = corner2d.read()

    for node in model._node_dict.values():
        print(f"Node {node.number:3}: {node.coordinates}")

    analysis.run()


def test_input_circle():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/circle2d"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import circle2d

    model, analysis = circle2d.read()

    print(model)


def test_quad_shape_interpolation():
    import numpy as np
    import soofea.model.shape

    func = lambda xi, eta: np.sin(xi * eta * np.pi / 4)
    func_hat = np.array([func(-1, -1), func(1, -1), func(1, 1), func(-1, 1)])
    shape = soofea.model.shape.QuadShape(1)

    position = [0.5, 0.5]
    N = shape.getArray(position)
    f = func(position[0], position[1])
    f_inter = func_hat @ N

    print(f"Exakter Funktionswert: {f}")
    print(f"Interpolierter Funktionswert: {f_inter}")


def test_numerical_integration():
    import soofea.numeric.num_int

    f = lambda ip: 2 * ip.natural_coordinates[0] ** 4 - ip.natural_coordinates[0]

    n_ips_array = [[1], [2], [3], [4]]

    for n_ips in n_ips_array:
        integration_points = soofea.numeric.num_int.getIntPoints('linear', n_ips)
        result = soofea.numeric.num_int.integrate(f, integration_points)

        print(f"n ips:  {n_ips[0]}")
        print(f"result: {result}")


def test_numint_2d():
    import soofea.numeric.num_int

    integration_points = soofea.numeric.num_int.getIntPoints('quad', [2, 2])

    print(integration_points)

    for ip in integration_points:
        print(ip.coordinates)
        print(ip.weight)
        print()


def test_type():
    import numpy as np
    from soofea.model.model import Model
    from soofea.model.model import Node
    from soofea.model.model import Element
    from soofea.model.type import ElementType

    # Create empty 2D model
    dimension = 2
    my_model = Model(dimension)

    # Create nodes and add them to model
    node_number_list = [1, 2, 3, 4]
    a = np.sqrt(3)
    node_coord_list = np.array([[-a, -a],
                                [a, -a],
                                [a, a],
                                [-a, a]])
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

    print(f"\nElement type:\n{el_type}")

    # Bring together element and its type
    element.setType(el_type)

    # Output integration point coordinates
    print("\nIntegration point natural coordinates:")
    for ip in element.int_points:
        print(f"{ip.getNaturalCoordinates()}")

    print("\nIntegration point coordinates:")
    for ip in element.int_points:
        print(f"{ip._coordinates}")

    return element


def test_jacobian():
    from soofea.numeric.num_int import methodIntegrate
    from soofea.analyzer.jacobian import ElementJacobian

    element = test_type()

    def fun(element, ip, parameters=None):
        jacobian = ElementJacobian(element, ip)

        return jacobian.getDet()

    area = methodIntegrate(fun, element, element.int_points)
    print(f"\nFlächeninhalt des Elements:\n{area}")


def test_material():
    from soofea.model.material import StVenantKirchhoffMaterial

    number = 1
    E_mod = 210000
    nu = 0.3
    dim = 3

    material = StVenantKirchhoffMaterial(number, E_mod, nu)
    C = material.getElasticityMatrix(dim)

    broken = False
    # Überprüfen Sie hier die 3 Symmetrien des Elastizitätstensors
    for i in range(6):
        for j in range(6):
            if C[i, j] != C[j, i]:
                print(f"minor symmetry broken for i={i}, j={j}")
                broken = True

    if not broken:
        print("Major symmetry fulfilled.")


# def test_implementation():
#    from soofea.model.material import StVenantKirchhoffMaterial
#    from soofea.analyzer.implementation import LinearElementImpl

#    # Das Element wird mit dem bereits vorhandenen Script erstellt.
#    # Zur Erinnerung: Das Element hat folgende Knotenpunkte
#    # x1 = (-sqrt(3)/-sqrt(3))
#    # x2 = ( sqrt(3)/-sqrt(3))
#    # x3 = ( sqrt(3)/ sqrt(3))
#    # x4 = (-sqrt(3)/ sqrt(3))
#    element = test_type()
#    element.type.height = 1.0

#    number = 1
#    E_mod = 210000
#    nu = 0.3
#    material = StVenantKirchhoffMaterial(number, E_mod, nu, 'plane_stress')
#    element.material = material

#    implementation = LinearElementImpl()
#    element.type.implementation = implementation

#    element.type.implementation.calcStrainStressInIp(element)
#    K_elem = element.type.implementation.calcStiffness(element)

#    print(K_elem)


def test_new_implementation():
    from soofea.model.material import StVenantKirchhoffMaterial
    from soofea.analyzer.implementation import LinearElementImpl

    # Das Element wird mit dem bereits vorhandenen Script erstellt.
    # Zur Erinnerung: Das Element hat folgende Knotenpunkte
    # x1 = (-sqrt(3)/-sqrt(3))
    # x2 = ( sqrt(3)/-sqrt(3))
    # x3 = ( sqrt(3)/ sqrt(3))
    # x4 = (-sqrt(3)/ sqrt(3))
    element = test_type()
    element.type.height = 1.0

    number = 1
    E_mod = 210000
    nu = 0.3
    material = StVenantKirchhoffMaterial(number, E_mod, nu, 'plane_stress')
    element.material = material

    implementation = LinearElementImpl()
    element.type.implementation = implementation

    K_elem = element.type.implementation.calcStiffness(element)

    print(K_elem)


def testQuadShapeDer(self):
    import numpy as np
    import soofea.model.shape

    shape = soofea.model.shape.HexShape

    np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([-1, -1]),
                                   np.array([[-0.5, 0.5, 0, 0], [-0.5, 0, 0, 0.5]]).T)
    np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([1, -1]),
                                   np.array([[-0.5, 0.5, 0, 0], [0, -0.5, 0.5, 0]]).T)
    np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([1, 1]),
                                   np.array([[0, 0, 0.5, -0.5], [0, -0.5, 0.5, 0]]).T)
    np.testing.assert_almost_equal(self.qshape1.getDerivativeArray([-1, 1]),
                                   np.array([[0, 0, 0.5, -0.5], [-0.5, 0, 0, 0.5]]).T)


if __name__ == "__main__":
    tests()
