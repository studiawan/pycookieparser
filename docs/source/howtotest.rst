Running tests
=============

To ensure your software functions as expected and maintain code quality, running tests is crucial. Follow these steps for effective test execution:

1. Navigating to the project directory

   Start by changing your working directory to the root directory of your project. This directory contains all project files and subdirectories.

   Open your terminal or command prompt and use the `cd` command to navigate to the root project directory::

      cd /path/to/your/project

   Replace ``/path/to/your/project`` with the actual path to your project's root directory.

2. Activate the Anaconda virtual environment:
   
   Before running the tool, ensure you activate the ``pycookieparser`` virtual environment using Anaconda. To do this, type the following command::

      conda activate pycookieparser

   Wait a few moments for the environment to activate. You'll know it's active when you see ``(pycookieparser)`` at the beginning of your terminal or command prompt line.

3. Executing tests with pytest

   Utilize the popular testing framework `pytest` for streamlined test execution. This framework simplifies writing and running tests.

   To run all tests in your project, use the following terminal command::

      pytest

   Pytest searches for test files within your project directory and its subdirectories. It automatically identifies and executes test functions.

4. Running specific test functions

   For targeted testing of specific functions within a module, `pytest` offers a focused approach.

   Suppose you have a test function named ``test_read_cookie_file`` in the module ``tests/test_pycookieparser.py``. Run this specific test using the following command::

      pytest tests/test_pycookieparser.py::test_read_cookie_file

   This command runs only the ``test_read_cookie_file`` test function within the specified module.

By adhering to these steps, you can successfully run tests for your project. Testing validates code correctness and detects potential issues early, contributing to software stability and reliability. Maintaining a comprehensive test suite is essential for long-term project maintainability.
