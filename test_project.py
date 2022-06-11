import sys, os
import numpy as np

src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)


def tests():
    test_excercise1()

def test_excercise1():
    from soofea.model.material import NeoHookeanMaterial
    from soofea.model.material import StVenantKirchhoffMaterial

    number = 1
    E_mod = 210000
    nu = 0.3
    dim = 2

    material1 = NeoHookeanMaterial(number, E_mod, nu, 'plane_strain')
    material2 = StVenantKirchhoffMaterial(number, E_mod, nu, 'plane_strain')

    Egreen = np.zeros((dim, dim))

    S1 = material1.getSecondPK(Egreen)
    print("NeoHookeanMaterial:")
    print(S1)

    C1 = material1.getElasticityMatrix(Egreen)
    C1 = np.reshape(C1, (dim**2, dim**2), 'F')
    print("NeoHookeanMaterial:")
    print(C1)
    C2 = material2.getElasticityMatrix(dim)
    C2 = np.reshape(C2, (dim**2, dim**2), 'F')
    print("StVenantKirchhoffMaterial:")
    print(C2)

    print()


if __name__ == "__main__":
    tests()
