How to run the pycookieparser
==================================

The pycookieparser tool allows you to parse and analyze cookie files. To use this tool, you'll need to run a specific command in the terminal. Here's a step-by-step guide to help you do that:

1. Open the terminal or command prompt:
   
   - **Windows**: Press ``Windows + R``, type ``cmd``, and hit Enter.
   - **Mac**: Press ``Command + Space``, type ``Terminal``, and hit Enter.
   - **Linux**: Depending on your distribution, you can usually find the terminal in your applications menu or use a shortcut like ``Ctrl + Alt + T``.

2. Activate the Anaconda virtual environment:
   
   Before running the tool, ensure you activate the ``pycookieparser`` virtual environment using Anaconda. To do this, type the following command::

      conda activate pycookieparser

   Wait a few moments for the environment to activate. You'll know it's active when you see ``(pycookieparser)`` at the beginning of your terminal or command prompt line.

3. Navigate to the directory of the tool (if required):

   If the ``pycookieparser`` tool isn't globally accessible, you might need to navigate to its directory using the ``cd`` command. For example::

      cd path/to/pycookieparser_directory

4. Run the tool:

   To run the tool, you'll need to type the following command, replacing ``/path/to/cookie_file`` with the actual path to your cookie file::

      pycookieparser /path/to/cookie_file

   .. note:: The path can be either absolute (starting from the root directory) or relative (starting from the current directory).

5. Example:

   If you have a cookie file named ``fdda2f81cc0b838dc00e3050b14da7ef2d835f3c`` inside a directory called ``tests``, you would run::

      pycookieparser tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c

6. Wait for the tool to process:

   After entering the command, the tool will process the cookie file and display the results. Follow any additional on-screen instructions if provided.
