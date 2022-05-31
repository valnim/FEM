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
    test_plateQuads()
    test_numint_2d()
    test_quad_shape_interpolation()
    test_type()
    test_jacobian()
    test_material()
    test_stiffness_b()
    test_stiffness()
    testDOF()
    testAnalsysis()


def test_plateQuads():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plateQuads"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import plateQuads

    model, analysis = plateQuads.read()

    print('Node Nr. 89: ' + str(model._node_dict[89].undeformed_coordinates) + '\n')
    print('Element Nr. 23: ' + str(model._element_dict[63].node_number_list) + '\n')
    print('Node Nr. 51: ' + str(model._node_dict[51].undeformed_coordinates) + '\n')
    print('Node Nr. 60: ' + str(model._node_dict[60].undeformed_coordinates) + '\n')
    print('Node Nr. 61: ' + str(model._node_dict[61].undeformed_coordinates) + '\n')
    print('Node Nr. 52: ' + str(model._node_dict[52].undeformed_coordinates) + '\n')
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


def testDOF():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plateDOF"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import plateDOF

    model, analysis = plateDOF.read()

    for node in model._node_dict.values():
        print(f"Node {node.number:3}: {node.undeformed_coordinates}")

    analysis.run()
    print()

def testAnalsysis():
    import os, sys
    from soofea.io.output_handler import VTKOutputHandler

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/plateAnalysis"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import plateAnalysis

    model, analysis = plateAnalysis.read()

    for node in model._node_dict.values():
        print(f"Node {node.number:3}: {node.undeformed_coordinates}")



    output_file_name = 'plateAnalysis.vtk'
    force_overwrite = True
    output_handler = VTKOutputHandler(output_file_name, model.dimension, force_overwrite=force_overwrite)
    analysis.run(output_handler)

    print()

def test_input_corner():
    import os, sys

    ex_path = str(os.path.join(os.path.abspath(sys.path[0]), "examples/corner2d"))
    if ex_path not in sys.path:
        sys.path.append(ex_path)

    import corner2d

    model, analysis = corner2d.read()

    for node in model._node_dict.values():
        print(f"Node {node.number:3}: {node.undeformed_coordinates}")

    analysis.run()
    print()


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

    position = [0.75, 0.15]
    position_one_node = [1, 1]
    N = shape.getArray(position_one_node)
    der = shape.getDerivativeArray(position)
    f = func(position[0], position[0])
    f_inter = func_hat @ N


    print(f"Exakter Funktionswert an anderen Nodes Coordinaten: {N}")
    #print(f"Interpolierter Funktionswert: {f_inter}")
    print(f"Derrivative: {der[2,1]}")
    print('Fertig')

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

    integration_points = soofea.numeric.num_int.getIntPoints('quad', [3, 3])

    print(integration_points)

    A = 0
    for ip in integration_points:
        print(ip.natural_coordinates)
        print(ip.weight)
        A += ip.weight
    print(A)
    print('Fertig')


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

    material = StVenantKirchhoffMaterial(number, E_mod, nu, 'plane_strain')
    C = material.getElasticityMatrix(dim)

    broken = False
    # Überprüfen Sie hier die 3 Symmetrien des Elastizitätstensors
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if C[i, j, k, l] != C[j, i, k, l]:
                        print(f"minor symmetry broken for i={i}, j={j}, k={k}, l={l}")
                        broken = True
                    if C[i, j, k, l] != C[i, j, l, k]:
                        print(f"minor symmetry broken for i={i}, j={j}, k={k}, l={l}")
                        broken = True
                    if C[i, j, k, l] != C[k, l, i, j]:
                        print(f"minor symmetry broken for i={i}, j={j}, k={k}, l={l}")
                        broken = True

    if not broken:
        print("Major symmetry fulfilled.")


def test_stiffness():
    from soofea.analyzer.implementation import LinearElementImpl
    from soofea.model.material import StVenantKirchhoffMaterial
    import numpy as np

    element = test_type()


    element.material = StVenantKirchhoffMaterial(1, 2.1e5, 0.3)
    impl = LinearElementImpl()
    A = impl.calcStiffness(element)

    print(A)
    print()

def test_stiffness_b():
    from soofea.model.model import Element
    from soofea.model.material import StVenantKirchhoffMaterial
    from soofea.analyzer.jacobian import ElementJacobian
    from soofea.numeric.num_int import methodIntegrate


    def fun(element: Element, ip, parameters=None):
        import numpy as np

        E_mod = 210000
        nu = 0.3

        dimension = element.node_list[0].getDimension()
        number_of_nodes = element.getNumberOfNodes()
        dofs_per_element = dimension * number_of_nodes

        dN = element.type.shape.getDerivativeArray(ip.getNaturalCoordinates())
        jacobian = ElementJacobian(element, ip)
        J = jacobian.getInv()
        J_det = jacobian.getDet()

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

        A = np.zeros([dimension, number_of_nodes, dimension, number_of_nodes])
        for i in range(dimension):
            for j in range(number_of_nodes):
                for k in range(dimension):
                    for l in range(number_of_nodes):
                        for m in range(dimension):
                            for n in range(dimension):
                                for o in range(dimension):
                                    for p in range(dimension):
                                        A[i, j, k, l] += C[i, m, k, n] * dN[l, o] * J[o, n] * dN[j, p] * J[
                                            p, m] * J_det
        return np.reshape(A, (dofs_per_element, dofs_per_element), order='F')

    element = test_type()
    element.material = StVenantKirchhoffMaterial(1, 2.1e5, 0.3)
    A = methodIntegrate(fun, element, element.int_points)

    print(A)
    print()




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
