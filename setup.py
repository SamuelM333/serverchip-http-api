from setuptools import setup

setup(name='ServerhipAPI',
      version='1.0',
      description='Serverchip API made with Python Eve',
      author='Samuel Murillo',
      author_email='samuelmurillo333@gmail.com',
      url='https://github.com/Serverchip/API',
      install_requires=[
           'Eve==0.6.4',
           'bcrypt==3.1.2',
           'pytest==3.0.5'
           ]
      )
