#
# CMFTestCase setup
#

# $Id$

from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('CMFUid', quiet=1)
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('ZCTextIndex', quiet=1)

# Check for Zope 2.9 or above
try:
    import zope.testing.testrunner
except ImportError:
    USELAYER = 0
else:
    USELAYER = 1

# Check for CMF 1.5 or above
try:
    from Products.CMFCore import permissions
except ImportError:
    CMF15 = 0
else:
    CMF15 = 1

# Check for CMF 1.6 or above
try:
    from Products.CMFDefault import factory
except ImportError:
    CMF16 = 0
else:
    CMF16 = 1
    ZopeTestCase.installProduct('DCWorkflow')
    # For BBB
    if not USELAYER:
        ZopeTestCase.installProduct('Five')

# Check for CMF 2.0 or above
try:
    from Products.CMFDefault.utils import translate
except ImportError:
    CMF20 = 0
else:
    CMF20 = 1

# Check for CMF 2.1 or above
try:
    from Products.CMFDefault.utils import getBrowserCharset
except ImportError:
    CMF21 = 0
else:
    CMF21 = 1

from Globals import PersistentMapping
from Testing.ZopeTestCase import transaction
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
from time import time

portal_name = 'cmf'
portal_owner = 'portal_owner'
default_products = ()
default_user = ZopeTestCase.user_name
default_password = ZopeTestCase.user_password

# CMF 1.6
default_base_profile = 'CMFDefault:default'
default_extension_profiles = ()

if CMF20:
    default_base_profile = 'Products.CMFDefault:default'


def setupCMFSite(id=portal_name, products=default_products, quiet=0,
                 base_profile=default_base_profile,
                 extension_profiles=default_extension_profiles):
    '''Creates a CMF site and/or installs products into it.'''
    PortalSetup(id, products, quiet, base_profile, extension_profiles).run()

if USELAYER:
    import utils
    setupCMFSite = utils.safe_load_site_wrapper(setupCMFSite)


class PortalSetup:
    '''Creates a CMF site and/or installs products into it.'''

    def __init__(self, id, products, quiet, base_profile, extension_profiles):
        self.id = id
        self.products = products
        self.quiet = quiet
        self.base_profile = base_profile
        self.extension_profiles = tuple(extension_profiles)

    def run(self):
        self.app = self._app()
        try:
            uf = self.app.acl_users
            if uf.getUserById(portal_owner) is None:
                # Add portal owner
                uf.userFolderAddUser(portal_owner, default_password, ['Manager'], [])
            if not hasattr(aq_base(self.app), self.id):
                # Log in and create site
                self._login(uf, portal_owner)
                self._optimize()
                self._setupCMFSite()
            if hasattr(aq_base(self.app), self.id):
                # Log in as portal owner
                self._login(uf, portal_owner)
                self._setupProducts()
        finally:
            self._abort()
            self._close()
            self._logout()

    def _setupCMFSite(self):
        '''Creates the CMF site.'''
        # Starting with CMF 1.6 site creation is based on GenericSetup
        if CMF16:
            self._setupCMFSite_genericsetup()
        else:
            self._setupCMFSite_portalgenerator()

    def _setupCMFSite_genericsetup(self):
        '''Creates a CMF site with GenericSetup.'''
        start = time()
        if self.base_profile != default_base_profile:
            self._print('Adding CMF Site (%s) ... ' % self.base_profile)
        else:
            self._print('Adding CMF Site ... ')
        # Add CMF site
        factory.addConfiguredSite(self.app, self.id, snapshot=0,
                                  profile_id=self.base_profile,
                                  extension_ids=self.extension_profiles)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))
        # Report applied expension profiles
        if (self.extension_profiles and
            self.extension_profiles != default_extension_profiles):
            s = len(self.extension_profiles) != 1 and 's' or ''
            self._print('  Applied extension profile%s %s.\n' %
                        (s, ', '.join(self.extension_profiles)))

    def _setupCMFSite_portalgenerator(self):
        '''Creates a CMF site with PortalGenerator.'''
        start = time()
        self._print('Adding CMF Site ... ')
        from Products.CMFDefault.Portal import manage_addCMFSite
        manage_addCMFSite(self.app, self.id, create_userfolder=1)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))

    def _setupProducts(self):
        '''Installs products into the CMF site.'''
        portal = self.app[self.id]
        if not hasattr(portal, '_installedProducts'):
            portal._installedProducts = PersistentMapping()
            self._commit()
        for product in self.products:
            if not portal._installedProducts.has_key(product):
                start = time()
                self._print('Adding %s ... ' % (product,))
                exec 'from Products.%s.Extensions.Install import install' % product
                install(portal)
                portal._installedProducts[product] = 1
                self._commit()
                self._print('done (%.3fs)\n' % (time()-start,))

    def _optimize(self):
        '''Applies optimizations to the PortalGenerator.'''
        _optimize()

    def _app(self):
        '''Opens a ZODB connection and returns the app object.'''
        return ZopeTestCase.app()

    def _close(self):
        '''Closes the ZODB connection.'''
        ZopeTestCase.close(self.app)

    def _login(self, uf, name):
        '''Logs in as user 'name' from user folder 'uf'.'''
        user = uf.getUserById(name).__of__(uf)
        newSecurityManager(None, user)

    def _logout(self):
        '''Logs out.'''
        noSecurityManager()

    def _commit(self):
        '''Commits the transaction.'''
        transaction.commit()

    def _abort(self):
        '''Aborts the transaction.'''
        transaction.abort()

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
    # The site creation code is not needed anymore in CMF >= 1.6
    # as it is now based on GenericSetup
    if not CMF16:
        # Don't setup 'index_html' in Members folder
        def setupMembersFolder(self, p):
            p.manage_addPortalFolder('Members')
        from Products.CMFDefault.Portal import PortalGenerator
        PortalGenerator.setupMembersFolder = setupMembersFolder

