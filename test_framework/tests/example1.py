import os;
import sys;
sys.path.append("../src");
from framework import *;
from testcase import *;
class ExampleTestCase(TestCase):
    def invoke(self):
        assert(1==1);
        pass;
    pass;

if __name__ == "__main__":
    test1 = ExampleTestCase();
    test_run = TestRun(test1);
    test_run.run();
    print(Status.get_name(test_run.status));
