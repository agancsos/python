#!/bin/python
import os;
import sys;
sys.path.insert(0, './src');
from framework import *;
from bootstrapservice import *;
Bootstraper.bootstrap();
Bootstraper.bootstrap("./tests");

## Starts the test suite
if __name__ == "__main__":
    session = TestSuite();
    session.run();
    pass;
