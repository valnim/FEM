import os
import numpy as np
from soofea.io.input_handler import GmshInputHandler
from soofea.model.type import ElementType, EdgeType
from soofea.model import Model
from soofea.model.material import StVenantKirchhoffMaterial
from soofea.analyzer.implementation import LinearElementImpl, LinearFaceImpl
from soofea.analyzer.analysis import LinearAnalysis
from soofea.model.bc_handler import BCHandler

# displacement = 1.0e-3
top_boundary = 2
q0 = 1.0e4
lx = 200
ly = 200
lz = 100
top_surface_force = lambda x, y, z: [0, 0, (q0*np.sin(np.pi*x/lx)*np.sin(np.pi*y/ly))]


class MyBCHandler(BCHandler):
    def integrateBC(self):
        for node in self._model.getBoundary(1).node_list:
            node.setBCDOF(x=0.0, y=0.0, z=0.0)

        # for node in self._model.getBoundary(2).node_list:
        #     node.setBCDOF(x=0.0, y=0.0, z=displacement)

        for face in self._model.getBoundary(top_boundary).component_list:  # Neumann Top
            for int_point in face.int_points:
                int_point.setSurfaceLoad(top_surface_force)

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
    model.getType(3).implementation = LinearFaceImpl()

    model.addMaterial(StVenantKirchhoffMaterial(1, 2.1e5, 0.3))
    #laut Angabe E-Modul 2.1e6 hier mit e5 gerechnet weil wsl Stahl gmeint

    input_handler.readMesh(model)

    model.addBCHandler(MyBCHandler())

    analysis = LinearAnalysis(model)
    
    return(model, analysis)
