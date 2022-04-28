import numpy as np

#Excercise 1
#Ente: 13/27
#Fuchs: 12/27

a = [1, 2, 3, 4]
b = np.linspace(0, 1, 4)
A = np.array([[1, 2], [3, 4]])
B = A + 3
C = 3 * A
print(B*C)


#Excercise 2
x1 = np.array([[2],[5]])
x2 = np.array([[7],[2]])

x1 = x1[::-1]
print(x1)

A = np.hstack([x1,x2])
print(A)
B = A.T
print(B)

C = A @ B
print(C)

print(np.linalg.det(np.linalg.inv(C))-1/np.linalg.det(C))  #Rest aufgrund von Floatingpoint Fehlern

#Excercise 3

def computepi(n):
    pi = 0
    for i in range(n):
        pi = pi + (1/((2*i)+1))*(-1)**i
    return 4 * pi

print(computepi(10000))

def unit13():
    narr = np.array([10, 100, 1000, 10000])
    computepi_vec = np.vectorize(computepi)
    values = computepi_vec(narr)
    print(values)
    errors = np.abs((values - np.pi)/np.pi)
    print(errors)

    import matplotlib.pyplot as plt
    plt.loglog(narr, errors)
    plt.xlabel('n')
    plt.ylabel('error')
    plt.title('Error of numerical approximation of pi')
    plt.grid(True)
    plt.show()

unit13()

#OOP

#Class Shape with methods area and perimeter
from abc import ABC, abstractmethod

class Shape(ABC):
    def getArea(self):
        return self.calcArea()

    def getPerimeter(self):
        return self.calcPerimeter()

    @abstractmethod
    def calcArea(self):
        pass

    @abstractmethod
    def calcPerimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calcArea(self):
        return np.pi * self.radius**2

    def calcPerimeter(self):
        return 2 * np.pi * self.radius

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def calcArea(self):
        return self.length**2

    def calcPerimeter(self):
        return 4 * self.length

#Test Shapes
c1 = Circle(3)
area_c1 = c1.getArea()
perimeter_c1 = c1.getPerimeter()
print(area_c1)
print(perimeter_c1)

s1 = Square(3)
area_s1 = s1.getArea()
perimeter_s1 = s1.getPerimeter()
print(area_s1)
print(perimeter_s1)

#Because Shape is an Abstract Method, no object of that type can be created
#Because the method calcArea is private



#Excercise 5
import sys, os
src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

import numpy as np
from soofea.model.model import Node, NodeContainer, Element, Model

n1_coords = np.array([3, 4])
n1_number = 1
n1 = Node(n1_number, n1_coords)
print(n1)

dimension = 2

my_model = Model(dimension)

node_number_list = [1, 2, 3, 4]
node_coord_list = np.array([[0.0, 0.0],
                            [0.5, 0.0],
                            [0.5, 0.5],
                            [0.0, 0.5],])
for node_number, node_coord in zip(node_number_list, node_coord_list):
    my_model.addNode(Node(node_number, node_coord))

element_number_list = [1]
element_node_numbers_list = [[1, 2, 3, 4]]
for element_number, element_node_numbers in zip(element_number_list,
                                                element_node_numbers_list):
    my_model.addElement(Element(element_number, element_node_numbers))

print(my_model._element_dict[1].getCoordinateArray())



print('Programmende')

