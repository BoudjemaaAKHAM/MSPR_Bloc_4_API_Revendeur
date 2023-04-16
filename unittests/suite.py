import unittest

import xmlrunner

from test import TestDummy


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDummy))
    runner = xmlrunner.XMLTestRunner(output='test-reports', verbosity=2)
    runner.run(suite())
    return suite


