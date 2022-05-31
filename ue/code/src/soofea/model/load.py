# This file is part of PySoofea
#
# SOOFEA - Software for Object Oriented Finite Element Analysis
#
# SOOFEA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import numpy as np


class Load:
    def __init__(self):
        pass


class ForceLoad(Load):
    def __init__(self, dimension):
        Load.__init__(self)
        self.force = np.zeros(dimension)
        '''A list with the same length as the dimension of the
            global coordinates system containing all force components.
            Initially all values are zero.'''

    def getValue(self, coord_id):
        return (self.force[coord_id])

    def setValue(self, coord_id, value):
        self.force[coord_id] = value
