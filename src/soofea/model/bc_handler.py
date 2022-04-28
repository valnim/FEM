'''
Created on Nov 12, 2012

@author: mueli
'''

from abc import ABCMeta, abstractmethod


class BCHandler:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._model = None

    def setModel(self, model):
        self._model = model

    @abstractmethod
    def integrateBC(self, time_stamp):
        pass
