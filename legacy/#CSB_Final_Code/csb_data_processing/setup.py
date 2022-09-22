from setuptools import setup

setup(name='csb_data_processing',
      version='0.1',
      description='csb processing scripts',
      url='https://github.com/csb-comren/data_processing/',
      author='Khaleel Arfeen',
      author_email='k.a@unb.ca',
      license='MIT',
      packages=['csb_data_processing'],
      install_requires=[
          'requests-toolbelt',
          'Pydap',
          'gsw==3.0.6',
      ],
      zip_safe=False)