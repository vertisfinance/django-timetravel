from setuptools import setup


setup(
    name='django-timetravel',
    description='Full featured audit functionality for Django',
    version='0.1',
    install_requires=[
        'django >= 1.7'
    ],
    license='MIT',
    packages=['django_timetravel']
)
