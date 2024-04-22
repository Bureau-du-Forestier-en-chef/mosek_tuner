<a href = "./README.fr.md"><img src = "https://img.shields.io/badge/%F0%9F%87%AB%F0%9F%87%B7-Click%20here%20for%20a%20french%20version-blue?style=flat-square" height="25" /></a>

## Parameters tuner for Mosek

The objective of the tuner is to reduce the amount of time spent on solving a problem using [Mosek](https://www.mosek.com/).
by tuning the solver's parameters. 

### How

First, you need to [Mosek installed](https://www.mosek.com/downloads/) on your machine. 

<p>Starting without any parameters the tuner will solve the problem using Mosek and find the initial solving time. 
Then starting with the first parameter in the csv file it will try to decrease the amount of time spent on solving by 
doing binary search on numerical parameter and enumeration for categorical parameters. 
If after 5 tries no decrease in solving time is observe then it will go to the next parameter.
For numerical parameter it will also stop the search when it reach the maximal number
of tests.</p>

### Inputs
<p>For tuning Mosek's parameters you need a problem file (.mps/.lp) and also a 
csv file containing the parameters you want to tune.</p>

Columns description:
 - name
   - A valid parameter (https://docs.mosek.com/latest/cmdtools/parameters.html#doc-all-parameter-list)
 - lower
   - The minimal value for int or float parameter
 - upper
   - The maximal value for int or float parameter
 - tests
   - The maximal numbers of tests done on float or int parameter
 - categories
   - The values tested for categorical parameter 

| name                      | lower   | upper   | tests | categories                                             |
|:--------------------------|:-------:|:-------:|:-----:|:------------------------------------------------------:|
|MSK_DPAR_PRESOLVE_TOL_S    |0.0      |0.0001   |50     |                                                        |
|MSK_IPAR_BI_CLEAN_OPTIMIZER|         |         |       |MSK_OPTIMIZER_DUAL_SIMPLEX\|MSK_OPTIMIZER_PRIMAL_SIMPLEX|
|MSK_IPAR_BI_MAX_ITERATIONS |999999999|999999999|       |                                                        |

### Run
Launch the tuner:

```bat
mkdir temp
pushd temp
	python.exe ../tune.py -m ../tests/test.lp -p ../tests/mosek_parameters.csv -max
popd
pause
```
### Outputs

<p>In the Tuner.log you will find information about the number of time it took to solve your problem.
Here the initial solving time is 22996.58 seconds. At iteration 1 the solving time is now 15469.78.
The sensibility of the MSK_DPAR_PRESOLVE_TOL_S is important with a range of 14478.49 to 22996.58 seconds (37%).</p>

```
2024-04-19 09:01:57,135: INFO: Reading parameters from ..\tests\mosek_parameters_complete.csv
2024-04-19 09:01:57,136: INFO: Read 33 parameters
2024-04-19 15:25:43,318: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S None
2024-04-19 15:25:43,319: INFO: Initial solving time: 22996.58
2024-04-19 19:44:01,867: INFO: Solving time of 15469.78 at iteration 1
2024-04-19 19:44:01,867: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 5e-05
2024-04-20 00:03:46,135: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 2.5e-05
2024-04-20 04:06:32,862: INFO: Solving time of 14544.67 at iteration 3
2024-04-20 04:06:32,862: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 3.7500000000000003e-05
2024-04-20 08:08:12,679: INFO: Solving time of 14478.49 at iteration 4
2024-04-20 08:08:12,693: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 1.25e-05
2024-04-20 12:10:25,434: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 6.250000000000001e-06
2024-04-20 12:10:25,434: INFO: Sensibility of: MSK_DPAR_PRESOLVE_TOL_S (14478.49 14511.36 14544.67 15469.78 15553.38 22996.58)
2024-04-20 16:10:46,924: INFO: Solving time of 14400.34 at iteration 6
2024-04-20 16:10:46,924: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 1.5625e-05
2024-04-20 20:11:25,154: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 1.2500000000000002e-05
2024-04-21 00:12:19,634: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 2.9e-05
2024-04-21 04:13:04,096: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 8.249999999999999e-06
2024-04-21 08:13:44,807: INFO: Working on MSK_DPAR_PRESOLVE_TOL_S 1.0375000000000001e-05
2024-04-21 12:15:09,935: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X None
2024-04-21 16:15:51,026: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 5e-05
2024-04-21 20:16:35,476: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 2.5e-05
2024-04-22 00:17:03,341: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 3.7500000000000003e-05
2024-04-22 04:17:40,800: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 1.25e-05
2024-04-22 04:17:40,800: INFO: Sensibility of: MSK_DPAR_PRESOLVE_TOL_X (14406.84 14416.67 14419.74 14423.48 14464.39)
2024-04-22 08:18:50,707: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 1.8750000000000002e-05
2024-04-22 12:19:48,349: INFO: Working on MSK_DPAR_PRESOLVE_TOL_X 1.5625e-05
```

<p>In the temp folder you can now see the best parameters found in the mosek_best.par file. The tuner will write
down the best parameters each time a new parameter value is found to be good.</p>

```
BEGIN MOSEK
MSK_DPAR_PRESOLVE_TOL_S 1.5625e-05
MSK_IPAR_BI_MAX_ITERATIONS 999999999
END MOSEK
```

## License 

mosek_tuner is a [LiLiQ-R 1.1](https://github.com/Bureau-du-Forestier-en-chef/mosek_tuner/blob/master/LICENSES/EN/LILIQ-R11EN.pdf) licensed library.

[![License](http://img.shields.io/:license-liliqR11-blue.svg?style=flat-square)](https://forge.gouv.qc.ca/licence/liliq-v1-1/#r%C3%A9ciprocit%C3%A9-liliq-r)

