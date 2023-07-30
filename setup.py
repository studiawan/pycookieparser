from setuptools import setup

setup(
    name='pycookieparser',
    version='0.0.1',
    description='A parser for binary cookie files',
    author='Hudan Studiawan',
    author_email='studiawan@gmail.com',
    url='https://github.com/studiawan/pycookieparser',
    packages=['pycookieparser'],
    entry_points={
        'console_scripts': [
            'pycookieparser = pycookieparser.pycookieparser:main',
        ]  
    },
    install_requires=['pytest', 'Sphinx'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
