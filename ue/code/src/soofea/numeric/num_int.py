# This file is part of PySoofea
#
# SOOFEA - Software for Object Oriented Finite Element Analysis
# Copyright (C) 2012 Michael E. Hammer
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

from math import sqrt
import scipy.special
import numpy as np
import unittest
import math


class IntegrationPoint:
    '''
    IntegrationPoint for the model namespace. Each Element, Edge,
    Face (as subclass of Type) gets its own soofea.model.IntegrationPoint.
    '''

    def __init__(self, weight, natural_coordinates):
        self.weight = weight
        self.natural_coordinates = natural_coordinates

    def getWeight(self):
        return self.weight


class TetraIntegrationPoints:
    a = (5 + 3 * sqrt(5)) / 20
    b = (5 - sqrt(5)) / 20
    c = (1 + sqrt(5. / 14)) / 4
    d = (1 - sqrt(5. / 14)) / 4
    int_points = {1: [[[1. / 4, 1. / 4, 1. / 4], 1.6]],
                  4: [[[a, b, b], 1. / 24],
                      [[b, a, b], 1. / 24],
                      [[b, b, a], 1. / 24],
                      [[b, b, b], 1. / 24]],
                  5: [[[1. / 4, 1. / 4, 1. / 4], -4. / 30],
                      [[1. / 2, 1. / 6, 1. / 6], 9. / 120],
                      [[1. / 6, 1. / 2, 1. / 6], 9. / 120],
                      [[1. / 6, 1. / 6, 1. / 2], 9. / 120],
                      [[1. / 6, 1. / 6, 1. / 6], 9. / 120]],
                  11: [[[1. / 4, 1. / 4, 1. / 4], -74. / 5625],
                       [[11. / 14, 1. / 14, 1. / 14], 343. / 45000],
                       [[1. / 14, 11. / 14, 1. / 14], 343. / 45000],
                       [[1. / 14, 1. / 14, 11. / 14], 343. / 45000],
                       [[1. / 14, 1. / 14, 1. / 14], 343. / 45000],
                       [[c, c, d], 56. / 2250],
                       [[c, d, c], 56. / 2250],
                       [[c, d, d], 56. / 2250],
                       [[d, c, c], 56. / 2250],
                       [[d, c, d], 56. / 2250],
                       [[d, d, c], 56. / 2250]]}

    def __init__(self):
        pass


class TriangleIntegrationPoints:
    int_points = {1: [[[1. / 3, 1. / 3], 1 / 2.]],
                  3: [[[2. / 3, 1. / 6], 1. / 6],
                      [[1. / 6, 2. / 3], 1. / 6],
                      [[1. / 6, 1. / 6], 1. / 6]],
                  4: [[[1. / 3, 1. / 3], -9. / 32],
                      [[6. / 10, 2. / 10], 25. / 96],
                      [[2. / 10, 6. / 10], 25. / 96],
                      [[2. / 10, 2. / 10], 25. / 96]],
                  6: [[[0.816847572980459, 0.091576213509771], 0.109951743655322 / 2],
                      [[0.091576213509771, 0.816847572980459], 0.109951743655322 / 2],
                      [[0.091576213509771, 0.091576213509771], 0.109951743655322 / 2],
                      [[0.108103018168070, 0.445948490915965], 0.223381589678011 / 2],
                      [[0.445948490915965, 0.108103018168070], 0.223381589678011 / 2],
                      [[0.108103018168070, 0.108103018168070], 0.223381589678011 / 2]],
                  7: [[[1. / 3, 1. / 3], 0.225],
                      [[0.797426985353087, 0.101286507323456], 0.125939150844827 / 2],
                      [[0.101286507323456, 0.797426985353087], 0.125939150844827 / 2],
                      [[0.101286507323456, 0.101286507323456], 0.125939150844827 / 2],
                      [[0.059715871789770, 0.470142064105115], 0.132394152788506 / 2],
                      [[0.470142064105115, 0.059715871789770], 0.132394152788506 / 2],
                      [[0.470142064105115, 0.470142064105115], 0.132394152788506 / 2]]}

    def __init__(self):
        pass


def getIntPoints(shape_type, number_of_int_points):
    ip_data = []
    math_ips = []
    if (shape_type == 'linear' or shape_type == 'quad' or shape_type == 'hex'):
        for coord_number in number_of_int_points:
            [coords, weights] = scipy.special.orthogonal.p_roots(coord_number)
            ip_data.append(np.array([coords.real, weights]))

        if (shape_type == 'linear'):
            for i in range(len(ip_data[0][0])):
                math_ips.append(IntegrationPoint(ip_data[0][1][i],
                                                 [ip_data[0][0][i]]))
        elif (shape_type == 'quad'):
            for i in range(len(ip_data[0][0])):
                for j in range(len(ip_data[1][0])):
                    math_ips.append(IntegrationPoint(ip_data[0][1][i] * ip_data[1][1][j],
                                                     [ip_data[0][0][i], ip_data[1][0][j]]))
        elif (shape_type == 'hex'):
            for i in range(len(ip_data[0][0])):
                for j in range(len(ip_data[1][0])):
                    for k in range(len(ip_data[2][0])):
                        math_ips.append(IntegrationPoint(ip_data[0][1][i] * ip_data[1][1][j] * ip_data[2][1][k],
                                                         [ip_data[0][0][i], ip_data[1][0][j], ip_data[2][0][k]]))
    elif (shape_type == 'triangle' or shape_type == 'tetra'):
        if (shape_type == 'triangle'):
            ip_data = TriangleIntegrationPoints.int_points[number_of_int_points]
        elif (shape_type == 'tetra'):
            ip_data = TetraIntegrationPoints.int_points[number_of_int_points]
        for ip in ip_data:
            math_ips.append(IntegrationPoint(ip[1], ip[0]))
    else:
        raise Exception("No integration points for the given shape type '" + shape_type + "' implemented")
    return (math_ips)


def integrate(function, int_points):
    ival = 0.0
    for ip in int_points:
        ival += function(ip) * ip.getWeight()
    return ival


def methodIntegrate(function, obj, integration_points, parameters=None):
    ival = function(obj, integration_points[0], parameters) * \
           integration_points[0].getWeight()

    for ip in integration_points[1:]:
        ival += function(obj, ip, parameters) * ip.getWeight()
    return ival


def testFunction(int_point):
    x_i = int_point.natural_coordinates[0]
    # return x_i**2
    return math.cos(x_i)


if __name__ == '__main__':
    int_points_list = []
    int_points_list.append(getIntPoints('linear', [1]))
    int_points_list.append(getIntPoints('linear', [2]))
    int_points_list.append(getIntPoints('linear', [3]))
    int_points_list.append(getIntPoints('linear', [4]))

    for int_points in int_points_list:
        print(f'numeric integral evaluated with {len(int_points)} integration points:\n')
        result = integrate(testFunction, int_points)
        print(f'\t{result}\n')
