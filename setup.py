"""Integrates pyslurp into shell and creates basic configs"""
from distutils.core import setup

from post_install import post_install


setup(name='PySlurp',
      version='0.1',
      description='Python Remote Variable Loader',
      author='MaibornWolff',
      url='https://www.maibornwolff.de',
      packages=["configuration",
                "configuration.keys",
                "configuration.templates",
                "exporters",
                "sources",
                "sources.gitlab"
                ],
      install_requires=["click==8.0.1", "python-gitlab==2.9.0"],
      entry_points={
          'console_scripts': [
              '_pyslurp = _pyslurp:cli',
          ],
      }
      )

post_install()
print("bla")
