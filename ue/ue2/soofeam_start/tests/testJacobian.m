% The element is created with the script from Exercises 4.
% This element has the following node coordinates:
% x1 = (1/2)
% x2 = (4/1)
% x3 = (4/5)
% x4 = (1/3)
testElementType

% The surface area is calculated with the method nsNumeric.NumInt.methodIntegrate.
% Compare the result with the exact surface area.
area = nsNumeric.NumInt.methodIntegrate(@calcArea,element.int_points,element);
disp('Surface area of the element:')
disp(area)

%---- Exercise 5 ----%

% Which function must be integrated so that the result of the integration
% is the elements surface area? Keep in mind the integration is done on the
% reference element, so a coordinate transformation takes place.
function value = calcArea(int_point, element)
    % Create an object of type nsAnalyzer.nsJacobian.Jacobian. Pass the
    % element, the int_point and the configuration 'undeformed' to the
    % constructor.
    % jacobian = 
    
    % Which value must the function return?
    % value = 
end
