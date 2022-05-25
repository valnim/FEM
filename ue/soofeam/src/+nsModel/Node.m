classdef Node < nsModel.NumberedObject
    %NODE Node of the finite element grid
    
    properties ( SetAccess = private )
        % needed for a nonlinear formulation.
        % still there for the linear one.
        undeformed_coordinates
        spatial_coordinates
        
        % formulation-independent properties
        dimension
        dof
    end
    
    methods
        % A node gets created only with its material coordinates, at the
        % initial state t=0.
        function self = Node( number, coordinates )
            self@nsModel.NumberedObject(number);
            self.undeformed_coordinates = coordinates;
            self.spatial_coordinates = coordinates;
            self.dimension = length(coordinates);
            
            self.dof = nsModel.nsDOF.DisplacementDOF(self.dimension);
        end
        
        function setBCDisplacement( self, coord_flag, displacement )
            % Call this method in the BCHandler of a linear analysis, where
            % absolute displacements are Dirichlet boundary conditions.
            % Pass a coordinate flag ('x', 'y' or 'z') to decide in which
            % coordinate direction the displacement is constrained.
            switch coord_flag
                case 'x'
                    self.dof.setConstraintDisplacement( 1, displacement );
                case 'y'
                    assert(self.dimension>1,'Prescribe y-value only if dimension of problem is > 1!');
                    self.dof.setConstraintDisplacement( 2, displacement );
                case 'z'
                    assert(self.dimension>2,'Prescribe z-value only if dimension of problem is > 2!');
                    self.dof.setConstraintDisplacement( 3, displacement );
            end
        end 
    end
end

