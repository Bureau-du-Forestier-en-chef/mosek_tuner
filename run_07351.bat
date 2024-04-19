rmdir /s /q temp
mkdir temp
pushd temp
	python.exe ../tune.py -m D:/test/PC_9589_U07351_4_Vg3_2023_vSSP6.Mps -p ../tests/mosek_parameters_complete.csv -max
popd

pause
