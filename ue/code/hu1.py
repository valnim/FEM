import abc
import numpy as np
import plotly.graph_objects as go

class Curve:
    def plot_curve(self, parameter_interval):
        X = self.x_value(parameter_interval)
        Y = self.y_value(parameter_interval)
        Z = self.z_value(parameter_interval)
        fig = go.Figure(go.Scatter3d(x=X, y=Y, z=Z, mode='lines'))
        fig.show()

    @abc.abstractmethod
    def x_value(self, parameter):
        return

    @abc.abstractmethod
    def y_value(self, parameter):
        return

    @abc.abstractmethod
    def z_value(self, parameter):
        return


class Circle(Curve):
    def __init__(self, r):
        self.r = r

    def x_value(self, parameter):
        return self.r * np.cos(parameter)

    def y_value(self, parameter):
        return self.r * np.sin(parameter)

    def z_value(self, parameter):
        return 0 * parameter


class TorusKnot(Curve):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def x_value(self, parameter):
        return (2 + np.cos(self.p * parameter)) * np.cos(self.q * parameter)

    def y_value(self, parameter):
        return (2 + np.cos(self.p * parameter)) * np.sin(self.q * parameter)

    def z_value(self, parameter):
        return np.sin(self.p * parameter)


c = Circle(5)
tk = TorusKnot(3, 4)
parameter_interval = np.linspace(0, 10, 1000)
c.plot_curve(parameter_interval)
tk.plot_curve(parameter_interval)
