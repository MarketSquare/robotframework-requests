Introduction
============

RequestsLibrary is a [Robot Framework](http://code.google.com/p/robotframework/)
test library that uses the [Requests](https://github.com/kennethreitz/requests) HTTP client. 


Usage
=====

As I haven't published this on PyPI yet you will need to clone this repository. 
Then either add the src directory to your PYTHONPATH or manually specify it in
the pybot commandline argument.

The following command will run the tests that I have written using Robot Framework

    pybot -P robotframework-requests/src robotframework-requests/tests
