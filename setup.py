from setuptools import setup, find_packages

version = '0.9.8'

setup(name='Products.CMFTestCase',
      version=version,
      description="Integration testing framework for CMF.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        #"Framework :: CMF",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='cmf testing',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://plone.org/products/cmftestcase',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
)
