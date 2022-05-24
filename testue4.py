import sys, os
import numpy as np

src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)


def tests():
    test_excercise1()


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


if __name__ == "__main__":
    tests()
