#
# CMFTestCase
#

# $Id: CMFTestCase.py,v 1.17 2004/12/26 21:50:27 shh42 Exp $

from Testing import ZopeTestCase

from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import utils

from setup import portal_name
from setup import portal_owner
from setup import default_products
from setup import default_user
from setup import default_password
from setup import setupCMFSite

from AccessControl.SecurityManagement import newSecurityManager


class CMFTestCase(ZopeTestCase.PortalTestCase):
    '''Base test case for CMF testing

       __implements__ = (IPortalTestCase, ISimpleSecurity, IExtensibleSecurity)

       See the ZopeTestCase docs for more
    '''

    def getPortal(self):
        '''Returns the portal object to the bootstrap code.

           Do not call this method! Use the self.portal
           attribute to access the portal object from tests.
        '''
        return self.app[portal_name]

    def createMemberarea(self, member_id):
        '''Creates a minimal memberarea.'''
        # Owner
        uf = self.portal.acl_users
        user = uf.getUserById(member_id)
        if user is None:
            raise ValueError, 'Member %s does not exist' % member_id
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        # Home folder
        membership = self.portal.portal_membership
        members = membership.getMembersFolder()
        members.manage_addPortalFolder(member_id)
        folder = membership.getHomeFolder(member_id)
        folder.changeOwnership(user)
        folder.__ac_local_roles__ = None
        folder.manage_setLocalRoles(member_id, ['Owner'])

    def loginAsPortalOwner(self):
        '''Use this when you need to manipulate the portal itself.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)


class FunctionalTestCase(ZopeTestCase.Functional, CMFTestCase):
    '''Base class for functional CMF tests'''

