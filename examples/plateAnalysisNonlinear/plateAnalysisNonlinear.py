import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, FaceImpl, NonlinearElementImpl
from soofea.analyzer.analysis import LinearAnalysis, NonlinearAnalysis
from soofea.model.bc_handler import BCHandler

displacement = 0.1


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
            node.setBCDOF(x=0.0, y=0.0)
        for node in self._model.getBoundary(3).node_list:
            node.setBCDOF(x=0, y=displacement)


def read():
    mesh_file_name = 'plateAnalysisNonlinear.msh'
    dimension = 2
    number_of_timesteps = 5
    total_time = 1.0
    convergence_criterion = 1e-10
    max_iterations = 100

    mesh_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], mesh_file_name)
    print(f"loading input file <{mesh_file_path}>...")
    input_handler = GmshInputHandler(mesh_file_path, dimension)
    model = Model(dimension)

    for i in range(number_of_timesteps):
        time = i * total_time / number_of_timesteps
        # model.addTimeStep(time) # TODO


    model.addType(ElementType(1, 1, 'quad', [2, 2]))
    model.getType(1).height = 1.0
    model.getType(1).implementation = NonlinearElementImpl()

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

    return (model, analysis)