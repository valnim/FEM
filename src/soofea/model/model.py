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
from soofea.base import NumberedObject
from soofea.model.dof import DisplacementDOF
from soofea.model.load import ForceLoad


class IntegrationPoint(object):
    '''
    Each Element, Edge, Face (as subclass of Type)
    gets its own soofea.model.IntegrationPoint
    '''

    def __init__(self, math_ip, coordinates):
        self.math_ip = math_ip
        self._coordinates = coordinates
        self.surface_load = None
        self.volume_load = None

    def setSurfaceLoad(self, surface_load):
        self.surface_load = surface_load(*tuple(self._coordinates.reshape(1, -1)[0]))

    def setVolumeLoad(self, volume_load):
        self.volume_load = volume_load(*tuple(self._coordinates.reshape(1, -1)[0]))

    def getWeight(self):
        return self.math_ip.weight

    def getNaturalCoordinates(self):
        return self.math_ip.natural_coordinates


class Node(NumberedObject):
    '''
    We defined the points, where the interpolation conditions are fulfilled,
    as nodes. The node was the start point for doing the finite element
    discretization. This means, a node holds at least the nodal displacement
    values which are used for interpolation. This leads to the definition of
    degrees of freedom :py:class:`soofea.model.dof.DOF` and
    :py:class:`soofea.model.load.Load`.
    '''

    def __init__(self, number, coordinates):
        NumberedObject.__init__(self, number)
        self.coordinates = coordinates
        self.spatial_coordinates = coordinates
        self.dof = DisplacementDOF(len(self.coordinates))
        '''The degrees of freedom: For classical structural analysis this
            would be of type :py:class:`soofea.model.dof.DisplacementDOF`.
            We therefore connect this attribute with a displacement dof.'''
        self.load = ForceLoad(len(self.coordinates))
        '''The load: For classical structural analysis this would be of
            type :py:class:`soofea.model.load.ForceLoad`.
            We therefore connect this attribute with a force load.'''

    def __str__(self):
        print_str = 'Node ' + str(self.number) + ' @ ' + str(self.coordinates) + '\n'
        return (print_str)

    def getDimension(self):
        '''
        Can be used to easily get the dimension of the global coordinate system.
        It simply returns the amount of material coordinates for this node.
        '''
        return (len(self.coordinates))

    def setBCDOF(self, x=None, y=None, z=None):
        '''
        This method allows the definition of Dirichlet boundary conditions
        for a given node.

        :param x: The prescribed displacement in x direction
        :param y: The prescribed displacement in y direction
        :param z: The prescribed displacement in z direction
        '''
        if x != None:
            self.dof.setConstraintValue(0, x)
        if y != None:
            self.dof.setConstraintValue(1, y)
        if z != None:
            self.dof.setConstraintValue(2, z)

    def setBCLoad(self, x=None, y=None, z=None):
        '''
        This method allows the definition of Neumann boundary conditions
        for a given node.

        :param x: The prescribed force load in x direction
        :param y: The prescribed force load in y direction
        :param z: The prescribed force load in z direction
        '''
        if x != None:
            self.load.setValue(0, x)
        if y != None:
            self.load.setValue(1, y)
        if z != None:
            self.load.setValue(2, z)


class NodeContainer(NumberedObject):
    '''
    An :py:class:`soofea.model.model.Element`,
    :py:class:`soofea.model.model.Edge` or
    :py:class:`soofea.model.model.Face` is a collection (a
    geometrical patch) gathering a certain connected amount of nodes. As
    these classes have similar properties and interfaces they are derived
    from this base class.

    The :py:class:`soofea.model.model.NodeContainer` class holds an appropriate
    :py:class:`soofea.model.type.Type` and
    therefore, holds the :py:class:`soofea.model.shape.Shape` and the
    implementation :py:class:`soofea.analyzer.impl.Impl`. In addition an
    :py:class:`soofea.model.model.Element` also contains a
    :py:class:`soofea.model.material.Material` object which is needed to
    calculate the elasticity matrix.
    '''

    def __init__(self, number, node_number_list):
        NumberedObject.__init__(self, number)
        self.node_number_list = node_number_list
        '''The list of node numbers.  This is redundant as we also store
        :py:attr:`node_list`. But the problem is, that at the moment of
        construction (during reading the input file) the node references do not
        exist. Therefore we first provide the node number list and then resolve
        this list to real node references in
        :py:meth:`soofea.model.model.Model.resolveNodes()`'''
        self.node_list = []
        '''A list containing the node references.. It is important to note
        that the nodes inside the :py:attr:`node_list` are sorted regarding
        their local node numbers.'''
        self.type = None
        '''Containing the :py:class:`soofea.model.type.Type` of this object'''
        self.int_points = []
        '''Containing all the :py:class:`soofea.model.model.IntegrationPoint` of
        this object. This list is initialized by :py:meth:`setType` as soon
        as a type is assigned.'''

    def __str__(self):
        print_str = str(self.node_number_list)
        return (print_str)

    def getNode(self, local_node_number):
        '''
        :param local_node_number: The local node number for which the node should be returned
        '''
        return (self.node_list[local_node_number])

    def setType(self, the_type):
        '''
        This method not only sets the type but also initiates the list of all
        :py:class:`soofea.model.model.IntegrationPoint`. This is done by
        iterating of the mathematical integration points
        (:py:class:`soofea.numeric.num_int.IntegrationPoint`) inside
        the :py:class:`soofea.model.type.Type`.

        :param the_type: The actual :py:class:`soofea.model.type.Type` of this object.
        '''
        self.type = the_type
        math_ips = the_type.getMathIntegrationPoints()
        for math_ip in math_ips:
            X = self.getCoordinateArray()
            H = self.type.shape.getArray(math_ip.natural_coordinates)
            coord = np.dot(X, H)
            self.int_points.append(IntegrationPoint(math_ip, coord))

    def getNumberOfNodes(self):
        return len(self.node_list)

    def getCoordinateArray(self, configuration='undeformed'):
        N = self.getNumberOfNodes()
        columns = [None] * N
        if(configuration == 'undeformed'):
            for node_number in range(N):
                columns[node_number] = self.node_list[node_number].coordinates
        elif(configuration == 'spatial'):
            for node_number in range(N):
                columns[node_number] = self.node_list[node_number].spatial_coordinates
        return np.array(columns).T


class BoundaryComponent(NodeContainer):
    def __init__(self, number, node_number_list):
        NodeContainer.__init__(self, number, node_number_list)


class Edge(BoundaryComponent):
    def __init__(self, number, node_number_list):
        BoundaryComponent.__init__(self, number, node_number_list)

    def __str__(self):
        print_str = 'Edge ' + str(self.number) + ' ' + NodeContainer.__str__(self) + '\n'
        return (print_str)


class Face(BoundaryComponent):
    def __init__(self, number, node_number_list):
        BoundaryComponent.__init__(self, number, node_number_list)

    def __str__(self):
        print_str = 'Face ' + str(self.number) + ' ' + NodeContainer.__str__(self) + '\n'
        return (print_str)


class Element(NodeContainer):
    def __init__(self, number, node_number_list):
        NodeContainer.__init__(self, number, node_number_list)
        self.material = None
        '''A structural element needs a
        :py:class:`soofea.model.material.Material` to provide the data for
        calculation of the element stiffness.'''

    def __str__(self):
        print_str = 'Element ' + str(self.number) + ' ' + NodeContainer.__str__(self) + '\n'
        return (print_str)


class Boundary(NodeContainer):
    def __init__(self, N):
        NodeContainer.__init__(self, N, [])  # The node number list is empty at this point
        self.component_list = []
        '''This list contains all boundary components. This might be
        :py:class:`soofea.model.model.Edge` for the 2D case or
        :py:class:`soofea.model.model.Face` for the 3D case.'''

    def addComponent(self, component):
        '''
        As this class is bases :py:class:`soofea.model.model.NodeContainer`
        we have to append the nodes of the new component to the
        :py:attr:`soofea.model.model.NodeContainer.node_number_list`
        and the :py:attr:`soofea.model.model.NodeContainer.node_list`.

        :param component: The component (:py:class:`soofea.model.model.Edge` - 2D, :py:class:`soofea.model.model.Face` - 3D)
	to add to the boundary
        '''
        self.component_list.append(component)
        for node in component.node_list:
            if node.number not in self.node_number_list:
                self.node_number_list.append(node.number)
                self.node_list.append(node)

    def __str__(self):
        print_str = 'Boundary ' + str(self.number) + \
                    ' ( Nodes ' + str(self.node_number_list) + ' )\n'
        return (print_str)


class Model:
    def __init__(self, dimension):
        self.dimension = dimension
        self.bc_handler = None
        self._node_dict = {}
        self._edge_dict = {}
        self._face_dict = {}
        self._element_dict = {}
        self._type_dict = {}
        self._material_dict = {}
        self._boundary_dict = {}

    def addBCHandler(self, bc_handler):
        self.bc_handler = bc_handler
        self.bc_handler.setModel(self)

    def resolveNodes(self, node_number_list):
        '''
        This method takes a list of node numbers and returns a list of
        references in the same order to the corresponding node objects.

        :param node_number_list: The node numbers which should be resolved
        '''
        node_list = []
        for node_number in node_number_list:
            node_list.append(self._node_dict[node_number])
        return (node_list)

    def addNode(self, node):
        self._node_dict[node.number] = node

    def getNode(self, number):
        return (self._node_dict[number])

    def getNumberOfNodes(self):
        return (len(self._node_dict))

    def addEdge(self, edge):
        self._edge_dict[edge.number] = edge
        edge.node_list = self.resolveNodes(edge.node_number_list)
        if 2 in self._type_dict.keys():
            edge.setType(self._type_dict[2])  # We set the edge type to be 2!

    def addFace(self, face):
        self._face_dict[face.number] = face
        face.node_list = self.resolveNodes(face.node_number_list)
        if 3 in self._type_dict.keys():
            face.setType(self._type_dict[3])  # We set the face type to be 3!

    def addElement(self, element):
        self._element_dict[element.number] = element
        element.node_list = self.resolveNodes(element.node_number_list)
        if 1 in self._type_dict.keys():
            element.setType(self._type_dict[1])  # We set the element type to be 1!
        if 1 in self._material_dict.keys():
            element.material = self._material_dict[1]  # We set the material type to be 1!

    def addType(self, new_type):
        self._type_dict[new_type.number] = new_type

    def getType(self, number):
        return (self._type_dict[number])

    def addMaterial(self, material):
        print(f"{material}")
        self._material_dict[material.number] = material

    def getNumberOfUnknowns(self):
        number_of_unknowns = self.dimension * len(self._node_dict)
        return number_of_unknowns

    def appendComponentToBoundary(self, N, component_N, component_type):
        if not N in self._boundary_dict:
            self._boundary_dict[N] = Boundary(N)
        if (component_type == 'edge'):
            self._boundary_dict[N].addComponent(self._edge_dict[component_N])
        elif (component_type == 'face'):
            self._boundary_dict[N].addComponent(self._face_dict[component_N])

    def getBoundary(self, N):
        return (self._boundary_dict[N])

    def __str__(self):
        print_str = ''
        for node in self._node_dict.values():
            print_str += str(node)

        for edge in self._edge_dict.values():
            print_str += str(edge)

        for boundary in self._boundary_dict.values():
            print_str += str(boundary)

        for element in self._element_dict.values():
            print_str += str(element)
        return print_str
