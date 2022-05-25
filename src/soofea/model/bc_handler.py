'''
Created on Nov 12, 2012

@author: mueli
'''

from abc import ABCMeta, abstractmethod


class BCHandler:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._model = None

    def setModel(self, model):
        self._model = model

    def resetBC(self):
        for node in self._model.node_list:
            for coord_id in range(node.getDimension()):
                node.dof_handler.resetDof(coord_id)

    def setPrescribedDOFZero(self):
        for node in self._model.node_list:
            for coord_id in range(node.getDimension()):
                if node.dof_handler.getConstraint(coord_id):
                    node.dof_handler.setConstraintValue(coord_id, 0.0)


    @abstractmethod
    def integrateBC(self, time_stamp):
        pass
