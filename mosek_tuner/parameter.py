from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy


class SolverParameter(ABC):
    """Mosek Solver Parameters abstract class

    Handle Mosek solver parameters

    Attributes:
        name: the name of the parameter.
        time: the amount of seconds took by the solver with this parameter.
        tested: List of parameters tested.
        maximal_test: Maximum number of tests we want to make
    """
    def __init__(self,p_name:str,p_maximal_tests:int):
        """Inits SolverParameter with a name"""
        if not p_name:
            raise RuntimeError("Empty parameter name")
        self._name = p_name
        self._time = float('inf')
        self._tested = []
        self._maximal_test = p_maximal_tests
    def get_best(self)->SolverParameter:
        """Get best parameter value found"""
        bestParameter = deepcopy(self)
        if len(self._tested) >0:
            bestParameter = deepcopy(sorted(self._tested)[0])
        return bestParameter
    @property
    def name(self)->str:
        """Get the name of the parameter"""
        return self._name
    @abstractmethod
    def get_value(self)->str:
        """Get the value of the parameter"""
        pass
    @abstractmethod
    def generate(self,p_time:float)->SolverParameter:
        """Generate a new parameter"""
        pass
    def can_change(self)->bool:
        """Check if you can change the parameter if you dont reach the maximal tests"""
        return self._maximal_test > 0 and len(self._tested) < self._maximal_test
    def _save(self,p_time:float)->None:
        """Set the time took and save the parameter in the tested list"""
        self._time = p_time
        the_copy = deepcopy(self)
        self._tested.append(the_copy)
    def __lt__(self,other:SolverParameter):
        """less than"""
        return self._time < other._time
    def __gt__(self,other:SolverParameter):
        """greater than"""
        return self._time > other._time
    def __eq__(self,other:SolverParameter):
        """equality"""
        return (self._time - other._time) < 1
   
