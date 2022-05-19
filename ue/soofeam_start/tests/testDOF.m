addpath examples/plateDOF

% The model is created in the function 'examples/plateDOF'. We will proceed
% in the same way later when calculating a 'real' example.
model = plateDOF();

% The Dirichlet boundary conditions are stored in the DisplacementDOF
% objects of the nodes.
model.bc_handler.incorporateBC();


%---- Exercise 7 ----%

% Output to command line
for i = 1:length(model.node_dict)
    fprintf('\nNode #%u:\n',i)
    
    node = model.node_dict(i);
    
    disp('  Node constraints:')
    disp(node.dof.constraint);
    
    disp('  Node displacements:')
    disp(node.dof.displacement);
end

% Plotting
for i = 1:length(model.node_dict)
    nodeconstraint(:,i) = model.node_dict(i).dof.constraint;
    nodedisplacement(:,i) = model.node_dict(i).dof.displacement;
    nodecoor(:,i) = model.node_dict(i).undeformed_coordinates;
end
newnodecoor = nodecoor + 10*nodedisplacement;

figure
plot(nodecoor(1,:),nodecoor(2,:),'o','Color',[0,0,0],'MarkerFaceColor',[0.6,0.6,0.6],'Markersize',10); 
hold on
plot(newnodecoor(1,:),newnodecoor(2,:),'x','Color',[0,0,0],'MarkerFaceColor',[0.6,0.6,0.6],'Markersize',10); 
