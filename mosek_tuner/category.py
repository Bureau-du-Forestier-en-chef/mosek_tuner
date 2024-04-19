from __future__ import annotations
from .parameter import SolverParameter
from copy import deepcopy

class CategoricalParameter(SolverParameter):
    """Mosek Categorical Solver Parameters

    Handle Mosek Categorical solver parameters.

    Attributes:
        values: Potential Categorical values in string.
        index: Index of the parameter int
    """
    def __init__(self,p_name:str,p_values:[str]):
        """Inits CategoricalParameter with a name and a list of potential values"""
        super().__init__(p_name,len(p_values))
        if len(p_values)==0:
            raise RuntimeError("No categories provided for parameter named "+p_name)
        self.__values = p_values
        if len(p_values) > 1:
            self.__index = None
        else:
            self.__index = 0
    def get_value(self)->str:
        """Get the value of the parameter"""
        returned = None
        if self.__index is not None:
            returned = self.__values[self.__index]
        return returned
    def generate(self,p_time:float)->CategoricalParameter:
        """Generate a new parameter"""
        self._save(p_time)
        new_parameter = deepcopy(self)
        new_parameter._time = float('inf')
        if new_parameter.__index is None:
            new_parameter.__index = 0
        else:
            if (new_parameter.__index < len(new_parameter.__values)-1):
                new_parameter.__index+=1
            else:
                new_parameter.__index = 0
        return new_parameter
    def can_change(self) -> bool:
        """Return true if you have multiple categories"""
        return super().can_change() and len(self.__values) > 1 and len(self._tested) != len(self.__values)
    def __str__(self)->str:
        """Get the string representation of the parameter"""
        value = ""
        if self.__index is not None:
            value = self.name +" "+self.get_value()
        return value

    
if __name__ == "__main__":
    print("Unit tests for CategoricalParameter")
    regular_cat = CategoricalParameter("test_param",["val1","val2","val3"])
    print("test name")
    assert (regular_cat.name == "test_param")
    print("test name done!")
    print("test get_value")
    assert regular_cat.get_value() == None
    print("test get_value done!")
    print("test can_change")
    assert regular_cat.can_change() == True
    single_cat = CategoricalParameter("test_param",["val1"])
    assert single_cat.can_change() == False
    print("test can_change done!")
    print("test generate")
    new_param = regular_cat.generate(10)
    print("test generate done!")
    print("test generated get_value")
    assert new_param.get_value() != regular_cat.get_value()
    print("test generated get_value done!")
    print("test name equal")
    assert new_param.name == regular_cat.name
    print("test name equal done!")
    sequence = ["val2","val3","val1","val2"]
    tested = []
    for index in range(0,4):
        new_param = new_param.generate(index)
        tested.append(new_param.get_value())
    print("test get_value over")
    assert sequence == tested
    print("test get_value over done!")
    print("test bad name")
    got_exception = False
    try:
        CategoricalParameter("",["test"])
    except RuntimeError:
        got_exception = True
    assert got_exception
    print("test bad name done!")
    print("test bad values")
    got_exception = False
    try:
        CategoricalParameter("test_param",[])
    except RuntimeError:
        got_exception = True
    assert got_exception
    print("test bad values done!")
    print("test to str")
    assert(str(single_cat) == "test_param val1")
    print("test to str done!")
    print("Unit tests for CategoricalParameter done!")
    