# -*- coding:utf-8 -*-

from exceptions import RuntimeError

class RobotCheckError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

class OperationError(RuntimeError):
    def __init__(self, arg):
        self.args = arg