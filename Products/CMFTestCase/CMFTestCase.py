#
# CMFTestCase
#

# $Id: CMFTestCase.py,v 1.4 2003/11/27 19:44:22 shh42 Exp $

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

portal_name  = 'cmf'
portal_owner = 'portal_owner'
default_user = ZopeTestCase.user_name


class CMFTestCase(ZopeTestCase.PortalTestCase):
    '''Base test case for CMF testing

       __implements__ = (IPortalTestCase, ISimpleSecurity, IExtensibleSecurity)

       See the ZopeTestCase docs for more
    '''

    def getPortal(self):
        '''Returns the portal object.'''
        return self.app[portal_name]

    def createMemberarea(self, member_id):
        '''Creates a minimal memberarea.'''
        # Owner 
        uf = self.portal.acl_users
        user = uf.getUserById(member_id)
        if user is None:
            raise ValueError, 'Member %s does not exist' % member_id
        user = user.__of__(uf)
        # Home folder
        membership = self.portal.portal_membership
        members = membership.getMembersFolder()
        members.manage_addPortalFolder(member_id)
        folder = membership.getHomeFolder(member_id)
        folder.changeOwnership(user)
        folder.__ac_local_roles__ = None
        folder.manage_setLocalRoles(member_id, ['Owner'])


def setupCMFSite(id=portal_name, quiet=0):
    '''Creates a CMF site.'''
    app = ZopeTestCase.app()
    _setupCMFSite(app, id, quiet)
    ZopeTestCase.close(app)


def setupCMFSkins(id=portal_name, quiet=0):
    '''Creates the default skin directories.'''
    app = ZopeTestCase.app()
    _setupCMFSkins(app, id, quiet)
    ZopeTestCase.close(app)


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
    # Don't setup default skins
    def setupDefaultSkins(self, p):
        pass
    from Products.CMFDefault.Portal import PortalGenerator
    PortalGenerator.setupDefaultSkins = setupDefaultSkins


def _setupCMFSite(app, id=portal_name, quiet=0):
    '''Creates a CMF site.'''
    if not hasattr(aq_base(app), id):
        _optimize()
        _start = time.time()
        if not quiet: ZopeTestCase._print('Adding CMF Site ... ')
        # Add user and log in
        app.acl_users._doAddUser(portal_owner, '', ['Manager'], [])
        user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
        newSecurityManager(None, user)
        # Add CMF site
        factory = app.manage_addProduct['CMFDefault']
        factory.manage_addCMFSite(id, '', create_userfolder=1)
        # Log out and commit
        noSecurityManager()
        get_transaction().commit()
        if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))


# Save away before _optimize patches over it
from Products.CMFDefault.Portal import PortalGenerator as _PortalGenerator
_setupDefaultSkins = _PortalGenerator.setupDefaultSkins


def _setupCMFSkins(app, id=portal_name, quiet=0):
    '''Creates the default skin directories.'''
    portal = app[id]
    if not hasattr(aq_base(portal.portal_skins), 'zpt_content'):
        _start = time.time()
        if not quiet: ZopeTestCase._print('Adding CMF Skins ... ')
        # Log in
        user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
        newSecurityManager(None, user)
        # Add CMF skins
        _setupDefaultSkins(_PortalGenerator(), portal)
        # Log out and commit
        noSecurityManager()
        get_transaction().commit()
        if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

