#
# CMFTestCase
#

# $Id: CMFTestCase.py,v 1.13 2004/09/04 21:47:48 shh42 Exp $

from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('MailHost', quiet=1)

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import time

from Testing.ZopeTestCase import installProduct
from Testing.ZopeTestCase import hasProduct
from Testing.ZopeTestCase import utils

portal_name = 'cmf'
portal_owner = 'portal_owner'
default_user = ZopeTestCase.user_name


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
        '''Use if you need to manipulate the portal itself.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)


class FunctionalTestCase(ZopeTestCase.Functional, CMFTestCase):
    '''Convenience class for functional unit testing'''


def setupCMFSite(portal_name=portal_name, quiet=0):
    '''Creates a CMF site.'''
    ZopeTestCase.utils.appcall(_setupCMFSite, portal_name, quiet)


def _setupCMFSite(app, portal_name, quiet):
    '''Creates a CMF site.'''
    if not hasattr(aq_base(app), portal_name):
        _optimize()
        start = time.time()
        if not quiet: ZopeTestCase._print('Adding CMF Site ... ')
        # Add user and log in
        app.acl_users._doAddUser(portal_owner, '', ['Manager'], [])
        user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
        newSecurityManager(None, user)
        # Add CMF site
        factory = app.manage_addProduct['CMFDefault']
        factory.manage_addCMFSite(portal_name, create_userfolder=1)
        # Log out and commit
        noSecurityManager()
        get_transaction().commit()
        if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-start,))


def _optimize():
    '''Reduces portal creation time.'''
    # Don't compile expressions on creation
    def __init__(self, text):
        self.text = text
    from Products.CMFCore.Expression import Expression
    Expression.__init__ = __init__
    # Don't clone actions but convert to list only
    def _cloneActions(self):
        return list(self._actions)
    from Products.CMFCore.ActionProviderBase import ActionProviderBase
    ActionProviderBase._cloneActions = _cloneActions
    # Don't setup 'index_html' in Members folder
    def setupMembersFolder(self, p):
        p.manage_addPortalFolder('Members')
    from Products.CMFDefault.Portal import PortalGenerator
    PortalGenerator.setupMembersFolder = setupMembersFolder

