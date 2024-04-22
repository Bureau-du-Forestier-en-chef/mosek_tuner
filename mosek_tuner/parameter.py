/*
Copyright (c) 2023 Gouvernement du Québec

SPDX-License-Identifier: LiLiQ-R-1.1
License-Filename: LICENSES/EN/LiLiQ-R11unicode.txt
*/

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
        MAX_FAIL: Maximum number of time a search can fail before skipping the parameter
    """
    MAX_FAIL = 10
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
        return self._maximal_test > 0 and len(self._tested) < self._maximal_test and not self.__loosing_time()
    def __loosing_time(self)->bool:
        loose = False
        min_time = float('inf')
        max_time = 0
        if len(self._tested) > SolverParameter.MAX_FAIL:
            loose = True
            for test in self._tested[-SolverParameter.MAX_FAIL:]:
                if test._time != float('inf'):
                    loose = False
                    min_time = min(test._time,min_time)
                    max_time = max(test._time,max_time)
            if max_time != 0:
                loose = ((max_time-min_time) / min_time) > 0.01 #Need at least 1% change
        return loose
    def _save(self,p_time:float)->None:
        """Set the time took and save the parameter in the tested list"""
        self._time = p_time
        the_copy = deepcopy(self)
        self._tested.append(the_copy)
        for parameter in self._tested:
            parameter._tested = self._tested
    def get_sorted_tests_time(self)->[float]:
        """Return the time spent by the solver for each tests"""
        times = []
        for choice in self._tested:
            times.append(choice._time)
        if times:
            times =  sorted(times)[:SolverParameter.MAX_FAIL]
        return times
    def __lt__(self,other:SolverParameter):
        """less than"""
        return self._time < other._time
    def __gt__(self,other:SolverParameter):
        """greater than"""
        return self._time > other._time
    def __eq__(self,other:SolverParameter):
        """equality"""
        return (self._time - other._time) < 1
   
