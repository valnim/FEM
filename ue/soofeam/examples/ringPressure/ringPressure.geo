// Circular ring with elliptic hole

a = 100;
b = 50;
R = 150;

cl = 1;   // default mesh size at nodes -> not needed here

numel_x = 10; // number of elements in x-direction
numel_y = 10; // number of elements in y-direction

Point(1) = {0, 0, 0, cl}; // center
Point(2) = {a, 0, 0, cl}; // bottom ellipse
Point(3) = {R, 0, 0, cl}; // bottom circle
Point(4) = {0, b, 0, cl}; // top ellipse
Point(5) = {0, R, 0, cl}; // top circle

Ellipse(1) = {2, 1, 2, 4};    // ellipse
Circle(2) = {3, 1, 5};    // circle
Line(3) = {2, 3}; // bottom
Line(4) = {4, 5}; // left

Line Loop(2) = {1, 4, -2, -3};

Plane Surface(1) = {2};

// Define transfinite lines for a structured grid
Transfinite Line{1} = numel_x+1;
Transfinite Line{2} = numel_y+1;
Transfinite Line{3} = numel_x+1;
Transfinite Line{4} = numel_y+1;

// Define the Surface as transfinite, by specifying the four corners of the
// transfinite interpolation
Transfinite Surface{1} = {2,3,4,5};

// (Note that the list on the right hand side refers to points, not curves. When
// the surface has only 3 or 4 points on its boundary the list can be
// omitted. The way triangles are generated can be controlled by appending
// "Left", "Right" or "Alternate" after the list.)

Physical Line(1) = {3};   // bottom symmetry
Physical Line(2) = {2};   // circle
Physical Line(3) = {4};   // left symmetry
Physical Line(4) = {1};   // ellipse

Physical Surface("mesh") = {1};

// Recombine the triangles into quads
Recombine Surface{1};
