from pathlib import Path
from subprocess import run
from re import search
from copy import deepcopy
from logging import basicConfig,info,INFO
from category import CategoricalParameter
from numerical import NumericalParameter
from os.path import isfile
from csv import DictReader


class ParametersTuner:
    """Mosek Parameters tuner

    Tune parameters for one problem.

    Attributes:
        folder: the mosek execution folder.
        problem: the .mps or .lp that we want to test.
        maximisaiton: tell if maximisation = true else minimization
        path_to_parameters: path to parameter file.
    """
    def __init__(self,p_problem_path:Path,
                 p_path_to_parameters:Path,
                 p_max:bool=False):
        """Inits ParametersTuner with the problem path, a folder path to put the best parameters
        and a path to a .mps or .lp file to tune one."""
        for file in [p_problem_path,p_path_to_parameters]:
            if not isfile(str(file)):
                raise RuntimeError(str(file) + "is not a valid file")
        self.__problem = p_problem_path
        self.__max = p_max
        basicConfig(filename="Tuner.log", 
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    level = INFO)
        self.__path_to_parameters = p_path_to_parameters
    def optimize(self):
        """Optimize the parameters with a csv files of parameters"""
        parameters = ParametersTuner.__read_parameters(self.__path_to_parameters)
        INITIAL_RUNNING_TIME = self.__run_mosek()
        best_time = INITIAL_RUNNING_TIME
        best_parameters = deepcopy(parameters)
        ParametersTuner.__write_parameters(parameters,p_name="mosek_0.par")
        parameters = ParametersTuner.__get_parameters(INITIAL_RUNNING_TIME)
        info("Initial running time: " + str(INITIAL_RUNNING_TIME))
        iteration = 1
        while(ParametersTuner.__can_change_parameters(parameters)):
            ParametersTuner.__write_parameters(parameters,best_time)
            CURRENT_RUNNTIME = ParametersTuner.__run_mosek(self.__problem,self.__max)
            PARAMETERS_NAME = "mosek_"+str(iteration)+".par"
            ParametersTuner.__write_parameters(parameters,PARAMETERS_NAME)
            if CURRENT_RUNNTIME < best_time:
                best_time = CURRENT_RUNNTIME
                best_parameters = deepcopy(parameters)
                ParametersTuner.__write_parameters(best_parameters,"mosek_best.par")
            info("Running time of "+str(best_time)+" at iteration "+iteration)
            parameters = ParametersTuner.__get_parameters(CURRENT_RUNNTIME)
            iteration +=1
    def __read_parameters(p_path_to_parameters:Path)->[]:
        """From a .csv file read the parameters we want to optimize first column is the parameter name
        lower_bound,upper_bound,categories (separated by |) if categories not empty it wont look at bound"""
        parameters = []
        info("Reading parameters from "+str(p_path_to_parameters))
        parameters_read = set()
        with open(p_path_to_parameters) as input_parameters_file:
            reader =  DictReader(input_parameters_file, delimiter=",")
            for line in reader:
                PARAMETER_NAME = line["name"]
                if PARAMETER_NAME in parameters_read:
                    RuntimeError(PARAMETER_NAME+" already exist in "+p_path_to_parameters)
                parameters_read.add(PARAMETER_NAME)
                CATEGORIES = line["categories"]
                if CATEGORIES:
                    PARAMETERS_CAT = CATEGORIES.split("|")
                    parameters.append(CategoricalParameter(PARAMETER_NAME,PARAMETERS_CAT))
                else:
                    LOWER_BOUND = line["lower"]
                    UPPER_BOUND = line["upper"]
                    n_tests = 0
                    if line["tests"]:
                        n_tests = int(line["tests"])
                    lower = 0
                    upper = 0
                    if (LOWER_BOUND.isdigit() and UPPER_BOUND.isdigit()):
                        lower = int(LOWER_BOUND)
                        upper = int(UPPER_BOUND)
                    else:
                        lower = float(LOWER_BOUND)
                        upper = float(UPPER_BOUND)
                    parameters.append(NumericalParameter(PARAMETER_NAME,lower,upper,n_tests))
        info("Read "+str(len(parameters))+" parameters")
        return parameters  
    def __write_parameters(p_parameters:[],p_best_time:float=float("inf"),p_name:str="mosek.par")->None:
        """Write down the parameters in a mosek parameter file"""
        with Path(p_name).open() as parameters_file:
            parameters_file.write("BEGIN MOSEK")
            if p_best_time != float("inf"):
                parameters_file.write("MSK_DPAR_OPTIMIZER_MAX_TIME "+str(p_best_time))#Make sure you dont spend time on bad parameters
            for parameter in p_parameters:
                parameters_file.write(parameter.name+" "+parameter.get_value())
            parameters_file.write("END MOSEK")
    def __get_time(p_log:str)->float:
        """Get the time took to run Mosek infinite if non feasible"""
        value = float('inf')
        #OPTIMAL = compile("Problem[\s\t]*status[\s\t]*:[\s\t]*PRIMAL_AND_DUAL_FEASIBLE")
        if  search("Problem[\s\t]*status[\s\t]*:[\s\t]*PRIMAL_AND_DUAL_FEASIBLE",p_log):
            time = search("(Optimizer[\s\t]*-[\s\t]*time:[\s\t]*)([0-9]*[.][0-9]*)",p_log)
            if time:
                value = float(time.group(2))
        return value
    def __get_parameters(p_parameters:[],p_time:float)->[]:
        """Get new values for different parameters"""
        new_parameter = []
        for parameter in p_parameters:
            if parameter.can_change():
                new_parameter.append(parameter.generate(p_time))
            else:
                new_parameter.append(parameter.get_best())
        return new_parameter
    def __can_change_parameters(p_parameters:[])->bool:
        """Return true true any parameters can be changed"""
        for parameter in p_parameters:
            if parameter.can_change():
                return True
        return False
    def __run_mosek(p_problem:Path,p_max:bool)->float:
        """Run Mosek and return the amount of time took if it is not optimal it will return max float"""
        parameters = ["mosek.exe","-p","mosek.par"]
        if p_max:
            parameters.append("-max")
        parameters.append(p_problem)
        result = run(parameters, capture_output=True, text=True)
        return ParametersTuner.__get_time(result.stdout.decode('utf-8'))
   
            

if __name__ == "__main__":
    print("Unit tests for Tuner")
    print("test log reader")
    with open("tests/mosek92_2thread.log", "r") as log_file:
        log_str = log_file.read()
        time = ParametersTuner._ParametersTuner__get_time(log_str)
        assert(time == 1252.72)
    with open("tests/mosek101_2thread_essaie#1.log", "r") as log_file:
        log_str = log_file.read()
        time = ParametersTuner._ParametersTuner__get_time(log_str)
        assert(time == 21836.36)
    with open("tests/mosek_ns.log", "r") as log_file:
        log_str = log_file.read()
        time = ParametersTuner._ParametersTuner__get_time(log_str)
        assert(time == float('inf'))
    assert(ParametersTuner._ParametersTuner__get_time("NOTHING")==float('inf'))
    print("test log reader done!")
    print("test read_parameters")
    parameters = ParametersTuner._ParametersTuner__read_parameters(Path("tests/mosek_parameters.csv"))
    can_move = 0
    for parameter in parameters:
        can_move+=parameter.can_change()
    assert(can_move==6)
    assert(len(parameters)==7)
    print("test read_parameters done!")
    print("test run mosek")
    result = ParametersTuner._ParametersTuner__run_mosek(Path(),True)
    assert(len(result)>0)
    print("test run mosek done")
    print("Unit tests for Tuner done!")