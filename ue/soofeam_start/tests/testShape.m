% The linear triangle reference element looks like this:

% eta
% ^
% |
% 3 (0/1)
% |`\
% |  `\
% |    `\
% |      `\
% |        `\
% 1----------2 --> xi
% (0/0)      (1/0)

% Here we check if all shape functions are 1 in their 'own' node and 0 in
% all other nodes.
% order = 1;
% tri_shape = nsModel.nsShape.TriangleShape(order);
% 
% disp('N-Matrix of the triangle in the first node:')
% disp(tri_shape.getArray([0 0]))
% 
% disp('N-Matrix of the triangle in the second node:')
% disp(tri_shape.getArray([1 0]))
% 
% disp('N-Matrix of the triangle in the third node:')
% disp(tri_shape.getArray([0 1]))



%---- Exercise 2 ----%

% The bilinear reference quad element looks like this:
%
%   eta
%   ^
%   |
%   |(0/1)       (1/1)
%   4-----------3
%   |           |
%   |           |
%   |           | 
%   |           |
%   |           |
%   1-----------2 --> xi
%    (0/0)       (1/0)

order = 1;
quad_shape = nsModel.nsShape.QuadShape(order);

disp('N-Matrix of the quad in the first node:')
disp(quad_shape.getArray([0 0]))

disp('N-Matrix of the quad in the second node:')
disp(quad_shape.getArray([1 0]))

disp('N-Matrix of the quad in the third node:')
disp(quad_shape.getArray([1 1]))

disp('N-Matrix of the quad in the fourth node:')
disp(quad_shape.getArray([0 1]))

coords = [0.75 0.15];
dN     = quad_shape.getDerivativeArray(coords);
disp('Partial derivativese at [0.75 0.15]:')
disp(dN)

disp('Derivative dN3_deta')
disp(dN(3,2))
