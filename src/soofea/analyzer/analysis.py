# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:57:56 2014

@author: matthiasrambausek
"""

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from math import fabs


class Analysis:
    def __init__(self, model):
        self._model = model

    def stiffnessAssembler(self, node_container, local_stiffness, global_stiffness):
        nr_of_entries = local_stiffness.shape[0] / \
                        node_container.type.shape.getNumberOfNodes()

        for local_row_counter in range(local_stiffness.shape[0]):
            for local_col_counter in range(local_stiffness.shape[1]):
                row_node = node_container.getNode(
                    int(local_row_counter / nr_of_entries)
                )
                col_node = node_container.getNode(
                    int(local_col_counter / nr_of_entries)
                )
                row_coord_offset = local_row_counter % nr_of_entries
                col_coord_offset = local_col_counter % nr_of_entries

                global_row_index = (row_node.number - 1) * nr_of_entries + \
                                   row_coord_offset

                global_col_index = (col_node.number - 1) * nr_of_entries + \
                                   col_coord_offset

                global_stiffness[global_row_index, global_col_index] += \
                    local_stiffness[local_row_counter, local_col_counter]

    def loadAssembler(self, node_container, local_load, global_load):
        nr_of_entries = len(local_load) // node_container.type.shape.getNumberOfNodes()
        for local_counter in range(len(local_load)):
            node = node_container.getNode(local_counter // nr_of_entries)
            coord_offset = local_counter % nr_of_entries
            global_index = (node.number - 1) * nr_of_entries + coord_offset
            global_load[global_index] += local_load[local_counter]

    def assembleStiffness(self, global_stiffness):
        print('\--> Assemble global stiffness')
        for element in self._model._element_dict.values():
            K_elem = element.type.implementation.calcStiffness(element)
            self.stiffnessAssembler(element, K_elem, global_stiffness)

    def assembleLoad(self, global_load):
        print('\--> Assemble global load')
        for boundary in self._model._boundary_dict.values():
            for face in boundary.component_list:
                F_surface_face = face.type.implementation.calcSurfaceLoad(face)
                self.loadAssembler(face, F_surface_face, global_load)
        for element in self._model._element_dict.values():
            F_volume = element.type.implementation.calcLoad(element)
            self.loadAssembler(element, F_volume, global_load)


    def integrateDirichletBC(self, global_stiffness, global_load):
        print('\--> Integrate Dirichlet BC')
        for node in self._model._node_dict.values():
            for coord_index in range(self._model.dimension):
                if node.dof.getConstraint(coord_index):
                    global_col_index = (node.number - 1) * self._model.dimension + \
                                       coord_index
                    for row_counter in range(global_stiffness.shape[0]):
                        if row_counter == global_col_index:
                            global_load[row_counter] = \
                                global_stiffness[row_counter, row_counter] * \
                                node.dof.getValue(coord_index)
                        else:
                            global_load[row_counter] -= \
                                global_stiffness[row_counter, global_col_index] * \
                                node.dof.getValue(coord_index)

                    temp = global_stiffness[global_col_index, global_col_index]
                    global_stiffness[:, global_col_index] = 0.0
                    global_stiffness[global_col_index, :] = 0.0
                    global_stiffness[global_col_index, global_col_index] = temp

    def integrateNeumannBC(self, global_load):
        print('\--> Integrate Neumann BC')
        for node in self._model._node_dict.values():
            f_load = node.load
            # if not np.allclose(f_load, np.zeros_like(f_load)):
            if not np.all(f_load == 0.0):
                for coord_index in range(self._model.dimension):
                    global_index = (node.number - 1) * self._model.dimension + \
                                   coord_index
                    global_load[global_index] += f_load.getValue(coord_index)

    def updateDOF(self, solution_vector):
        for node in self._model._node_dict.values():
            for coord_index in range(self._model.dimension):
                global_index = (node.number - 1) * self._model.dimension + \
                               coord_index
                node.dof.setDisplacement(coord_index,
                                         solution_vector[global_index])

    def solveFESystem(self):
        number_of_unknowns = self._model.getNumberOfUnknowns()

        global_load = np.zeros(number_of_unknowns)
        global_stiffness = lil_matrix((number_of_unknowns, number_of_unknowns))

        self.assembleStiffness(global_stiffness)
        self.assembleLoad(global_load)

        self.integrateNeumannBC(global_load)
        self.integrateDirichletBC(global_stiffness, global_load)

        print(
            f"Sparsity of Stiffness matrix: {1 - global_stiffness.nnz / (global_stiffness.shape[0] * global_stiffness.shape[1])}")
        print("\-> Solving System ...")
        displacement = spsolve(global_stiffness.tocsr(), global_load)

        print("\-> ... done")

        self.updateDOF(displacement)
        return fabs(np.dot(displacement, global_load))


class LinearAnalysis(Analysis):
    def __init__(self, model):
        Analysis.__init__(self, model)

    def run(self, output_handler=None):
        print("-> Linear analysis")
        self._model.bc_handler.integrateBC()
        self.solveFESystem()

        if not output_handler == None:
            output_handler.write(self._model)
