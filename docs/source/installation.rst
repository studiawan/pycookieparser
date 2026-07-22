Installation 
============

Prerequisites
---------------
Ensure you have the following installed:

- Python 3.10 or higher
- Git

Steps
------

1. Clone the ``pycookieparser`` repository

   In your terminal, navigate to a directory where you'd like to clone the repository. Execute the following command to clone the ``pycookieparser`` repository::
      
        git clone https://github.com/studiawan/pycookieparser.git

2. Navigate to the root project directory:

   After cloning, you'll have a new directory named ``pycookieparser``. Change to this directory with::
      
        cd pycookieparser

3. Create a virtual environment
   
   Create a Python virtual environment using the built-in ``venv`` module::
      
        python3 -m venv .venv

4. Activate the virtual environment
   
   Activate the virtual environment:

   - **Mac/Linux**::

        source .venv/bin/activate

   - **Windows**::

        .venv\Scripts\activate

   You'll know it's active when you see ``(.venv)`` at the beginning of your terminal prompt.

5. Install the package
   
   Now that you're in the root project directory with the virtual environment active, install the package using::
      
        pip install .

   For development (includes pytest, Sphinx, and sphinx-rtd-theme)::

        pip install -e ".[dev]"

6. Verify installation (optional):
   
   You can check if the package is successfully installed in your virtual environment using::
      
        pip list
      
   Look for ``pycookieparser`` in the list to confirm.
   
   In addition, run ``pycookieparser -h`` command on your terminal. It should display the CLI usage options including ``-i/--input_path``, ``-d/--directory``, ``-t/--output_type``, and ``-o/--output_path``.

7. Completion

   You have successfully installed the ``pycookieparser`` package in your virtual environment.

Remember, every time you need to use this package, ensure that you activate the virtual environment using ``source .venv/bin/activate``.
