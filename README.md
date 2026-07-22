# pybinarycookie
iOS binary cookie parser.

# How to install

Clone the repository: 

`git clone https://github.com/studiawan/pycookieparser.git`

Then go to the root project directory, create a virtual environment, and activate it:

`python3 -m venv .venv`
`source .venv/bin/activate`

Install the package:

`pip install .`

For development (includes pytest, Sphinx):

`pip install -e ".[dev]"`

# How to run

To run the tool, you can type this command in the terminal:

`pycookieparser -i /path/to/cookie_file -t {txt,json,csv} -o /path/to/output_dir [--summary]`

For example:

`pycookieparser -i tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c -t json -o . --summary`

Or for batch directory processing:

`pycookieparser -d /path/to/directory -t json -o /path/to/output_dir --summary`

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