#
# CMFTestCase interfaces
#

# $Id: interfaces.py,v 1.2 2005/02/25 11:02:21 shh42 Exp $

from Testing.ZopeTestCase.interfaces import *


class ICMFSecurity(IPortalSecurity):

    def loginAsPortalOwner():
        '''Logs in as the user owning the portal object.
           Use this when you need to manipulate the portal
           itself.
        '''

    def addProduct(name):
        '''Installs a product into the CMF site by executing
           its Extensions.Install.install method.
           This is alternative to passing a 'products'
           argument to setupCMFSite.
        '''

