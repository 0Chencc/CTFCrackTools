# Copyright (C) 2001,2002 Python Software Foundation
# email package unit tests

# The specific tests now live in Lib/email/test
from email.test.test_email import TestEncoders, suite
from test import test_support

def test_main():
    #This one doesn't work on Jython
    del TestEncoders.test_encode7or8bit

    s = suite()
    test_support.run_unittest(suite())

if __name__ == '__main__':
    test_main()
