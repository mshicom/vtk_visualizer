from setuptools import setup
import os.path

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
    long_description = f.read()

setup(name = 'vtk_visualizer',
      version = '0.9.0',
      author = "Oystein Skotheim",
      author_email = "oystein.skotheim@sintef.no",
      maintainer = 'Oystein Skotheim',
      url = 'http://www.edge.no/wiki/Python_VTK',
      download_url = 'https://bitbucket.org/oskotheim/vtk_visualizer',
      description = "Easy 3D visualization of point clouds and geometric primitives",  
      long_description = long_description,
      packages = ['vtk_visualizer'],
      install_requires = ['python_qt_binding', 'vtk'],
      license = 'BSD',
      platforms = 'any',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Visualization'
          ],          
      )