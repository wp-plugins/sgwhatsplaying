from distutils.core import setup

setup(name='sgwhatsplaying',
      scripts=['sgwpupdate.py'],
      py_modules=['sgwpmpd'],
      packages=['sgpyutil'],

      version='1.1',
      url='http://www.moregruel.net/',
      description='Update WordPress plugin with song info',
      author='Steve Greenland',
      author_email='steveg@moregruel.net',
      classifiers=['License :: OSI Approved :: GNU General Public License (GPL)'],
      )
