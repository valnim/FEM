classdef LinearAnalysis < nsAnalyzer.nsAnalysis.Analysis

    methods
        function self = LinearAnalysis(model, output_handler)
            self@nsAnalyzer.nsAnalysis.Analysis(model, output_handler);
        end
        
        function run(self)
            % The undeformed state at t=0 is exported in the vtk format.
            self.output_handler.write(self.model);
            
            disp('-> Linear Analysis')
            
            % The Dirichlet boundary conditions (=displacement boundary
            % conditions) are written into the DOF objects of each node.
            self.model.bc_handler.incorporateBC();
            
            % The linear equation system is created and solved.
            self.solveFESystem();
                        
            % The solution is exported in the vtk format.
            self.output_handler.write(self.model);
        end
    end
    
    methods (Access = protected)      
        function updateDOF(self, solution_vector)
            for node = self.model.node_dict
                for coord_index = 1:self.model.dimension
                    global_index = (node.number-1) * self.model.dimension + coord_index;
                    node.dof.setDisplacement(coord_index, solution_vector(global_index));
                end
            end
        end

        function global_stiffness = calcGlobalStiffnessMatrix(self, global_stiffness)          
            for element = self.model.element_dict
                % The element stiffness matrix is created...
                K_elem = element.type.implementation.calcStiffness(element);
                
                % ... and assembled into the global stiffness matrix. We
                % will not discuss how the function assembleStiffness works
                % in this lecture.
                global_stiffness = self.assembleStiffness(element, K_elem, global_stiffness);
            end
        end            
        
        function global_load = calcGlobalLoadVector(self, global_load)          
            % In the linear analysis, the load vector contains body forces
            % and volume forces. We do not discuss them in this lecture,
            % therefore this function is empty.
        end
    end
end

