from setuptools import setup, find_namespace_packages

setup(name='pyCliAddressBook',
      version='1.0.14',
      description='Personal assistant with command line interface',
      url='https://github.com/yuragoit/pyCliAddressBook',
      author='Yurii Skiter, Valerii Sydorenko, Dmytro Levoshko',
      author_email='contract@restriction.com',
      license='MIT',
      # packages=find_namespace_packages(),
      packages=['pyCliAddressBook', 'pyCliAddressBook.*'],
      # install_requires=['python-dateutil<=2.8.2',
      #                   'rich<=12.5.1', 'prompt-toolkit<=3.0.30', 'phonenumbers<=8.12.55'],
      # extras_require={'phonenumbers': ['phonenumbers<=8.12.50']},
      entry_points={'console_scripts': [
          'assistant=pyCliAddressBook.main:CLI']}
      )
