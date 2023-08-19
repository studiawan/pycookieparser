How to build documentation
===========================

To ensure your documentation is built correctly, you'll want to follow a series of steps that will guide you through the process. Below, you'll find a detailed walk-through that will help you effectively build your documentation.

.. note:: Make sure to activate your Anaconda virtual environment.

1. Navigate to the documentation directory.

   Before anything else, you'll need to ensure that you are in the correct directory where your documentation files are stored. In our case, the documentation is stored in the ``docs`` directory.

   To change to the ``docs`` directory, use the following command in your terminal or command prompt::

       cd docs

2. Clean up previously generated documentation.

   It's a good practice to clean up any previously generated documentation files. This ensures that you're starting fresh, without any leftover or outdated files that might interfere with your new build.

   To clean up the previous builds, run the following command::

       make clean

   This will remove any previous build outputs and allow you to start with a clean slate.

3. Build the documentation.

   Now that you're set up, you can proceed to build the documentation. This will generate the necessary HTML files and other resources required to view your documentation.

   To build the documentation, run the following command::

       make html

   Once the command completes, your documentation will be built and you can find the generated HTML files in the appropriate output directory (commonly named ``docs/build``). Find a file named ``index.html`` to go to the main page of the documentation.
