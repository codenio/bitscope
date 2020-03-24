import setuptools

with open('DESCRIPTION.md', 'r') as readme:
  long_description = readme.read()

with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
      name='bitscope',
      version='0.0.1',
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