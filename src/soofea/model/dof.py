import numpy as np


class DOF:
    def __init__(self):
        pass


class DisplacementDOF(DOF):
    def __init__(self, dimension):
        DOF.__init__(self)
        self._constraint = np.zeros(dimension, dtype='bool')
        self._displacements = np.zeros(dimension)

    def getValue(self, coord_id):
        return self._displacements[coord_id]

    def getConstraint(self, coord_id):
        return self._constraint[coord_id]

    def setConstraintValue(self, coord_id, value):
        self._constraint[coord_id] = True
        self._displacements[coord_id] = value

    def setDisplacement(self, coord_id, value):
        self._displacements[coord_id] = value
