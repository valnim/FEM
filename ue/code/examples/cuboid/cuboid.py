import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import LinearStVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, FaceImpl
from soofea.analyzer.analysis import LinearAnalysis
from soofea.model.bc_handler import BCHandler

# displacement = 1.0e-3
q0 = 10000
lx = 200
ly = 200
force = lambda x, y, z: [0, 0, q0 * np.sin(np.pi * x / lx) * np.sin(np.pi * y / ly)]

class MyBCHandler(BCHandler):
    def integrateBC(self):

        #        for node in (set(self._model.getBoundary(2).node_list)): # & set(self._model.getBoundary(4).node_list)):
        #            node.setBCDOF(x=0.0)
        #
        # self._model.getNode(1).setBCDOF(x=0.0)

        # for node in self._model.getBoundary(1).node_list:
        # node.setBCDOF(y=0.0)

        # for node in self._model.getBoundary(2).node_list:
        # node.setBCDOF(y=displacement)

        for node in self._model.getBoundary(1).node_list:
            node.setBCDOF(x=0.0, y=0.0, z=0.0)

        # for node in self._model.getBoundary(2).node_list:
        #     node.setBCDOF(x=0.0, y=0.0, z=displacement)

        for face in self._model.getBoundary(2).component_list:  # Neumann Top
            for int_point in face.int_points:
                int_point.setSurfaceLoad(force)


def read():
    mesh_file_name = 'cuboid.msh'
    dimension = 3

    mesh_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], mesh_file_name)
    print(f"loading input file <{mesh_file_path}>...")
    input_handler = GmshInputHandler(mesh_file_path, dimension)
    model = Model(dimension)

    model.addType(ElementType(1, 1, 'hex', [2, 2, 2]))
    model.getType(1).height = 1.0
    model.getType(1).implementation = LinearElementImpl()

    model.addType(ElementType(3, 1, 'quad', [2, 2]))
    model.getType(3).height = 1.0
    model.getType(3).implementation = FaceImpl()

    model.addMaterial(LinearStVenantKirchhoffMaterial(1, 2.1e5, 0.3))

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = LinearAnalysis(model)

    return model, analysis
