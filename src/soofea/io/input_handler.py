""" ------------------------------------------------------------------
This file is part of SOOFEA Python.

SOOFEA - Software for Object Oriented Finite Element Analysis
Copyright (C) 2012 Michael Hammer

SOOFEA is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
------------------------------------------------------------------ """

import os
from soofea.model import Node, Element, Edge, Face
from abc import ABCMeta, abstractmethod


class InputHandler:
    __metaclass__ = ABCMeta

    def __init__(self, file_name, dimension):
        self._file_name = file_name
        self._dimension = dimension
        if not os.path.exists(file_name):
            raise Exception('Input file could not be found')
        self._input_file = open(file_name, 'r')

    @abstractmethod
    def _read(self, model):
        pass

    def readMesh(self, model):
        self._read(model)

    def __del__(self):
        self._input_file.close()


class GmshInputHandler(InputHandler):
    element_types = {1: '2-node_line',
                     2: '3-node_triangle',
                     3: '4-node_quadrangle',
                     4: '4-node_tetrahedron',
                     5: '8-node_hexahedron',
                     15: '1-node_point'}

    def __init__(self, file_name, dimension):
        InputHandler.__init__(self, file_name, dimension)
        self._meshes = {}
        self.number_of_elements = 0
        self.number_of_nodes = 0

    def _elementContainerState(self, line_data, old_state):
        state = None
        if (self.element_types[int(line_data[1])] == '1-node_point'):
            state = 'points'
        elif self.element_types[int(line_data[1])] == '3-node_triangle':
            if self._dimension == 2:
                state = 'elements'
            else:
                state = 'faces'
        elif (self.element_types[int(line_data[1])] == '2-node_line'):
            state = 'edges'
        elif (self.element_types[int(line_data[1])] == '4-node_quadrangle'):
            if self._dimension == 2:
                state = 'elements'
            else:
                state = 'faces'
        elif (self.element_types[int(line_data[1])] == '8-node_hexahedron'):
            state = 'elements'
        elif not state:
            raise BaseException('We do not know element type : ' + line_data[1])
        if (state != old_state):
            print(f"--> We are on new state {state}")
        return (state)

    def _read(self, model):
        print("-> Parsing GMSH input file")
        state = 'foo'
        boundary_ids = []

        for line in self._input_file:
            if (state == 'foo'):
                if (line.rstrip(' \r\n') == '$PhysicalNames'):
                    state = 'physical'
                    print("--> Reading physical names...")
                    continue

                if (line.rstrip(' \r\n') == '$Nodes'):
                    state = 'nodes'
                    print("--> Reading nodes...")
                    continue

                if (line.rstrip(' \r\n') == '$Elements'):
                    state = 'elements_container'
                    print("--> Reading element container...")
                    continue

            # Physical groups------------------------------------------------------------
            if (state == 'physical'):
                if (line.rstrip(' \r\n') == '$EndPhysicalNames'):
                    state = 'foo'
                    continue

                line_data = line.split()
                if len(line_data) == 1:
                    continue

                mesh_name = line_data[2].strip('" ')
                if mesh_name in self._meshes:
                    self._meshes[mesh_name].append(int(line_data[1]))
                else:
                    self._meshes[mesh_name] = [int(line_data[1])]

            # Nodes ------------------------------------------------------------------
            if (state == 'nodes'):
                if (line.rstrip(' \r\n') == '$EndNodes'):
                    state = 'foo'
                    continue

                node_data = line.split()
                if len(node_data) == 1:
                    # We are on first line
                    self.number_of_nodes = node_data[0]
                    continue

                if (self._dimension == 2):
                    model.addNode(Node(int(node_data[0]), [float(node_data[1]), float(node_data[2])]))
                else:
                    model.addNode(
                        Node(int(node_data[0]), [float(node_data[1]), float(node_data[2]), float(node_data[3])]))

            # Element Container------------------------------------------------------------
            if (
                    state == 'elements_container' or state == 'elements' or state == 'faces' or state == 'edges' or state == 'points'):
                if (line.rstrip(' \r\n') == '$EndElements'):
                    print("--> Leaving Element Container")
                    state = 'foo'
                    continue

                line_data = line.split()

                if len(line_data) == 1:
                    # We are hopefully on first line
                    self.number_of_elements = line_data[0]
                    continue

                state = self._elementContainerState(line_data, state)

                # Points----------------------------------------------------------------
                if (state == 'points'):
                    pass

                # Edges------------------------------------------------------------
                if (state == 'edges'):
                    nr_of_tags = int(line_data[2])
                    if (nr_of_tags < 2):
                        raise Exception("BaseException('We need the id of the line were the edge lies on')")

                    model.addEdge(Edge(int(line_data[0]), [int(node_num) for node_num in line_data[(3 + nr_of_tags):]]))

                    boundary_id = line_data[4]
                    if not boundary_id in boundary_ids:
                        boundary_ids.append(boundary_id)
                    model.appendComponentToBoundary(int(boundary_id), int(line_data[0]), 'edge')
                    continue

                # Faces------------------------------------------------------------
                if (state == 'faces'):
                    nr_of_tags = int(line_data[2])
                    if (nr_of_tags < 2):
                        raise Exception("BaseException('We need the id of the surface were the face lies on')")

                    model.addFace(Face(int(line_data[0]), [int(node_num) for node_num in line_data[(3 + nr_of_tags):]]))

                    boundary_id = line_data[4]
                    if not boundary_id in boundary_ids:
                        boundary_ids.append(boundary_id)
                    model.appendComponentToBoundary(int(boundary_id), int(line_data[0]), 'face')
                    continue

                # Elements--------------------------------------------------------------
                if (state == 'elements'):
                    nr_of_tags = int(line_data[2])

                    model.addElement(
                        Element(int(line_data[0]), [int(node_num) for node_num in line_data[(3 + nr_of_tags):]]))
