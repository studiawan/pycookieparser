from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pycookieparser',
    version='0.0.2',
    description='A parser for binary cookie files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hudan Studiawan',
    author_email='studiawan@gmail.com',
    url='https://github.com/studiawan/pycookieparser',
    packages=['pycookieparser'],
    entry_points={
        'console_scripts': [
            'pycookieparser = pycookieparser.pycookieparser:main',
        ]  
    },
    python_requires='>=3.10',
    install_requires=[],
    extras_require={
        'dev': ['pytest', 'Sphinx', 'sphinx-rtd-theme'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Security',
        'Topic :: System :: Forensics',
    ],
)
