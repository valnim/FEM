/*********************************************************************
 *
 *  2D-plate
 *
 *********************************************************************/

x = 100;
y = 1;

el_per_side_x = 200; // number of elements per side
el_per_side_y = 2; // number of elements per side

Point(1) = {0, 0, 0, 1};   // bottom left corner
Point(2) = {x, 0, 0, 1};   // bottom right corner
Point(3) = {x, y, 0, 1};   // top right corner
Point(4) = {0, y, 0, 1};   // top left corner

Line(1) = {1, 2};            // bottom side
Line(2) = {2, 3};            // right side
Line(3) = {3, 4};            // top side
Line(4) = {4, 1};            // left side

Line Loop(5) = {1, 2, 3, 4};

Plane Surface(6) = {5};

// See http://gmsh.info/doc/texinfo/gmsh.html#t6_002egeo for the usage of transfinite meshes
Transfinite Line{1} = el_per_side_x+1;
Transfinite Line{2} = el_per_side_y+1;
Transfinite Line{3} = el_per_side_x+1;
Transfinite Line{4} = el_per_side_y+1;

Transfinite Surface{6} = {1,2,3,4};


Physical Line(1) = {1};
Physical Line(2) = {2};
Physical Line(3) = {3};
Physical Line(4) = {4};

Physical Surface(1) = {6};

// Recombine the triangles into quads
Recombine Surface{6};
