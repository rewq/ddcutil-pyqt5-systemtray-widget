from setuptools import setup, find_packages

setup(name='DDCUtil-Tray',
      version='0.0.1',
      description='Shows how to use setup.py',
      url='https://www.scrygroup.com',
      author='Rewq',
      license='GPLv2',
      packages=['ddctray'],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python'
      ],
      keywords='tutorial',
      include_package_data = True,
      entry_points = {
        "console_scripts": [        # command-line executables to expose
            "ddctray = ddctray.tray:run",
        ]
      },
      install_requires=[
        'PyQt5',
      ]
)
