import unittest

import xmlrunner

from test import TestDummy


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDummy))
    return suite


if __name__ == "__main__":
    # Define the XMLTestRunner with output directory 'test-reports'
    runner = xmlrunner.XMLTestRunner(output='test-reports', verbosity=2)

    # Run the test suite using the XMLTestRunner
    runner.run(suite())
