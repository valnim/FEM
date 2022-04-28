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

class NumberedObject:
    '''
    Most classes of the :py:mod:`soofea.model.model` are subclasses of
    this class. It adds a property :py:attr:`number` which
    represents a unique number for each object of this type in the model.
    Each :py:class:`soofea.model.model.Node`, :py:class:`soofea.model.model.Element`
    aso. has its unique global number. It is important
    for the assembling algorithm that the nodes have strictly increasing global
    numbers. This is not necessary for the other objects. In general the global
    numbers start with 1
    '''

    def __init__(self, number):
        self.number = number
        '''A unique number starting with 1'''
