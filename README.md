# pybinarycookie
iOS binary cookie parser.

# How to install

Create Anaconda virtual environment and activate it:

`conda create --name pycookieparser`
`conda activate pycookieparser`

Clone the repository: 

`git clone https://github.com/studiawan/pycookieparser.git`

Then go to root project directory, and run: 

`pip install .`

# How to run

To run the tool, you can type this command in the terminal:

`pycookieparser /path/to/cookie_file`

For example:

`pycookieparser tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c`

# How to run tests

Change directory to the root project directory and then run:

`pytest`

If you want to run a specific function of the module, namely `test_read_cookie_file`:

`pytest tests/test_pycookieparser.py::test_read_cookie_file`

# How to build docs

Change to `docs` directory:

`cd docs`
format 
Clean up the previous generated documentation:

`make clean`

Build the documentation:

`make html`