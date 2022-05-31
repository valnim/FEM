/*********************************************************************
 *
 *  LU Kontinuumsmechanik
 *
 *  Gmsh-File of the Kirsch-Problem
 *
 *********************************************************************/

 s = 100;
 r = 20;
 cl = 1;
 n1 = 16;
 n2 = 16;


Point(1) = {0, 0, 0, cl};
Point(2) = {r, 0, 0, cl};
Point(3) = {s, 0, 0, cl};
Point(4) = {s, s, 0, cl};
Point(5) = {0, s, 0, cl};
Point(6) = {0, r, 0, cl};

Circle(1) = {6, 1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};

Line Loop(7) = {4, 1, 5, 2, 3};
Plane Surface(1) = {7};

Transfinite Line{1} = n2+1;
Transfinite Line{2} = n1+1; // Using Progression 1.05;
Transfinite Line{3} = n2/2+1;
Transfinite Line{4} = n2/2+1;
Transfinite Line{5} = n1+1; // Using Progression 0.95;

Transfinite Surface{1} = {2,3,5,6};

Physical Line(1) = {1};  // Circle
Physical Line(2) = {2};  // bottom
Physical Line(3) = {3};  // right
Physical Line(4) = {4};  // top
Physical Line(5) = {5};  // left

Physical Surface(2) = {1};

Recombine Surface{1};
Mesh.Algorithm = 8;
