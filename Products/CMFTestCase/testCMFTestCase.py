#
# Tests the CMFTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFTestCase import CMFTestCase
from Acquisition import aq_base

CMFTestCase.setupCMFSite()

default_user = CMFTestCase.default_user


class TestCMFTestCase(CMFTestCase.CMFTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership

    def testDefaultMemberarea(self):
        self.assertEqual(self.folder.getOwner().getId(), default_user)
        self.assertEqual(self.folder.get_local_roles_for_userid(default_user), ('Owner',))
        self.failIf(hasattr(aq_base(self.folder), 'index_html'))

    def testCreateMemberarea(self):
        self.membership.addMember('user2', 'secret', [], [])
        self.createMemberarea('user2')
        home = self.membership.getHomeFolder('user2')
        self.assertEqual(home.getOwner().getId(), 'user2')
        self.assertEqual(home.get_local_roles_for_userid('user2'), ('Owner',))
        self.assertEqual(home.get_local_roles_for_userid(default_user), ())
        self.failIf(hasattr(aq_base(home), 'index_html'))


if __name__ == '__main__':
    framework()
else:
    from unittest import TestSuite, makeSuite
    def test_suite():
        suite = TestSuite()
        suite.addTest(makeSuite(TestCMFTestCase))
        return suite

