For the grid solver project I wrote the program in Python3.6 in Ubuntu.
There are two folders
	gridSolver contains the program to gridSolve the original given dataset
	testHarness contains code to generate beacon range readings and then evaluate them using the gridSolver
        I was not able to get a working API running

For this you will need the following Python packages:
	numpy
	os
	multiprocessing (this was used because python favors multiprocessing over multithreading)
	csv
	random
	math

For gridSolver
	In the gridSolver folder you need the following
		gridSolver.py
		beacons.csv
		grid.csv
		ranges.csv

	input file format
		beacons.csv -> 3 comma separated values containing the x, y, and z location of a beacon. beacons are seperated by lines
		grid.csv -> grid containing 0 and 1 where 0 is unoccupied and 1 is occupied
		ranges.csv -> 3 comma separated values containing the beacon_number, range, timestamp

	output file format
		outFile.csv - > 4 comma separated values containing x, y, z location estimate of the phone, and the timestamp for the estimate

	To run this project
		1. use the terminal to set your current directory to the location of the gridSolver folder
		2. run the following command in the command line "python3 gridSolver.py" without the ""
			You may need to use "python" instead of "python3" depending on how you have Python configured
		3. wait for the program to run. an output file named "outFile.csv" should appear in the codingChallenge folder containing the localization 

For testHarness
	In the testHarness folder you need the following
		gridSolver.py
		testHarness.py
		beacons.csv
		grid.csv

	input file format
		beacons.csv -> 3 comma separated values containing the x, y, and z location of a beacon. beacons are seperated by lines
		grid.csv -> grid containing 0 and 1 where 0 is unoccupied and 1 is occupied

	output file format
		outFile.csv - > 4 comma separated values containing x, y, z location estimate of the phone, and the timestamp for the estimate

	To run this project
		1. use the terminal to set your current directory to the location of the testHarness folder
		2. run the following command in the command line "python3 testHarness.py" without the ""
			You may need to use "python" instead of "python3" depending on how you have Python configured
		3. wait for the program to run. an output file named "outFile.csv" should appear in the codingChallenge folder containing the localization 



