import sys, os
import numpy as np

src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)


def tests():
    #test_excercise1()
    test_nonlinear_elementimpl()


def test_excercise1():
    from soofea.model.material import HyperelasticStVenantKirchhoffMaterial

    number = 1
    E_mod = 210000
    nu = 0.3
    dim = 2

    material = HyperelasticStVenantKirchhoffMaterial(number, E_mod, nu, 'plane_strain')

    I = np.identity(dim)
    F = I
    Egreen = 0.5 * (np.transpose(F)*F-I)

    S = material.getSecondPK(Egreen)
    print(S)

    C = material.getElasticityMatrix(Egreen)
    C = np.reshape(C, (dim**2, dim**2), 'F')
    print(C)
    print()


def test_nonlinear_elementimpl():
    from soofea.analyzer.implementation import NonlinearElementImpl
    from soofea.model.material import HyperelasticStVenantKirchhoffMaterial

    # The element is created using an existing script.
    # It has the following node coordinates:
    # x1 = (1/2)
    # x2 = (4/1)
    # x3 = (4/5)
    # x4 = (1/3)
    element = test_type()

    # An object of type nsAnalyzer.nsImplentation.NonlinearElementImpl is
    # created.
    # This object is assigned to the type of the element:
    impl = NonlinearElementImpl()
    element.type.implementation = impl

    # The material is created with the material parameters E_mod = 210000 und
    # nu = 0.3 for plane strain.
    # Then the material is assigned to the element.
    number = 1
    E_mod = 210000
    nu = 0.3
    dim = 2

    material = HyperelasticStVenantKirchhoffMaterial(number, E_mod, nu, 'plane_strain')
    element.material = material

    # The element stiffness matrix is calculated according to the nonlinear
    # theory:
    print('A =')
    A = element.type.implementation.calcStiffness(element)
    print(A)

    # The element force vector is calculated according to the nonlinear theory:
    print('F_int = ')
    F_int = element.type.implementation.calcLoad(element)
    print(F_int)


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

if __name__ == "__main__":
    tests()
