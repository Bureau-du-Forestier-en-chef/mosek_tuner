<a href = "./README.md"><img src = "https://img.shields.io/badge/%F0%9F%87%A8%F0%9F%87%A6-Cliquez%20ici%20pour%20la%20version%20anglaise-red?style=flat-square" height="25" /></a>

## Accordeur de paramètres pour Mosek

L'objectif du tuner est de réduire le temps passé à résoudre un problème à l'aide de [Mosek](https://www.mosek.com/).
en ajustant les paramètres du solveur.


### Comment

Tout d'abord, vous devez [installez Mosek](https://www.mosek.com/downloads/) sur votre machine.

<p>En démarrant sans aucun paramètre, le tuner résoudra le problème à l'aide de Mosek et trouvera le temps de résolution initial.
Ensuite, en commençant par le premier paramètre du fichier csv, il tentera de réduire le temps consacré à la résolution en
effectuer une recherche binaire sur les paramètres numériques et une énumération des paramètres catégoriels.
Si après 5 essais aucune diminution du temps de résolution n’est observée alors on passera au paramètre suivant.
Pour les paramètres numériques, la recherche s'arrêtera également lorsqu'elle atteindra le nombre maximal.
de tests.</p>


### Intrants
<p>Pour régler les paramètres de Mosek, vous avez besoin d'un fichier de problèmes (.mps/.lp) ainsi que d'un
fichier csv contenant les paramètres que vous souhaitez régler.</p>

Description des colonnes :
 - name
   - Un paramètre valide (https://docs.mosek.com/latest/cmdtools/parameters.html#doc-all-
 - lower
   - La valeur minimale du paramètre int ou float
 - upper
   - La valeur maximale du paramètre int ou float
 - tests
   - Le nombre maximal de tests effectués sur le paramètre float ou int
 - categories
   - Les valeurs testées pour le paramètre catégoriel

| name                      | lower   | upper   | tests | categories                                             |
|:--------------------------|:-------:|:-------:|:-----:|:------------------------------------------------------:|
|MSK_DPAR_PRESOLVE_TOL_S    |0.0      |0.0001   |50     |                                                        |
|MSK_IPAR_BI_CLEAN_OPTIMIZER|         |         |       |MSK_OPTIMIZER_DUAL_SIMPLEX\|MSK_OPTIMIZER_PRIMAL_SIMPLEX|
|MSK_IPAR_BI_MAX_ITERATIONS |999999999|999999999|       |                                                        |

### Exécuter
Lancez le tuner :

```bat
mkdir temp
pushd temp
	python.exe ../tune.py -m ../tests/test.lp -p ../tests/mosek_parameters.csv -max
popd
pause
```
### Extrants

<p>Dans le fichier Tuner.log, vous trouverez des informations sur le temps nécessaire pour résoudre votre problème.
Ici, le temps de résolution initial est de 22996,58 secondes. À l'itération 1, le temps de résolution est désormais de 15469,78.
La sensibilité du MSK_DPAR_PRESOLVE_TOL_S est importante avec une plage de 14478,49 à 22996,58 secondes (37%).</p>

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

<p>Dans le dossier temporaire, vous pouvez maintenant voir les meilleurs paramètres trouvés dans le fichier mosek_best.par. Le tuner écrira
les meilleurs paramètres chaque fois qu'une nouvelle valeur de paramètre s'avère bonne.</p>


```
BEGIN MOSEK
MSK_DPAR_PRESOLVE_TOL_S 1.5625e-05
MSK_IPAR_BI_MAX_ITERATIONS 999999999
END MOSEK
```

## License 

mosek_tuner est une bibliothèque sous licence [LiLiQ-R 1.1](https://github.com/Bureau-du-Forestier-en-chef/mosek_tuner/blob/master/LICENSES/EN/LILIQ-R11EN.pdf) licensed library.

[![License](http://img.shields.io/:license-liliqR11-blue.svg?style=flat-square)](https://forge.gouv.qc.ca/licence/liliq-v1-1/#r%C3%A9ciprocit%C3%A9-liliq-r)

