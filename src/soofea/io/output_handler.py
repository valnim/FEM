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

import os, sys
import vtk
from vtk.util.colors import lamp_black


class OutputHandler:
    def __init__(self, file_name, dimension, force_overwrite):
        self._file_name = file_name
        self._dimension = dimension
        self._force_overwrite = force_overwrite


class VTKOutputHandler(OutputHandler):
    def __init__(self, file_name, dimension, force_overwrite=False):
        OutputHandler.__init__(self, file_name, dimension, force_overwrite)

    def createVTKMesh(self, model):
        mesh = vtk.vtkUnstructuredGrid()

        # Add nodes
        node_list = vtk.vtkPoints()
        xyz = []
        for node in model._node_dict.values():
            if (model.dimension == 2):
                xyz = [node.coordinates[0], node.coordinates[1], 0]
            else:
                xyz = node.coordinates
            node_list.InsertPoint(node.number, xyz)
        mesh.SetPoints(node_list)

        # Add elements
        for element in model._element_dict.values():
            if (element.type.shape.__class__.__name__ == 'QuadShape'):
                new_cell = vtk.vtkQuad()
            if (element.type.shape.__class__.__name__ == 'TriShape'):
                new_cell = vtk.vtkTriangle()
            if (element.type.shape.__class__.__name__ == 'HexShape'):
                new_cell = vtk.vtkHexahedron()
            for node_counter in range(len(element.node_list)):
                new_cell.GetPointIds().InsertId(node_counter, element.node_list[node_counter].number)
            mesh.InsertNextCell(new_cell.GetCellType(), new_cell.GetPointIds())

        # Add displacement
        disp_array = vtk.vtkDoubleArray()
        disp_array.SetNumberOfComponents(3)
        disp_array.SetName("displacement")
        for node in model._node_dict.values():
            if (model.dimension == 2):
                disp_array.InsertTuple3(node.number, \
                                        node.dof.getDisplacement(0), \
                                        node.dof.getDisplacement(1), \
                                        0)
            else:
                disp_array.InsertTuple3(node.number, \
                                        node.dof.getDisplacement(0), \
                                        node.dof.getDisplacement(1), \
                                        node.dof.getDisplacement(2))
        mesh.GetPointData().SetVectors(disp_array)

        #        # Add strain
        #        if hasattr(model.getNode(1),'strain'):
        #            strain_array = vtk.vtkDoubleArray()
        #            strain_array.SetNumberOfComponents(9)
        #            strain_array.SetName("strain")
        #            for node in model._node_dict.values():
        #                if( model.dimension == 2 ):
        #                    strain_array.InsertTuple9( node.number,
        #                                               node.strain[0,0], node.strain[0,1], 0,\
        #                                               node.strain[1,0], node.strain[1,1], 0,\
        #                                               0             , 0             , 0 )
        #                else:
        #                    strain_array.InsertTuple9( node.number, \
        #                                               node.strain[0,0], node.strain[0,1], node.strain[0,2],\
        #                                               node.strain[1,0], node.strain[1,1], node.strain[1,2],\
        #                                               node.strain[2,0], node.strain[2,1], node.strain[2,2] )
        #            mesh.GetPointData().SetActiveTensors("strain")
        #            mesh.GetPointData().SetTensors(strain_array)

        #        # Add stress
        #        if hasattr(model.getNode(1),'stress'):
        #            stress_array = vtk.vtkDoubleArray()
        #            stress_array.SetNumberOfComponents(9)
        #            stress_array.SetName("stress")
        #            for node in model._node_dict.values():
        #                if( model.dimension == 2 ):
        #                    stress_array.InsertTuple9( node.number,
        #                                               node.stress[0,0], node.stress[0,1], 0,\
        #                                               node.stress[1,0], node.stress[1,1], 0,\
        #                                               0             , 0             , 0 )
        #                else:
        #                    stress_array.InsertTuple9( node.number, \
        #                                               node.stress[0,0], node.stress[0,1], node.stress[0,2],\
        #                                               node.stress[1,0], node.stress[1,1], node.stress[1,2],\
        #                                               node.stress[2,0], node.stress[2,1], node.stress[2,2] )
        #            mesh.GetPointData().SetActiveTensors("stress")
        #            mesh.GetPointData().SetTensors(stress_array)

        return (mesh)

    def write(self, model):
        file_name = self._file_name
        if hasattr(model, 'last_finished_time_step'): file_name += "." + str(model.last_finished_time_step)

        overwrite = False
        if not self._force_overwrite:
            if os.path.exists(file_name):
                str_in = input('Output file does exist! Should it be overwritten? (Y/n): ')
                if (str_in == ''):
                    overwrite = True
                if (str_in == 'Y') or (str_in == 'y'):
                    overwrite = True
            else:
                overwrite = True
        else:
            overwrite = True
        if not overwrite:
            print('You choose not to overwrite the output file ...')
            sys.exit(-1)

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(file_name)
        mesh = self.createVTKMesh(model)
        writer.SetInputData(mesh)
        writer.Write()

    def vis(self, model):
        mesh = self.createVTKMesh(model)

        geom_filter = vtk.vtkGeometryFilter()
        geom_filter.SetInput(mesh)

        element_mapper = vtk.vtkPolyDataMapper()
        element_mapper.SetInput(geom_filter.GetOutput())
        element_mapper.ScalarVisibilityOff()

        edge_filter = vtk.vtkExtractEdges()
        edge_filter.SetInput(geom_filter.GetOutput())
        edge_mapper = vtk.vtkPolyDataMapper()
        edge_mapper.SetInput(edge_filter.GetOutput())
        edge_mapper.ScalarVisibilityOff()

        element_actor = vtk.vtkActor()
        element_actor.SetMapper(element_mapper)
        element_actor.GetProperty().SetColor(0.91, 0.87, 0.67)
        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.GetProperty().SetColor(0, 0, 0)
        edge_actor.GetProperty().SetDiffuseColor(lamp_black)

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(element_actor)
        renderer.AddActor(edge_actor)
        renderer.SetBackground(.5, .6, .7)

        renderer.GetActiveCamera().SetParallelProjection(True)
        renderWindow.Render()
        renderWindowInteractor.Start()
