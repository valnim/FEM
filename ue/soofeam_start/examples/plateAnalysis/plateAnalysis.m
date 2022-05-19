function [mymodel,analysis] = plateAnalysis

% The Matlab variable mfilename contains the name of the current file.
example_name = mfilename;
dimension = 2;
   
mesh_file_name = ['examples/',example_name,'/',example_name,'.msh'];
output_file_name = ['examples/',example_name,'/results/',example_name];
input_handler = nsIO.GmshInputHandler(mesh_file_name, dimension);
output_handler = nsIO.VTKOutputHandler(output_file_name);

% Create empty model
mymodel = nsModel.Model( dimension );

% Create Element Type and append it to the model
% Constructor of nsModel.nsType.Type: self = Type(shape_order, shape_type, number_of_int_points)
element_type = nsModel.nsType.Type(1, 'quad', 2);
mymodel.setElementType(element_type);
mymodel.element_type.setImplementation(nsAnalyzer.nsImplementation.LinearElementImpl());

% Create Face Type and append it to the model
% Constructor of nsModel.nsType.Type: self = Type(shape_order, shape_type, number_of_int_points)
face_type = nsModel.nsType.Type(1, 'linear', 2);
mymodel.setBoundaryType(face_type);
mymodel.boundary_type.setImplementation(nsAnalyzer.nsImplementation.BoundaryImpl());

% Create a Material and append it to the model.
% Constructor of nsModel.nsMaterial.StVenantKichhoffMaterial:
%   self = StVenantKichhoffMaterial(E, nu, twodim_type)
material = nsModel.nsMaterial.LinearStVenantKirchhoffMaterial(2.1e5,0.3,'plane_strain');
mymodel.setMaterial(material);

% The model is read from the gmsh file. In this process the type and
% material objects are assigned to the elements.
input_handler.read( mymodel )

% The BC handler (in which the boundary conditions are defined) is assigned
% to the model.
bc_handler = MyBCHandler(mymodel);
mymodel.setBCHandler( bc_handler );

% The analysis object is created.
analysis = nsAnalyzer.nsAnalysis.LinearAnalysis(mymodel, output_handler);

end