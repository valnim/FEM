% We read a 2d mesh.
dimension = 2;

% The model is created empty.
model = nsModel.Model(dimension);

% The path to the input file must be provided
mesh_file_name = 'examples/plateQuads/plateQuads.msh';

% You can ignore the following line for now
model.setElementType(nsModel.nsType.Type(1, 'quad', 2)); model.element_type.setImplementation(nsAnalyzer.nsImplementation.LinearElementImpl()); model.setBoundaryType(nsModel.nsType.Type(1, 'linear', 2)); model.boundary_type.setImplementation(nsAnalyzer.nsImplementation.BoundaryImpl()); model.setMaterial(nsModel.nsMaterial.LinearStVenantKirchhoffMaterial(2.1e5,0.3,'plane_stress'));

% An input handler is created. The constructor needs the name of the input
% file and the dimension of the problem as input parameters.
input_handler = nsIO.GmshInputHandler(mesh_file_name, dimension);

% The input handler reads the mesh information from the file and stores
% them in the model.
fprintf('Creating Model ...\n')
input_handler.read( model )

% The properties of the model can be displayed in the command window.
disp(model);


%---- Exercise 1 ----%

% Enter the commands of Exercise 1 here:
