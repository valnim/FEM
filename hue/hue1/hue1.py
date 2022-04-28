import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class curve():
    @abstractmethod
    def xValue(self, parameter):
        pass

    @abstractmethod
    def yValue(self, parameter):
        pass

    @abstractmethod
    def zValue(self):
        pass


    def plotCurve(self, parameter_interval):
        ax = plt.figure().add_subplot(projection='3d')
        z = self.zValue(parameter_interval)
        x = self.xValue(parameter_interval)
        y = self.yValue(parameter_interval)
        ax.plot(x, y, z, label='parametric curve')
        ax.legend()

        plt.show()

class Circle(curve):
    def __init__(self, r):
        self.r = r

    def xValue(self, parameter):
        return self.r * np.cos(parameter)

    def yValue(self, parameter):
        return self.r * np.sin(parameter)

    def zValue(self, parameter):
        return 0


class TorusKnot(curve):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def xValue(self, parameter):
        return (2 + np.cos(self.p * parameter)) * np.cos(self.q * parameter)


    def yValue(self, parameter):
        return (2 + np.cos(self.p * parameter)) * np.sin(self.q * parameter)

    def zValue(self, parameter):
        return np.sin(self.p * parameter)


intervall = np.linspace(0, 10000, 100000)
c1 = Circle(10)
c1.plotCurve(intervall)

t1 = TorusKnot(2, 3)
t1.plotCurve(intervall)
