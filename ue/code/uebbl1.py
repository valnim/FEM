import numpy as np
import plotly.graph_objects as go
import abc
from soofea.model.model import Node, Element, Model

# Exercise 1
print("Fuchs: 12/27")
print("Ente: 13/27")

# Exercise 2
x1 = np.array([[2], [5]])
x2 = np.array([[7], [2]])

temp = x1[0, 0]
x1[0, 0] = x1[1, 0]
x1[1, 0] = temp

A = np.hstack([x1, x2])
B = A.T

C = A @ B
print(f"C: {C}")

y1 = 1 / np.linalg.det(C)
y2 = np.linalg.det(np.linalg.inv(C))
np.testing.assert_almost_equal(y1, y2)

# Exercise 3
def compute_pi(N):
    pi = 0
    for idx in range(int(N)):
        pi = pi + (-1)**idx / (2*idx + 1)
    return 4 * pi


N_arr = np.array([1e1, 1e2, 1e3, 1e4, 1e5])
v_compute_pi = np.vectorize(compute_pi)
Sol = v_compute_pi(N_arr)
Err = np.abs((Sol - np.pi) / np.pi)
print(f"Error:\n{Err}")

fig = go.Figure(data=go.Scatter(x=N_arr, y=Err))
fig.update_xaxes(type="log")
fig.update_yaxes(type="log")
fig.show()

# Exercise 4
class Shape:
    def get_area(self):
        return self._calc_area()

    def get_perimeter(self):
        return self._calc_perimeter()

    @abc.abstractmethod
    def _calc_area(self):
        return

    @abc.abstractmethod
    def _calc_perimeter(self):
        return


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def _calc_area(self):
        return self.radius**2 * np.pi

    def _calc_perimeter(self):
        return self.radius * 2 * np.pi


class Square(Shape):
    def __init__(self, x):
        self.x = x

    def _calc_area(self):
        return self.x

    def _calc_perimeter(self):
        return 4 * self.x


def test_Shapes():
    sq = Square(2)
    sq.get_perimeter()

    cr = Circle(5)
    cr.get_perimeter()

test_Shapes()

# 4.4: Because Shape is an abstract class
# 4.5: Because the method is private

# Exercise 5
n1_coords = np.array([3, 4])
n1_number = 1
n1 = Node(n1_number, n1_coords)
print(n1)

dimension = 2
my_model = Model(dimension)
node_number_list = [1, 2, 3, 4]
node_coord_list = np.array([[0.0, 0.0],
                            [1.0, 0.0],
                            [1.0, 1.0],
                            [0.0, 1.0]])

for node_number, node_coord in zip(node_number_list, node_coord_list):
    my_model.addNode(Node(node_number, node_coord))

element_number_list = [1]
element_node_numbers_list = [[1, 2, 3, 4]]
for element_number, element_node_numbers in zip(element_number_list,
                                                element_node_numbers_list):
    my_model.addElement(Element(element_number, element_node_numbers))

print(my_model._element_dict[1].getCoordinateArray())
print(my_model)

pass
