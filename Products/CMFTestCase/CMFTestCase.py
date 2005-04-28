#
# CMFTestCase
#

# $Id$

from Testing.ZopeTestCase import PortalTestCase
from Testing.ZopeTestCase import Functional

from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import utils

from setup import portal_name
from setup import portal_owner
from setup import default_products
from setup import default_user
from setup import default_password
from setup import setupCMFSite

from interfaces import ICMFSecurity
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager


class CMFTestCase(PortalTestCase):
    '''Base test case for CMF testing'''

    __implements__ = (ICMFSecurity,
                      PortalTestCase.__implements__)

    def getPortal(self):
        '''Returns the portal object to the setup code.

           DO NOT CALL THIS METHOD! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return self.app[portal_name]

    def createMemberarea(self, name):
        '''Creates a minimal memberarea.'''
        uf = self.portal.acl_users
        user = uf.getUserById(name)
        if user is None:
            raise ValueError, 'Member %s does not exist' % name
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        pm = self.portal.portal_membership
        members = pm.getMembersFolder()
        members.manage_addPortalFolder(name)
        folder = pm.getHomeFolder(name)
        folder.changeOwnership(user)
        folder.__ac_local_roles__ = None
        folder.manage_setLocalRoles(name, ['Owner'])

    def loginAsPortalOwner(self):
        '''Use this if - AND ONLY IF - you need to manipulate the
           portal object itself.
        '''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

    def addProduct(self, name):
        '''Installs a product into the CMF site.'''
        sm = getSecurityManager()
        self.loginAsPortalOwner()
        try:
            installed = getattr(self.portal, '_installedProducts', {})
            if not installed.has_key(name):
                exec 'from Products.%s.Extensions.Install import install' % name
                install(self.portal)
                self._refreshSkinData()
        finally:
            setSecurityManager(sm)


class FunctionalTestCase(Functional, CMFTestCase):
    '''Base class for functional CMF tests'''

    __implements__ = (Functional.__implements__,
                      CMFTestCase.__implements__)

