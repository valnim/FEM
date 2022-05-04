// 2d Plate under tension -> benchmark: compared to deal.II and pySoofea

b = 10;
h = 10;

cl = 1;   // default mesh size at nodes -> not needed here

numel_x = 2; // number of elements in x-direction
numel_y = 2; // number of elements in y-direction

Point(1) = {0, 0, 0, cl}; // bottom left
Point(2) = {b, 0, 0, cl}; // bottom right
Point(3) = {b, h, 0, cl}; // top right
Point(4) = {0, h, 0, cl}; // top left

Line(1) = {1, 2}; // bottom
Line(2) = {2, 3}; // right
Line(3) = {3, 4}; // top
Line(4) = {4, 1}; // left

Line Loop(1) = {1, 2, 3, 4};

Plane Surface(1) = {1};

// Define transfinite lines for a structured grid
Transfinite Line{1} = numel_x+1;
Transfinite Line{-2} = numel_y+1;
Transfinite Line{3} = numel_x+1;
Transfinite Line{4} = numel_y+1;

// Define the Surface as transfinite, by specifying the four corners of the
// transfinite interpolation
Transfinite Surface{1} = {1,2,3,4};

// (Note that the list on the right hand side refers to points, not curves. When
// the surface has only 3 or 4 points on its boundary the list can be
// omitted. The way triangles are generated can be controlled by appending
// "Left", "Right" or "Alternate" after the list.)

Physical Line(1) = {1};
Physical Line(2) = {2};
Physical Line(3) = {3};
Physical Line(4) = {4};

Physical Surface("mesh") = {1};

// Recombine the triangles into quads
Recombine Surface{1};
