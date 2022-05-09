function [mymodel] = plateDOF

dimension = 2;
   
% The input file is defined
mesh_file_name = 'examples/plateDOF/plateDOF.msh';
input_handler = nsIO.GmshInputHandler(mesh_file_name, dimension);

% The empty model is created
mymodel = nsModel.Model( dimension );

% Ignore the following line for now
mymodel.setElementType(nsModel.nsType.Type(1, 'quad', 2)); mymodel.element_type.setImplementation(nsAnalyzer.nsImplementation.LinearElementImpl()); mymodel.setBoundaryType(nsModel.nsType.Type(1, 'linear', 2)); mymodel.boundary_type.setImplementation(nsAnalyzer.nsImplementation.BoundaryImpl()); mymodel.setMaterial(nsModel.nsMaterial.LinearStVenantKirchhoffMaterial(2.1e5,0.3,'plane_stress'));

% The model is read from the input gmsh file
input_handler.read( mymodel )

% The BC handler is created and assigned to the model.
bc_handler = MyBCHandler(mymodel);
mymodel.setBCHandler( bc_handler )

end