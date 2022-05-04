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
order = 1;
tri_shape = nsModel.nsShape.TriangleShape(order);

disp('N-Matrix of the triangle in the first node:')
disp(tri_shape.getArray([0 0]))

disp('N-Matrix of the triangle in the second node:')
disp(tri_shape.getArray([1 0]))

disp('N-Matrix of the triangle in the third node:')
disp(tri_shape.getArray([0 1]))



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
