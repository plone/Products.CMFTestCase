#
# Interface tests
#

# $Id: testInterfaces.py,v 1.1 2005/01/02 19:27:34 shh42 Exp $

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFTestCase import CMFTestCase
from Products.CMFTestCase.interfaces import *

from Interface.Verify import verifyObject


class TestCMFTestCase(CMFTestCase.CMFTestCase):

    _configure_portal = 0

    def getPortal(self):
        return None

    def testIProfiled(self):
        self.failUnless(verifyObject(IProfiled, self))

    def testIPortalTestCase(self):
        self.failUnless(verifyObject(IPortalTestCase, self))

    def testICMFSecurity(self):
        self.failUnless(verifyObject(ICMFSecurity, self))


class TestFunctionalTestCase(CMFTestCase.FunctionalTestCase):

    _configure_portal = 0

    def getPortal(self):
        return None

    def testIFunctional(self):
        self.failUnless(verifyObject(IFunctional, self))

    def testIProfiled(self):
        self.failUnless(verifyObject(IProfiled, self))

    def testIPortalTestCase(self):
        self.failUnless(verifyObject(IPortalTestCase, self))

    def testICMFSecurity(self):
        self.failUnless(verifyObject(ICMFSecurity, self))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCMFTestCase))
    suite.addTest(makeSuite(TestFunctionalTestCase))
    return suite

if __name__ == '__main__':
    framework()

