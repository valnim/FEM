classdef NonlinearAnalysis < nsAnalyzer.nsAnalysis.Analysis
    %NEWTONRAPHSONANALYSIS implements the nonlinear solver.
    
    properties ( SetAccess = private )
        convergence_criteria
        max_iterations
    end
    
    methods
        function self = NonlinearAnalysis( model, output_handler, convergence_criteria, max_iterations )
            self@nsAnalyzer.nsAnalysis.Analysis(model, output_handler);
            self.convergence_criteria = convergence_criteria;
            self.max_iterations = max_iterations;
        end
        
        function run(self)
            % This method is called from the main script 'soofeam.m' and
            % runs the nonlinear FE-analysis.
            
            % Export the undeformed state in the vtk format here. Use a
            % public method of self.output_handler. You can have a peek at
            % the method LinearAnalyis.run if you are unsure.
            
            
            disp('-> Newton-Raphson Analysis')
                      
            % This loops over all time steps. The first entry is the
            % undeformed step and is skipped.
            for time_stamp = self.model.time_bar(2:end)
                % Information about the current time step is displayed in
                % the command window. For very long/large simulations, this
                % output is written into a log file instead or
                % additionally.
                fprintf('\n\ntime step #%d; t = %f\n  nwtn_stp\tnormed inc\t\tnormed res\n  ------------------------------------------', time_stamp.index, time_stamp.time);
                
                % Remove all boundary conditions of the previous time step
                % from the model.
                % Use a method of self.model.bc_handler.
                
                
                % Incorporate the boundary conditions of the current time
                % step into the model.
                % Use a method of self.model.bc_handler.
                
                
                % Here, the Newton iteration starts
                for iteration_counter = 1:self.max_iterations
                    % Here, the linear equation system resulting from the
                    % linearization is calculated and solved. This works
                    % the same way as in the linear analysis.
                    % Use a method of this object (self).
                    % [increment, residuum] = 
                    

                    if iteration_counter == 1
                        % In the first Newton-Raphson step, the prescribed
                        % Dirichlet boundary conditions are set to zero,
                        % because they are already fulfilled exactly. Do
                        % this here. Use a method of self.model.bc_handler.
                        
                        
                        % In the first Newton-Raphson step, increment and
                        % residuum and stored as reference values. When
                        % checking convergence we use this values for
                        % normalization.
                        reference_inc = increment;
                        reference_res = residuum;
                    end                       
                    
                    % Information about the progress of the Newton-Raphson
                    % iteration is displayed in the command window. For
                    % very long/large simulations, this output is written
                    % into a log file instead or additionally.
                    normed_inc = norm(increment)/norm(reference_inc);
                    normed_res = norm(residuum)/norm(reference_res);
                    fprintf('\n  %d\t\t\t%e\t%e',iteration_counter, normed_inc, normed_res);
              
                    % Check the values of normed_inc and normed_res for
                    % convergence. Use the convergence criterion
                    % self.convergence_criteria for residuum and increment.
                    % if ...
                    %     break;
                                            
                    % If the convergence criterion is not fulfilled, check
                    % if we already reached the maximum number of
                    % iterations self.max_iterations.
                    % elseif ...
                    %     error('Max Iteration amount was reached in Newton-Raphson procedure before convergence was reached')
                        
                    % end
                    
                % End of Newton-Raphson loop
                end
                
                % Export the converged state in vtk format at the end of
                % each time step. Use the same method you used for
                % exporting the undeformed state.

                
            % End of timestep loop
            end
            
        % End of method run(self)
        end
    end
    
    methods ( Access = protected )
        function updateDOF(self, solution_vector)
            % This method is called once per newton step in the method
            % Analysis.solveFESystem and stores the solution vector in the
            % the model.
            
            % Note: The solution vector is structured [u1 v1 w1 u2 v2 w2
            % ... un vn wn]
            for node = self.model.node_dict
                for coord_index = 1:self.model.dimension
                    global_index = (node.number-1) * self.model.dimension + coord_index;
                    node.dof.addIncrement(coord_index, solution_vector(global_index));
                    
                    % Here the spatial coordinates of the nodes are
                    % updated.
                    node.updateCoordinates();
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
            % This method is called in the function Analysis.solveFESystem
            % and calculates the global Load vector.
            % In contrast to the linear analysis, the internal work
            % contributes to the load vector, i.e. to the residuum
            for element = self.model.element_dict
                F_int = element.type.implementation.calcLoad( element );
                global_load = self.assembleLoad(element, F_int, global_load);
            end
        end
    end
end
