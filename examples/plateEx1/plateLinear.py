import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial, HyperelasticStVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, LinearFaceImpl, NonlinearElementImpl
from soofea.analyzer.analysis import LinearAnalysis, NonlinearAnalysis
from soofea.model.bc_handler import BCHandler



class MyBCHandler(BCHandler):
    def integrateBC(self, time_stamp=0):
        v = 10
        bottom_boundary = 1
        right_boundary = 2
        top_boundary = 3

        for node in self._model.getBoundary(bottom_boundary).node_list:
            node.setBCDOF(x=0.0, y=0.0)
        for node in self._model.getBoundary(right_boundary).node_list:
            node.setBCDOF(x=0)
        for node in self._model.getBoundary(top_boundary).node_list:
            node.setBCDOF(y=v)

def read():
    mesh_file_name = 'plateLinear.msh'
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
    model.getType(2).implementation = LinearFaceImpl()

    model.addMaterial(StVenantKirchhoffMaterial(1, 2.1e5, 0.3, 'plane_strain'))

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = LinearAnalysis(model)

    return (model, analysis)
