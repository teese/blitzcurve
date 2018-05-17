from setuptools import setup, find_packages
from os import path

# grab the long_description from the readme file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="blitzcurve",
      author="Mark Teese",
      description="Time-resolved fluorescence anisotropy analysis.",
      long_description=long_description,
      url="https://github.com/teese/blitzcurve",
      classifiers=['Programming Language :: Python :: 3.6',
                   'License :: OSI Approved :: MIT License',
                   'Development Status :: 3 - Alpha',
                   'Intended Audience:: Science / Research',
                   'Topic :: Scientific/Engineering :: Chemistry',
                   'Topic :: Scientific/Engineering :: Physics',
                   ],
      install_requires=["pandas", "numpy", "matplotlib", "scipy"],
      version="0.0.2",
      packages=find_packages()
      )