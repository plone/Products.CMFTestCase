#
# CMFTestCase interfaces
#

# $Id$

from Testing.ZopeTestCase.interfaces import *


class ICMFSecurity(IPortalSecurity):

    def loginAsPortalOwner():
        '''Logs in as the user owning the portal object.
           Use this when you need to manipulate the portal
           itself.
        '''


class ICMFTestCase(IPortalTestCase):

    def addProduct(name):
        '''Installs a product into the CMF site by executing
           its 'Extensions.Install.install' function.
           This is an alternative to passing a 'products'
           argument to 'setupCMFSite'.
        '''

