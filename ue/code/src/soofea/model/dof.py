import numpy as np


class DOF:
    def __init__(self):
        pass


class DisplacementDOF(DOF):
    def __init__(self, dimension):
        DOF.__init__(self)
        self._constraints = np.zeros(dimension, dtype='bool')
        self._displacements = np.zeros(dimension)
        self._increments = np.zeros(dimension)

    def getDisplacements(self):
        return self._displacements

    def getDisplacement(self, coord_id):
        return self._displacements[coord_id]

    def setDisplacement(self, coord_id, value):
        self._displacements[coord_id] = value

    def getConstraint(self, coord_id):
        return self._constraints[coord_id]

    def setConstraintDisplacement(self, coord_id, displacement):
        self._constraints[coord_id] = True
        self._displacements[coord_id] = displacement

    def setConstraintIncrement(self, coord_id, increment):
        self._increments[coord_id] = increment
        self._constraints[coord_id] = True

    def getIncrement(self, coord_id):
        return self._increments[coord_id]

    def resetDOF(self, coord_id):
        self._increments[coord_id] = 0
        self._constraints[coord_id] = False

    def addIncrement(self, coord_id, increment):
        self._displacements[coord_id] = self._displacements[coord_id] + increment
        self._increments[coord_id] = increment
