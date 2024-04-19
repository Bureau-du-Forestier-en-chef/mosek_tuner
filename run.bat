mkdir temp
pushd temp
	python.exe ../tune.py -m ../tests/test.lp -p ../tests/mosek_parameters.csv -max
popd
pause
