import setuptools

from distutils.util import convert_path

try:
  with open('DESCRIPTION.md', 'r') as readme:
    long_description = readme.read()
except:
  long_description = """# bitscope

**bitscope** is a comprehensive library for programming and data collection from Bitscope Micro.

It is a python wrapper for **bitlib** package installed using **bitscope-library_2.0.FE26B** and **python-bindings-2.0-DC01L**"""


with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

pkg_ns = {}

ver_path = convert_path('bitscope/metadata.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_ns)

setuptools.setup(
      name='bitscope',
      version=pkg_ns['__version__'],
      description='python package for bitscope micro',
      url='https://github.com/codenio/bitscope',
      author='Aananth K',
      author_email='aananthraj1995@gmail.com',
      license='GPL-3.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=requirements
)