import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial, HyperelasticStVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, NonlinearFaceImpl, NonlinearElementImpl
from soofea.analyzer.analysis import LinearAnalysis, NonlinearAnalysis
from soofea.model.bc_handler import BCHandler




class MyBCHandler(BCHandler):
    def integrateBC(self, time_stamp=0):

        bottom_boundary = 1

        for node in self._model.getBoundary(bottom_boundary).node_list:
            node.setBCIncrement(x=0.0, y=0.0, z=0.0)

        top_boundary = 2
        alpha_total = 2 * np.pi
        delta_alpha = alpha_total / (len(self._model.time_bar) - 1)

        for node in self._model.getBoundary(top_boundary).node_list:
            coords_old = node.spatial_coordinates
            x_old = coords_old[0]
            y_old = coords_old[1]

            r_old = np.sqrt(x_old**2 + y_old**2)
            j_old = np.arctan2(y_old, x_old)

            r_new = r_old
            j_new = j_old + delta_alpha

            x_new = r_new * np.cos(j_new)
            y_new = r_new * np.sin(j_new)

            dx = x_new - x_old
            dy = y_new - y_old

            node.setBCIncrement(x=dx, y=dy)


def read():
    mesh_file_name = 'twist.msh'
    dimension = 2
    number_of_time_steps = 32
    total_time = 1.0
    convergence_criterion = 1e-10
    max_iterations = 20

    mesh_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], mesh_file_name)
    print(f"loading input file <{mesh_file_path}>...")
    input_handler = GmshInputHandler(mesh_file_path, dimension)
    model = Model(dimension)

    for i in range(number_of_time_steps):
        time = (i + 1) * total_time / number_of_time_steps
        model.addTimeStep(time)

    model.addType(ElementType(1, 1, 'hex', [2, 2, 2]))
    model.getType(1).height = 1.0
    model.getType(1).implementation = NonlinearElementImpl()

    model.addType(ElementType(2, 1, 'quad', [2, 2]))
    model.getType(2).height = 1.0
    model.getType(2).implementation = NonlinearFaceImpl()

    model.addMaterial(HyperelasticStVenantKirchhoffMaterial(1, 2.1e5, 0.3, 'plane_strain'))

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = NonlinearAnalysis(model, convergence_criterion, max_iterations)

    return model, analysis
