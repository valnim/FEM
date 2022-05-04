addpath examples/plateDOF

% The model is created in the function 'examples/plateDOF'. We will proceed
% in the same way later when calculating a 'real' example.
model = plateDOF();

% The Dirichlet boundary conditions are stored in the DisplacementDOF
% objects of the nodes.
model.bc_handler.incorporateBC();


%---- Exercise 7 ----%