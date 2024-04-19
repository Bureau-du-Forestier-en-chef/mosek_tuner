from __future__ import annotations
from .parameter import SolverParameter
from copy import deepcopy
from random import shuffle

class NumericalParameter(SolverParameter):
    """Mosek Continuous Solver Parameters

    Handle Mosek Continuous solver parameters.

    Attributes:
        lower: lower bound int or float
        upper: upper bound int or float
        value: parameter value
    """
    def __init__(self,p_name:str,p_lower_bound,p_upper_bound,p_number_tests:int):
        """Inits NumericalParameter with a name and lower and upper bound if lower is > then upper 
        it will throw"""
        super().__init__(p_name,p_number_tests)
        if p_lower_bound > p_upper_bound:
            raise RuntimeError("Lower bound is greater then upper for parameter "+p_name)
        self.__lower = p_lower_bound
        self.__upper = p_upper_bound
        if p_lower_bound != p_upper_bound:
            self.__value =  None#self.__lower + NumericalParameter.__divide_by_two(self.__upper - self.__lower)
        else:
            self.__value = self.__lower
    def get_value(self)->str:
        """Get the value of the parameter"""
        returned = None
        if self.__value is not None:
            returned = str(self.__value)
        return returned
    def generate(self,p_time:float)->NumericalParameter:
        """Generate a new parameter based on binary search"""
        valuable = []
        for test in self._tested:
            if test.get_value() is not None:
                valuable.append(test)
        SORTED_LIST = sorted(valuable)
        BEST_ONE = None
        if SORTED_LIST:
            BEST_ONE = SORTED_LIST[0]
        self._save(p_time)
        new_parameter = deepcopy(self)
        new_parameter._time = float('inf')
        target = new_parameter.__lower + NumericalParameter.__divide_by_two(new_parameter.__upper - new_parameter.__lower)
        if self.__value is not None:
            if BEST_ONE is None:#No data
                target = self.__lower + NumericalParameter.__divide_by_two(self.__value - self.__lower)
            elif (self <  BEST_ONE): #the new solution is better then go on the left
                if BEST_ONE.__get_side_of(self) == "left": #Scrap right side
                    new_parameter.__upper = BEST_ONE.__value
                else:
                    new_parameter.__lower = BEST_ONE.__value
                target = NumericalParameter.__divide_by_two(new_parameter.__upper - new_parameter.__lower)
            elif(BEST_ONE < self): #If the last move was worst
                if BEST_ONE.__get_side_of(self) == "left": #if left is bad go on the right side of best_one
                    new_parameter.__lower = self.__value
                else: #if it is on the right then go on the left
                    new_parameter.__upper = self.__value
                target = NumericalParameter.__divide_by_two(new_parameter.__upper - new_parameter.__lower)
            elif(BEST_ONE == self):
                target  = max(self.__lower,NumericalParameter.__divide_by_two(self.__value))
        else:
            target = self.__lower + NumericalParameter.__divide_by_two(self.__upper - self.__lower)
        new_parameter.__set_target(target)
        return new_parameter
    def can_change(self) -> bool:
        is_stock = False
        if isinstance(self.__value,int) and self.__is_already_tested():
            is_stock = True
        return self.__lower != self.__upper and super().can_change() and not is_stock
    def __get_side_of(self,other : NumericalParameter)->str:
        """check if the other is on the right on left side of the binary search"""
        side = "right"
        if other.__value < self.__value:
            side = "left"
        return side
    def __divide_by_two(p_value):
        """Divide a number by two knowing it can be float or int and return result"""
        result = 0
        if isinstance(p_value,int):
            result = p_value // 2
        else:
            result = p_value / 2
        return result
    def __is_already_tested(self)->bool:
        """Check if parameters alreayd tested"""
        for parameter in self._tested:
            if parameter.__value == self.__value:
                return True
        return False
    def __set_target(self,p_initial)->None:
        """Set the target value of the parameter"""
        self.__value = p_initial
        if self.__is_already_tested():
            self.__value = None
            step = 1
            if not isinstance(p_initial,int):
                step = ((self.__upper - self.__lower) / 100)
                range_of =[ self.__lower + step * index for index in range(0,100)]
            else:
                range_of = list(range(self.__lower,self.__upper,step))
            for parameter in self._tested:
                if parameter.__value in range_of:
                    range_of.remove(parameter.__value)
            if self.__value in range_of:
                range_of.remove(self.__value)
            if range_of:
                shuffle(range_of)
                self.__value = range_of[0]
    def __str__(self):
        """string representation of the parameter"""
        value = ""
        if self.__value is not None:
            value = self.name +" "+self.get_value()
        return value
    
if __name__ == "__main__":
    print("Unit tests for NumericalParameter")
    parameter = NumericalParameter("test1",1,10,10)
    print("test get_value")
    newone = parameter.generate(10)
    assert(newone.get_value() != None)
    newone2 = newone.generate(20)
    assert(newone2.get_value() == "3")
    newone3 = newone2.generate(5)
    assert(newone3.get_value() == "2")
    parameter2 = NumericalParameter("test2",1.45,20.56,10)
    assert(parameter2.get_value() is None)
    print("test get_value done!")
    print("test generate")
    parameter_stock = NumericalParameter("test1",10,10,0)
    assert(parameter_stock.get_best() is not None)
    new_parameter = parameter_stock.generate(10)
    assert(new_parameter is not None)
    b1 = parameter2.get_best()
    b2 = parameter2.generate(10).get_best()
    assert(not b1 == b2)
    print("test generate done!")
    print("test name")
    assert(parameter.name == "test1")
    print("test name done!")
    print("test can_change")
    assert parameter2.can_change() == True
    assert NumericalParameter("test_param2",10,10,10).can_change() == False
    assert NumericalParameter("test_param3",10.45,10.45,10).can_change() == False
    print("test can_change done!")
    print("test to str")
    assert (str(parameter) == "")
    print("test to str done!")
    print("Unit tests for NumericalParameter done!")
