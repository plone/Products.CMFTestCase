#
# Skeleton CMFTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFTestCase import CMFTestCase

CMFTestCase.installProduct('SomeProduct')
CMFTestCase.setupCMFSite()


class TestSomeProduct(CMFTestCase.CMFTestCase):

    def afterSetUp(self):
        pass

    def testSomething(self):
        # Test something
        self.assertEqual(1+1, 2)

            
if __name__ == '__main__':
    framework()
else:
    from unittest import TestSuite, makeSuite
    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestSomeProduct))
        return suite

