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
        for node in self._model.getNodes():
            for coord_id in range(self._model.dimension):
                node.dof.resetDOF(coord_id)

    def setPrescribedDOFZero(self):
        for node in self._model.getNodes():
            for coord_id in range(self._model.dimension):
                if node.dof.getConstraint(coord_id):
                    node.dof.setConstraintIncrement(coord_id, 0.0)

    @abstractmethod
    def integrateBC(self, time_stamp=0):
        pass
