#
# CMFTestCase
#

# $Id: CMFTestCase.py,v 1.23 2005/02/11 14:58:47 shh42 Exp $

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
from AccessControl.SecurityManagement import newSecurityManager


class CMFTestCase(PortalTestCase):
    '''Base test case for CMF testing'''

    __implements__ = (ICMFSecurity,
                      PortalTestCase.__implements__)

    def getPortal(self):
        '''Returns the portal object to the setup code.

           Do not call this method! Use the self.portal
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
        '''Use this when you need to manipulate the portal itself.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)


class FunctionalTestCase(Functional, CMFTestCase):
    '''Base class for functional CMF tests'''

    __implements__ = (Functional.__implements__,
                      CMFTestCase.__implements__)

