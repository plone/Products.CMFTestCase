#
# CMFTestCase interfaces
#

# $Id: interfaces.py,v 1.1 2005/01/02 19:27:34 shh42 Exp $

from Testing.ZopeTestCase.interfaces import *


class ICMFSecurity(IPortalSecurity):

    def loginAsPortalOwner():
        '''Logs in as the user owning the portal object.
           Use this when you need to manipulate the portal
           itself.
        '''

