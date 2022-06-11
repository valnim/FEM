/*********************************************************************
 *
 *  cuboid
 *
 *********************************************************************/

// geometric values
lx = 1;   			// cuboid length/2 x -> symmetry
ly = 1;   			// cuboid length/2 y -> symmetry
lz = 5;   			// cuboid length z

el_x = 2; 		// number of elements per side
el_y = 2;
el_z = 10;
cl = 1;

Point(1) = {-lx/2, -ly/2, 0, cl};   	// bottom back left corner
Point(2) = { lx/2, -ly/2, 0, cl};   	// bottom front left corner
Point(3) = { lx/2,  ly/2, 0, cl};   	// bottom front right corner
Point(4) = {-lx/2,  ly/2, 0, cl};   	// bottom back right corner


Line(1) = {1, 2};            // bottom side
Line(2) = {2, 3};            // right side
Line(3) = {3, 4};            // top side
Line(4) = {4, 1};            // left side

Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

Physical Surface(1) = {1};
// See http://gmsh.info/doc/texinfo/gmsh.html#t6_002egeo for the usage of transfinite meshes
Transfinite Line{1} = el_x+1;
Transfinite Line{2} = el_y+1;
Transfinite Line{3} = el_x+1;
Transfinite Line{4} = el_y+1;

Transfinite Surface{1};
Recombine Surface{1};

ext[] = Extrude {0, 0, lz} {
  Surface{1}; Layers{el_z}; Recombine;
};

Physical Surface(2) = {ext[0]};
Physical Surface(3) = {ext[1]};
Physical Surface(4) = {ext[2]};
Physical Surface(5) = {ext[3]};
Physical Surface(6) = {ext[4]};
Physical Volume(1) = {ext[1]};
