from setuptools import setup, find_packages
import os

version = '1.0.0dev'

setup(name='Products.CMFTestCase',
      version=version,
      description="Integration testing framework for CMF.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: CMF",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='cmf testing',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://cmf.org/products/cmftestcase',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
