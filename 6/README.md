# Directory 6

## Purpose
The main component of this directory is the _xrules_ test harness. The harness consumes JSON input from STDIN and produces results to STDOUT. There are also four sample tests for the _xrules_ harness in the ./Tests folder.

## Files and directories:
- **\_\_init\_\_.py**: marks this directory on disk as a Python package directory
- **./Makefile**: sets up the python environment with all necessary packages for the Bazaar Game to be run.
- **./requirements.txt**: packages required for Bazaar to run.
- **./xrules**: executable file for the test harness. Expects inputs from STDIN when started and outputs to STDOUT when finished. 
  - The input to _xrules_ consists of a list of Equations, the TurnState given to the active player, and the Rules representing the chosen pebble exchanges.
  - The output of _xrules_ consists of: the JSON value false indicating that the proposed trades are illegal or two JSON values indicating that the proposed trades are legal and result in the update bank and the update wallet of the active player.
- **./Tests**: directory containing tests as a .json file pairs. For each test case n, there are two test files: n-in.json with given input, and n-out.json with expected output for that input.