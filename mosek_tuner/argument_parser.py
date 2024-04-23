'''
Copyright (c) 2023 Gouvernement du Québec

SPDX-License-Identifier: LiLiQ-R-1.1
License-Filename: LICENSES/EN/LiLiQ-R11unicode.txt
'''

from argparse import ArgumentParser
from .tuner import ParametersTuner
from pathlib import Path

class TunerParser(ArgumentParser):
    """Mosek Tuner parser

    Parse from commmand line the arguments needed to build a tuner.

    Attributes:
        __arguments: Arguments parsed by the user.
    """
    def __init__(self):
        """"Constructor for the argument parser"""
        super().__init__(description="Mosek Parameters tuner")
        self.add_argument('-m', dest='problem_path', type=str, required=True,
                    help='Matrix to solve')
        self.add_argument('-p', dest='parameters_path', type=str, required=True,
                    help='Path to the parameter file')
        self.add_argument('-max',dest='max' ,action='store_true')
        self.__arguments = None
    def get_tuner(self)->ParametersTuner:
        """"Will return a valid ParametersTuner or throw runtime errors"""
        self.__arguments = self.parse_args()
        return ParametersTuner(Path(self.__arguments.problem_path),
                               Path(self.__arguments.parameters_path),
                               self.__arguments.max)
    
if __name__ == "__main__":
    print("Testing TunerParser")
    from unittest.mock import patch
    import sys,os
    from tempfile import mkdtemp
    test_argv = ["test","-m",os.path.join(os.getcwd(),"tests/test.lp"),
                "-p",os.path.join(os.getcwd(),"tests/mosek_parameters.csv"),"-max"]
    temp_dir = mkdtemp()
    os.chdir(temp_dir)
    with patch.object(sys, 'argv', test_argv):
        parser = TunerParser()
        new_tuner = parser.get_tuner()
        assert(new_tuner.run())
    print("Testing TunerParser done!")