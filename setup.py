from setuptools import setup

setup(name='ServerhipAPI',
      version='1.0',
      description='Serverchip API made with Python Eve',
      author='Samuel Murillo',
      author_email='samuelmurillo333@gmail.com',
      url='https://github.com/Serverchip/API',
      install_requires=[
          'bcrypt==3.1.2'
          'Eve==0.7.4'
          'pytest==3.0.5',
          'Flask-SocketIO==2.9.2',
          'eventlet==0.21.0'
      ]
      )
