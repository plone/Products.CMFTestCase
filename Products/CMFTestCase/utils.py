"""Stop gap fix for abuse of ZTC.installProduct('Five') """

try:
    from zope.testing.cleanup import cleanUp
except ImportError:
    from Testing.ZopeTestCase.placeless import tearDown as cleanUp

# will appear soon in ZTC
def setDebugMode(mode):
    """
    Allows manual setting of Five's inspection of debug mode to allow for
    zcml to fail meaningfully
    """
    import Products.Five.fiveconfigure as fc
    fc.debug_mode=mode

def safe_load_site():
    """Load entire component architecture (w/ debug mode on)"""
    setDebugMode(1)
    from Products.Five import zcml
    zcml.load_site()
    setDebugMode(0)

def safe_load_site_wrapper(function):
    """Wrap function with a temporary loading of entire component architecture"""
    def wrapper(*args, **kw):
        safe_load_site()
        value = function(*args, **kw)
        cleanUp()
        import Products.Five.zcml as zcml
        zcml._initialized=False
        return value
    return wrapper
