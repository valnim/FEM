classdef Analysis < handle
    properties ( SetAccess = protected )
        model
        output_handler
    end
    
    methods
        function self = Analysis(model, output_handler)
            self.model = model;
            self.output_handler = output_handler;
        end
    end
    
    methods ( Access = protected )
        function [solution_vector, global_load] = solveFESystem(self)
            # At the beginning, global stiffness matrix and global load
            # vector are created empty.
            number_of_unknowns = self.model.getNumberOfUnknowns();
            
            global_load = zeros(number_of_unknowns, 1);
            global_stiffness = sparse(number_of_unknowns, number_of_unknowns);
            
            # The element stiffness matrizes are calculated and the global
            # stiffness matrix is assembled.
            global_stiffness = self.calcGlobalStiffnessMatrix(global_stiffness);
            
            # The element load vectors are calculated and the global load
            # vector is assembled.
            global_load = self.calcGlobalLoadVector(global_load);
            
            # The Dirichlet boundary conditions are integrated into the
            # linear equation system.
            [global_stiffness, global_load] = self.integrateDirichletBC(global_stiffness, global_load);
            
            # The Matlab operator '' solves the linear equations system
            # global_stiffness * solution_vector = global_load
            #
            # The solution_vector contains the nodal displacements for a
            # linear analysis and the nodal displacement increments for a
            # nonlinear analysis.
            solution_vector = global_stiffness\global_load;
            
            # The solution vector is stored in the DOF objects of the
            # model.
            self.updateDOF(solution_vector);
        end
                
        function [global_stiffness, global_load] = integrateDirichletBC(self, global_stiffness, global_load)
            for node = self.model.node_dict
                for coord_index = 1:self.model.dimension
                    if node.dof.getConstraint(coord_index)
                        # Row in the column solution vector
                        global_col_index = (node.number-1)*self.model.dimension + coord_index;
                        for row_counter=1:length(global_stiffness)
                            # Check if the analysis is linear or nonlinear.
                            # Use the displacement or the increment as
                            # boundary condition respectively.
                            if isa(self,'nsAnalyzer.nsAnalysis.LinearAnalysis')
                                bc_value = node.dof.getDisplacement(coord_index);
                            elseif isa (self,'nsAnalyzer.nsAnalysis.NonlinearAnalysis')
                                bc_value = node.dof.getIncrement(coord_index);
                            else
                                error('analysis type not found')
                            end
                            
                            if row_counter == global_col_index
                                global_load(row_counter) = global_stiffness(row_counter, row_counter)*bc_value;
                            else
                                global_load(row_counter) = global_load(row_counter) - global_stiffness(row_counter, global_col_index)*bc_value;
                            end
                        end
                        temp = global_stiffness(global_col_index, global_col_index);
                        global_stiffness(:, global_col_index) = 0;
                        global_stiffness(global_col_index,:) = 0;
                        global_stiffness(global_col_index, global_col_index) = temp;
                    end
                end
            end
        end
    end
    
    methods( Static, Access = protected )
        function global_stiffness = assembleStiffness(node_container, local_stiffness, global_stiffness)
            
            # dofs_per_node is dimension of stiffness matrix divided by
            # number of nodes per element. I have not figured out why, yet.
            # Maybe number of entries means numbers of dofs per node, so 2
            # for 2D and 3 for 3D original line: nr_of_entries =
            # local_stiffness.shape(1)/node_container.type.shape.getNumberOfNodes;
            
            dofs_per_element = length(local_stiffness);
            
            dofs_per_node = dofs_per_element/node_container.type.shape.getNumberOfNodes;
            
            for local_row_index = 1:length(local_stiffness)
                for local_col_index = 1:length(local_stiffness)
                    # In the assembly process, the task is to find the
                    # global indices of the global stiffness matrix which
                    # belong to the local indices of the local indices of
                    # the current element
                    
                    # There are dofs_per_node columns for each node.
                    # example 2D: u1,v1,u2,v2,... -> indices 1 & 2 must be
                    # mapped to 1 -> indices 3 & 4 must be mapped to 2,
                    # etc. hence the ceil.
                    local_node_index_row = ceil(local_row_index/dofs_per_node);
                    local_node_index_col = ceil(local_col_index/dofs_per_node);
                    
                    # get the current nodes
                    row_node = node_container.node_list(local_node_index_row);
                    col_node = node_container.node_list(local_node_index_col);
                    
                    # get the global node number
                    global_node_index_row = row_node.number;
                    global_node_index_col = col_node.number;
                    
                    # retrieve the position in the global stiffness matrix.
                    # example 2D: node 8 with dofs u8 & v8 must deliver
                    # global indices 7*2+1 = 15 & 7*2+2 = 16 the first
                    # summend is called start_position, the second one is
                    # called offset and can be obtained via a modulu
                    # operation.
                    row_start_position = (global_node_index_row - 1)*dofs_per_node;
                    col_start_position = (global_node_index_col - 1)*dofs_per_node;
                    
                    row_offset = mod(local_row_index,dofs_per_node);
                    col_offset = mod(local_col_index,dofs_per_node);
                    
                    
                    # at the last index of each node, the mod operator
                    # returns 0, but it should of course return
                    # dofs_per_node
                    if row_offset == 0
                        row_offset = dofs_per_node;
                    end
                    if col_offset == 0
                        col_offset = dofs_per_node;
                    end
                    
                    # so the global indices are finally obtained
                    global_row_index = row_start_position + row_offset;
                    global_col_index = col_start_position + col_offset;
                    
                    global_stiffness(global_row_index,global_col_index) = global_stiffness(global_row_index,global_col_index) + local_stiffness(local_row_index,local_col_index);
                end
            end
        end
        
        function global_load = assembleLoad(node_container, local_load, global_load)
            
            # analogous to assembleStiffness(...) method above
            dofs_per_node = length(local_load)/node_container.type.shape.getNumberOfNodes;
            for local_row_index = 1:length(local_load)
                
                local_node_index_row = ceil(local_row_index/dofs_per_node);
                row_node = node_container.node_list(local_node_index_row);
                
                global_node_index_row = row_node.number;
                
                row_start_position = (global_node_index_row - 1)*dofs_per_node;
                row_offset = mod(local_row_index,dofs_per_node);
                if row_offset == 0
                    row_offset = dofs_per_node;
                end
                global_row_index = row_start_position + row_offset;
                
                global_load(global_row_index) = global_load(global_row_index) + local_load(local_row_index);
            end
        end
    end
    
    methods ( Abstract )
        run(self)
    end
    
    methods ( Abstract, Access = protected )
        updateDOF(self, solution_vector)
        calcGlobalStiffnessMatrix(self, global_stiffness)
        calcGlobalLoadVector(self, global_load)
    end
end

