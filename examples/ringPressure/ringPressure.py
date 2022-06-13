import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial, HyperelasticStVenantKirchhoffMaterial, NeoHookeanMaterial
from soofea.analyzer.implementation import LinearElementImpl, LinearFaceImpl, NonlinearElementImpl, NonlinearFaceImpl
from soofea.analyzer.analysis import LinearAnalysis, NonlinearAnalysis
from soofea.model.bc_handler import BCHandler



class MyBCHandler(BCHandler):
    def integrateBC(self, time_stamp=0):
        bottom_boundary = 3
        left_boundary = 4
        ellipsis_boundary = 1
        pressure = 5e2 * time_stamp.time / self._model.time_bar[-1].time

        for node in self._model.getBoundary(bottom_boundary).node_list:
            node.setBCIncrement(y=0.0)
        for node in self._model.getBoundary(left_boundary).node_list:
            node.setBCIncrement(x=0)
        for face in self._model.getBoundary(ellipsis_boundary).component_list:
            for int_point in face.int_points:
                int_point.setPressure(pressure)

def read():
    mesh_file_name = 'ringPressure.msh'
    dimension = 2
    number_of_time_steps = 5
    total_time = 1.0
    convergence_criterion = 1e-9
    max_iterations = 100

    mesh_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], mesh_file_name)
    print(f"loading input file <{mesh_file_path}>...")
    input_handler = GmshInputHandler(mesh_file_path, dimension)
    model = Model(dimension)

    for i in range(number_of_time_steps):
        time = (i + 1) * total_time / number_of_time_steps
        model.addTimeStep(time)

    model.addType(ElementType(1, 1, 'quad', [2, 2]))
    model.getType(1).height = 1.0
    model.getType(1).implementation = NonlinearElementImpl()

    model.addType(EdgeType(2, 1, [2]))
    model.getType(2).height = 1.0
    model.getType(2).implementation = NonlinearFaceImpl()

    model.addMaterial(NeoHookeanMaterial(1, 1.5e3, 0.4, 'plane_strain'))

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = NonlinearAnalysis(model, convergence_criterion, max_iterations)

    return model, analysis
