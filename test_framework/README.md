# test_framework
## About
* Author   : Abel Gancsos
* Version  : v. 1.0.0

## Synopsis
This Python package is meant as a free and open source test framework that can be used for a wide range of Unit Tests built in Python.  The idea was to have a dynamic collection of Unit Tests, where no manual input is neccessary to update the Test Suite.  Then by running the main module of the package, all tests will be itterated and a final code coverage will be displayed.

## Assumptions
* There is a need for a lightweight and open source test framework
* The package will be used to test a wide range of applications
* The package will be ran against a range of different platforms
* The environment will be constantly updated.
* The Test Suite may take several hours to complete all tests.

## Requirements
* The package will run steps needed to validate applications.
* The package will be constantly updated.


## Constraints
* The environment must be updated dynamically.
* No manual input must be done to update the environment.

## Implementation Description
The package implementation is actually quite simple, it depends soley on reflection or more accurately introspection.  What happens is that the bootstrap component of the package iterates the modules within the different directories of the package, imports the classes within the module, and then stores in in a public collection within the bootstrap.  The reason that the classes are stored within the bootstrap is so that there's more control over the classes, higher chance of importing the modules, as well as enumeration.  The one caveat is that if the classes are cleared from the bootstrap, then access is no longer available.  The package then continues to create an instance of each concrete form of the TestCase object and adds it to the TestSuite.  Then when the TestSuite is invoked, it itterates through the collection of tests, invokes those in a safe way and adds the result to either a success collection or failure collection.  The test coverage is then calculated using the formula: (total success/(total success + total failure)) * 100.  

## Flags

## References
* https://stackoverflow.com/questions/11108628/python-dynamic-from-import
