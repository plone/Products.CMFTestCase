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

try:
    from Products.CMFCore.interfaces import ISiteRoot
except ImportError:
    pass
else:
    class ICMFTestSiteRoot(ISiteRoot):
        """Marker interface for the object which serves as the root of a site.
           This will automatically and should only be provided during tests runs.
        """
