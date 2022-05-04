classdef DisplacementDOF < handle
    % specifies displacement DOFs
    
    properties ( SetAccess = protected )
        displacement
        increment
        constraint
    end
    
    methods
        function self = DisplacementDOF( dimension )
            % the values of the displacementDOFs are the displacements. they are stored in an 1xdim array.
            self.displacement = zeros( 1, dimension );
            
            self.increment = zeros(1, dimension);
            
            % Per default, all values of a displacement DOF are not constraint,
            % hence they are initiated as 'false'.
            self.constraint = false( 1, dimension );
        end
        
        function displacement = getDisplacement( self, coordinate_id )
            % Simple get-Function
            displacement = self.displacement( coordinate_id );
        end
         
        function increment = getIncrement( self, coordinate_id )
            increment = self.increment( coordinate_id );
        end        
        
        function setDisplacement(self, coord_id, displacement)
            % Simple set-Function
            self.displacement(coord_id) = displacement;
        end
        
        function constraint = getConstraint( self, coordinate_id )
            % Simple get-Function            
            constraint = self.constraint( coordinate_id );
        end

        function setConstraintDisplacement( self, coordinate_id, displacement )
            % When Dirichlet boundary conditions are defined, two things
            % have to be done:
            %  1.) Set the value of the displacement
            %  2.) Set the constraint-value to 'true'. This will be needed
            %  when the the boundary conditions are integrated into the
            %  linear system of equations.
            self.displacement (coordinate_id ) = displacement;
            self.constraint( coordinate_id ) = true;
        end
        
        function setConstraintIncrement( self, coordinate_id, increment )
            self.increment (coordinate_id ) = increment;
            self.constraint( coordinate_id ) = true;
        end
        
        function resetDOF(self, coordinate_id)
            self.increment(coordinate_id) = 0;
            self.constraint(coordinate_id) = false;
        end
        
        function addIncrement( self, coordinate_id, increment)
            self.displacement(coordinate_id) = self.displacement(coordinate_id) + increment;
            self.increment(coordinate_id)    = increment;
        end
    end
end