
CMFTestCase Readme

    CMFTestCase is a thin layer on top of the ZopeTestCase package. It has
    been developed to simplify testing of CMF-based applications and products.


    The CMFTestCase package provides:

        - The function 'installProduct' to install a Zope product into the 
          test environment.

        - The function 'setupCMFSite' to create a CMF portal in the test db.

        - The 'CMFTestCase' base class of which to derive your unit test cases.

        - The 'FunctionalTestCase' base class of which to derive your test 
          cases for functional (integration) tests.

        - The 'utils' module known from the ZopeTestCase package.


    Example CMFTestCase::

        from Products.CMFTestCase import CMFTestCase

        CMFTestCase.installProduct('SomeProduct')
        CMFTestCase.setupCMFSite()

        class TestSomething(CMFTestCase.CMFTestCase):

            def afterSetup(self):
                self.folder.invokeFactory('Document', 'doc')

            def testEditDocument(self):
                self.folder.doc.edit(text_format='plain', text='data')
                self.assertEqual(self.folder.doc.EditableBody(), 'data')


    Please see the docs of the ZopeTestCase package, especially those 
    of the PortalTestCase class. 

    Look at the example tests in this directory to get an idea of how 
    to use the CMFTestCase package.

    Copy testSkeleton.py to start your own tests.

