#!/usr/bin/env python3
###############################################################################
# Name        : unittest.py                                                   #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Practicing for the AWS exam.                                  #
###############################################################################
class UnitTest:
    expected=None;printed=None;
    def __init__(self, expected, printed=False):
        self.expected = expected; self.printed = printed;
    def on_invoke(self, args): raise NotImplemented();
    def invoke(self, args):
        try:
            result = self.on_invoke(args);
            if self.printed: print(result);
            assert result == self.expected;
            return True;
        except Exception as ex:
            print(ex);
            return False;
