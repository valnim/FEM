/*********************************************************************
 *
 *  cuboid
 *
 *********************************************************************/

// geometric values
lx = 200;   			// cuboid length/2 x -> symmetry
ly = 200;   			// cuboid length/2 y -> symmetry
lz = 100;   			// cuboid length z

el_per_side = 6; 		// number of elements per side
cl = 1;

Point(1) = {0, 0, 0, cl};   	// bottom back left corner
Point(2) = {lx, 0, 0, cl};   	// bottom front left corner
Point(3) = {lx, ly, 0, cl};   	// bottom front right corner
Point(4) = {0, ly, 0, cl};   	// bottom back right corner
Point(5) = {0, 0, lz, cl};   	// top back left corner
Point(6) = {lx, 0, lz, cl};   	// top front left corner
Point(7) = {lx, ly, lz, cl};   	// top front right corner
Point(8) = {0, ly, lz, cl};   	// top back right corner

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 5};
Line(9) = {1, 5};
Line(10) = {2, 6};
Line(11) = {3, 7};
Line(12) = {4, 8};

Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Line Loop(2) = {5, 6, 7, 8};
Plane Surface(2) = {2};
Line Loop(3) = {1, 10, -5, -9};
Plane Surface(3) = {3};
Line Loop(4) = {3, 12, -7, -11};
Plane Surface(4) = {4};
Line Loop(5) = {4, 9, -8, -12};
Plane Surface(5) = {5};
Line Loop(6) = {2, 11, -6, -10};
Plane Surface(6) = {6};

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};

// Transfinite Mesh
Transfinite Line{1,2,3,4,5,6,7,8,9,10,11,12} = el_per_side+1;

Transfinite Surface{1} = {1,2,3,4};
Transfinite Surface{2} = {5,6,7,8};
Transfinite Surface{3} = {1,5,6,2};
Transfinite Surface{4} = {3,7,4,8};
Transfinite Surface{5} = {1,5,8,4};
Transfinite Surface{6} = {2,6,7,3};

Recombine Surface{1,2,3,4,5,6};

Transfinite Volume{1} = {1, 2, 3, 4,5, 6, 7, 8};

// Physical groups
Physical Surface(1) = {1};	// bottom
Physical Surface(2) = {2};	// top
Physical Surface(3) = {3, 5};	// 'outer' surface
Physical Surface(4) = {6};	// yz-symmetry plane
Physical Surface(5) = {4};	// xz-symmetry plane

Physical Volume(1) = {1};