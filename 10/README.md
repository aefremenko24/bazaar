# Directory 10

## Purpose
The main components of this directory are the _xserver_  and _xclients_ runnables. The harnesses consume JSON input from STDIN and produce results to STDOUT. There are also sample tests for both harnesses in the ./Tests folder.

## Files and directories:
- **\_\_init\_\_.py**: marks this directory on disk as a Python package directory
- **./Makefile**: sets up the python environment with all necessary packages for the Bazaar Game to be run.
- **./requirements.txt**: packages required for Bazaar to run.
- **./xserver**: executable file for the server harness. Expects inputs from STDIN when started and outputs to STDOUT when finished.
- **./xclients**: executable file for the clients harness. Expects inputs from STDIN when started and outputs to STDOUT when finished.
- **./Tests**: directory containing tests as a .json file pairs. For each test case n, there are two test files: n-in.json with given input, and n-out.json with expected output for that input.