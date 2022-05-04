% The type is created: A bilinear (shape_order=1) quad element with 2
% integration points per coordinate direction
shape_order = 1;
shape_type = 'quad';
num_int_points = 2;

element_type = nsModel.nsType.Type(shape_order, shape_type, num_int_points);

% A quad element with node coordinates (1/2), (4/1), (4/5) and (1/3) is
% created manually. Later we will not create nodes and elements by hand,
% but will read the geometry of the mesh from an input file.
node_numbers = [1 2 3 4];
node_coordinates = [[1 2];[4 1];[4 5];[1 3]];

n = length(node_numbers);
node_list = nsModel.Node.empty;
for i=1:n
    node_list(i) = nsModel.Node(node_numbers(i), node_coordinates(i,:));
end

element_number = 1;
element = nsModel.Element(element_number,node_list);

% We now connect the geometric element with the type (i.e. with shape
% functions and integration points/numerical integration).spunkten)
element.setType(element_type);
disp(element)


%---- Exercise 4 ----%

% Have a look at the method nsModel.NodeContainer.setType - in addition to
% assigning the type to the element, it creates the integration points on
% the real element.

% Write a loop which loops over the RealIntegrationPoints of the element
% and display their coordinates.
