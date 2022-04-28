import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, FaceImpl
from soofea.analyzer.analysis import LinearAnalysis
from soofea.model.bc_handler import BCHandler

displacement = 1.0e-3
top_boundary = 2
q0 = -1
s = 1
top_surface_force = lambda x, y: [0, q0]

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

        for node in self._model.getBoundary(4).node_list:
            node.setBCDOF(x=0.0, y=0.0)

        # for node in self._model.getBoundary(3).node_list:
        #     node.setBCDOF(x=displacement, y=displacement)

        for face in self._model.getBoundary(top_boundary).component_list:  # Neumann Top
            for int_point in face.int_points:
                int_point.setSurfaceLoad(top_surface_force)


def read():
    mesh_file_name = 'krag2d.msh'
    dimension = 2

    mesh_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], mesh_file_name)
    print(f"loading input file <{mesh_file_path}>...")
    input_handler = GmshInputHandler(mesh_file_path, dimension)
    model = Model(dimension)

    model.addType(ElementType(1, 1, 'quad', [2, 2]))
    model.getType(1).height = 1.0
    model.getType(1).implementation = LinearElementImpl()

    model.addType(EdgeType(2, 1, [2]))
    model.getType(2).height = 1.0
    model.getType(2).implementation = FaceImpl()
    #    model.addType(EdgeType(2,1, [3]))
    #    model.getType(2).height = 1.0;
    #    model.getType(2).implementation = None

    model.addMaterial(StVenantKirchhoffMaterial(1, 2.1e5, 0.3, 'plane_stress'))

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = LinearAnalysis(model)

    return model, analysis
