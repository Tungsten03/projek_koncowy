# KRAQEN 1.0
----Kacper Rajewski Air Quality Environment----
The application was developed as a final project for postgraduate studies

The program requests data from the GIOS API and stores it in an SQLite database. 
The main functionality of the application focuses on analyzing the measurement data from air quality monitoring stations in Poland.



## Table of Contents

- [HowToRun](#HowToRun)
- [Tests](#Tests)
- [Documentation](#documentation)

- [Requirements](#Requirements)
- [License](#license)
- [Project Status](#project-status)
- [References](#references)
- [Contact](#contact)

## HowToRun
__MS Windows__ compiled version 1.0 located in:
https://github.com/Tungsten03/projek_koncowy/tree/tests/dist/Main

**OR**

Download source code listed below and run __Main.py__
__requirements__ to set up the virtual environment prepared using pip freeze
run: __pip install -r requirements.txt__

__Source code__:
Main.py
analyze_full.py
database
data_filter
utility
tests
**optional** [generated on app start] 
stations.db - for historical data

## Tests
testing module: unittest
Tests can be performed in app main menu (TESTY button)
or run the tests using the command: __python -m unittest discover -s tests__
Test coverage located in htmlcov

there are few 'simple' tests - I definitely see a potential for expanding my knowladge here, aware of the gaps.
Mocking the database is tricky - seems to work but not 100% sure

## Documentation
Documentation generated with sphinx module
download: https://github.com/Tungsten03/projek_koncowy/tree/tests/docs/_build/html
to open it localy
**Github Pages in progress** - a painfull loss for now

###Disclaimer
I do apologize for github repo mess - need to work on git more

