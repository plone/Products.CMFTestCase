#
# CMFTestCase setup
#

# $Id: setup.py,v 1.1 2004/09/12 13:53:45 shh42 Exp $

from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('MailHost', quiet=1)

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import time

portal_name = 'cmf'
portal_owner = 'portal_owner'
default_user = ZopeTestCase.user_name


def setupCMFSite(id=portal_name, quiet=0):
    '''Creates a CMF site.'''
    ZopeTestCase.utils.appcall(_setupCMFSite, id, quiet)


def _setupCMFSite(app, id, quiet):
    '''Creates a CMF site.'''
    if not hasattr(aq_base(app), id):
        _optimize()
        start = time.time()
        if not quiet: ZopeTestCase._print('Adding CMF Site ... ')
        # Add user and log in
        app.acl_users._doAddUser(portal_owner, '', ['Manager'], [])
        user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
        newSecurityManager(None, user)
        # Add CMF site
        factory = app.manage_addProduct['CMFDefault']
        factory.manage_addCMFSite(id, create_userfolder=1)
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

