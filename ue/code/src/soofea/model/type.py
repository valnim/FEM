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

from soofea.base import NumberedObject
from soofea.numeric.num_int import getIntPoints
from soofea.model.shape import QuadShape, TriShape, LinearShape, HexShape


class Type(NumberedObject):
    def __init__(self, number, shape_order, shape_type, number_of_int_points):
        NumberedObject.__init__(self, number)
        self.implementation = None
        if shape_type == 'quad':
            self.shape = QuadShape(shape_order)
        elif shape_type == 'triangle':
            self.shape = TriShape(shape_order)
        elif shape_type == 'linear':
            self.shape = LinearShape(shape_order)
        elif shape_type == 'hex':
            self.shape = HexShape(shape_order)
        else:
            raise Exception("The given shape type '" + shape_type + "' is not implemented")

        self._math_ips = getIntPoints(shape_type, number_of_int_points)

    def getMathIntegrationPoints(self):
        return self._math_ips


class ElementType(Type):
    def __init__(self, N, shape_order, shape_type, number_of_int_points):
        Type.__init__(self, N, shape_order, shape_type, number_of_int_points)


class EdgeType(Type):
    def __init__(self, N, shape_order, number_of_int_points):
        Type.__init__(self, N, shape_order, 'linear', number_of_int_points)
