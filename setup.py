from setuptools import setup, find_packages
import os

version = "0.1"

setup(name='collective.ptg.dropbox',
      version=version,
      description="Add on collective.plonetruegallery to aggregate "
                  "from dropbox",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2"
        ],
      keywords='gallery dropbox ',
      author='Espen M-N',
      author_email='espen@medialog.no',
      url='http://www.plone.org/products/plone-true-gallery',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.ptg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          'dropbox',
          'collective.plonetruegallery'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """
)
