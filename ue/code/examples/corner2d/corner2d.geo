// Geometrieparameter
l = 4;
b = 2;

// Charakteristische Laenge
cl = 2;

// Eckpunkte der Geometrie
Point(1) = {0, 0, 0, cl};
Point(2) = {l, 0, 0, cl};
Point(3) = {l, b, 0, cl};
Point(4) = {b, l, 0, cl};
Point(5) = {0, l, 0, cl};

// Rand der Geometrie
Line(6) = {1, 2};
Line(7) = {2, 3};
Line(8) = {3, 4};
Line(9) = {4, 5};
Line(10) = {5, 1};

// Fläche der Geometrie
Line Loop(1) = {10, 6, 7, 8, 9};
Plane Surface(1) = {1};

Physical Line(1) = {9, 8, 7};
Physical Line(2) = {10};
Physical Line(3) = {6};

Physical Surface(4) = {1};
