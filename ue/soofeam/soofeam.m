restoredefaultpath
close all
clear
clc

% %---- FE calculation ----%

% Define example name
example = 'plateAnalysis';

% adding paths
addpath src
addpath (['examples/',example]);

% Creating the model and analysis objects using the example file
fprintf('Creating Model ...\n')
[model, analysis] = feval(example);

% running the analysis - whether linear or nonlinear is specified in the
% example file.
fprintf('\nStarting Analysis ...\n')
analysis.run();
fprintf('\n\n... done\n')
