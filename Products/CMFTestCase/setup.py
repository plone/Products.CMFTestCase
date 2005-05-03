#
# CMFTestCase setup
#

# $Id$

from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('ZCTextIndex', quiet=1)

from PersistentMapping import PersistentMapping
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import time

portal_name = 'cmf'
portal_owner = 'portal_owner'
default_products = ()
default_user = ZopeTestCase.user_name
default_password = ZopeTestCase.user_password


def setupCMFSite(id=portal_name, products=default_products, quiet=0):
    '''Creates a CMF site and/or installs products into it.'''
    PortalSetup(id, products, quiet).run()


class PortalSetup:
    '''Creates a CMF site and/or installs products into it.'''

    def __init__(self, id=portal_name, products=default_products, quiet=0):
        self.id = id
        self.products = products
        self.quiet = quiet

    def run(self):
        self.app = ZopeTestCase.app()
        try:
            uf = self.app.acl_users
            if not hasattr(aq_base(self.app), self.id):
                # Add portal owner and log in
                uf.userFolderAddUser(portal_owner, 'secret', ['Manager'], [])
                user = uf.getUserById(portal_owner).__of__(uf)
                newSecurityManager(None, user)
                self._optimize()
                self._setupCMFSite()
            if hasattr(aq_base(self.app), self.id):
                # Log in as portal owner
                user = uf.getUserById(portal_owner).__of__(uf)
                newSecurityManager(None, user)
                self._setupProducts()
        finally:
            noSecurityManager()
            get_transaction().abort()
            ZopeTestCase.close(self.app)

    def _setupCMFSite(self):
        '''Creates the CMF site.'''
        start = time.time()
        self._print('Adding CMF Site ... ')
        # Add CMF site
        factory = self.app.manage_addProduct['CMFDefault']
        factory.manage_addCMFSite(self.id, create_userfolder=1)
        self._commit()
        self._print('done (%.3fs)\n' % (time.time()-start,))

    def _setupProducts(self):
        '''Installs products into the CMF site.'''
        portal = self.app[self.id]
        if not hasattr(portal, '_installedProducts'):
            portal._installedProducts = PersistentMapping()
        for product in self.products:
            if not portal._installedProducts.has_key(product):
                start = time.time()
                self._print('Adding %s ... ' % (product,))
                exec 'from Products.%s.Extensions.Install import install' % product
                install(portal)
                portal._installedProducts[product] = 1
                self._commit()
                self._print('done (%.3fs)\n' % (time.time()-start,))

    def _optimize(self):
        '''Applies optimizations to the PortalGenerator.'''
        _optimize()

    def _commit(self):
        '''Commits the transaction.'''
        get_transaction().commit()

    def _print(self, msg):
        '''Prints msg to stderr.'''
        if not self.quiet:
            ZopeTestCase._print(msg)


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

