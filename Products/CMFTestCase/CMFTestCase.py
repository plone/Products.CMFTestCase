#
# CMFTestCase
#

# $Id$

from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import installProduct

from Testing.ZopeTestCase import Sandboxed
from Testing.ZopeTestCase import Functional
from Testing.ZopeTestCase import PortalTestCase

from setup import CMF15
from setup import CMF16
from setup import CMF20
from setup import CMF21
from setup import portal_name
from setup import portal_owner
from setup import default_products
from setup import default_base_profile
from setup import default_extension_profiles
from setup import default_user
from setup import default_password
from setup import setupCMFSite

from interfaces import ICMFTestCase
from interfaces import ICMFSecurity

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from warnings import warn

import setup
import utils


class CMFTestCase(PortalTestCase):
    '''Base test case for CMF testing'''

    __implements__ = (ICMFTestCase, ICMFSecurity,
                      PortalTestCase.__implements__)

    if setup.USELAYER:
        import layer
        layer = layer.ZCMLLayer

    def _portal(self):
        '''Returns the portal object for a test.'''
        try:
            return self.getPortal(1)
        except TypeError:
            return self.getPortal()

    def getPortal(self, called_by_framework=0):
        '''Returns the portal object to the setup code.

           DO NOT CALL THIS METHOD! Use the self.portal
           attribute to access the portal object from tests.
        '''
        if not called_by_framework:
            warn('Calling getPortal is not allowed, please use the '
                 'self.portal attribute.', UserWarning, 2)
        return getattr(self.app, portal_name)

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

