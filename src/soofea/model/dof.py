import numpy as np


class DOF:
    def __init__(self):
        pass


class DisplacementDOF(DOF):
    def __init__(self, dimension):
        DOF.__init__(self)
        self._constraint = np.zeros(dimension, dtype='bool')
        self._displacements = np.zeros(dimension)
        self._increment = np.zeros(dimension)

    def getValue(self, coord_id):
        return self._displacements[coord_id]

    def getConstraint(self, coord_id):
        return self._constraint[coord_id]

    def setConstraintValue(self, coord_id, value):
        self._constraint[coord_id] = True
        self._displacements[coord_id] = value

    def setDisplacement(self, coord_id, value):
        self._displacements[coord_id] = value

    def getDisplacements(self, coord_id):
        return self._displacements[coord_id]

    def getIncrement(self, coord_id):
        return self._increment[coord_id]

    def setConstraintIncrement(self, coord_id, increment):
        self._constraint[coord_id] = True
        self._increment[coord_id] = increment

    def resetDof(self, coord_id):
        self._increment[coord_id] = 0.0
        self._constraint[coord_id] = False

    def addIncrement(self, coord_id, increment):
        self._displacements[coord_id] += increment
        self._increment[coord_id] = increment
