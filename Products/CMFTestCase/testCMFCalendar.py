#
# Tests a CMF product
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFTestCase.ctc import *

installProduct('CMFCalendar')
setupCMFSite(products=('CMFCalendar',))


class TestCalendar(CMFTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog

    def testToolsInstalled(self):
        self.failUnless(hasattr(self.portal, 'portal_calendar'))

    def testTypesInstalled(self):
        types = self.portal.portal_types.objectIds()
        self.failUnless('Event' in types)

    def testIndexesInstalled(self):
        try:
            self.catalog._catalog.getIndex('start')
        except KeyError:
            self.fail()

    def testCreateEvent(self):
        self.folder.invokeFactory('Event', id='lunch',
                                  start_date='2005-01-11 08:00',
                                  end_date='2005-01-12 14:00')

        r = self.catalog(start={'query': '2005-01-11', 'range': 'max'})

        self.assert_(r)
        self.assertEqual(r[0].getId, 'lunch')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCalendar))
    return suite

if __name__ == '__main__':
    framework()
