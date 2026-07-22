How to run the pycookieparser
==================================

The pycookieparser tool allows you to parse and analyze cookie files. To use this tool, you'll need to run a specific command in the terminal. Here's a step-by-step guide to help you do that:

1. Open the terminal or command prompt:
   
   - **Windows**: Press ``Windows + R``, type ``cmd``, and hit Enter.
   - **Mac**: Press ``Command + Space``, type ``Terminal``, and hit Enter.
   - **Linux**: Depending on your distribution, you can usually find the terminal in your applications menu or use a shortcut like ``Ctrl + Alt + T``.

2. Activate the virtual environment:
   
   Before running the tool, ensure you activate the ``pycookieparser`` virtual environment. To do this, type the following command:

   - **Mac/Linux**::

      source .venv/bin/activate

   - **Windows**::

      .venv\Scripts\activate

3. Navigate to the directory of the tool (if required):

   If the ``pycookieparser`` tool isn't globally accessible, you might need to navigate to its directory using the ``cd`` command. For example::

      cd path/to/pycookieparser_directory

4. Command Line Options:

   The ``pycookieparser`` CLI supports the following arguments:

   - ``-i``, ``--input_path``: Path to a single binary cookie file to parse.
   - ``-d``, ``--directory``: Path to a directory for batch processing all cookie files within it.
   - ``-t``, ``--output_type``: Output format. Options are ``json``, ``csv``, or ``txt``. *(Required)*
   - ``-o``, ``--output_path``: Output directory path where parsed results will be saved. *(Required)*
   - ``--summary``: *(Optional)* Print a statistical summary of parsed cookies to the console.

   .. note:: Either ``-i/--input_path`` or ``-d/--directory`` must be provided, but not both at the same time. Both ``-t/--output_type`` and ``-o/--output_path`` are required arguments.

5. Examples:

   **Parsing a single cookie file:**

   To parse a cookie file named ``fdda2f81cc0b838dc00e3050b14da7ef2d835f3c`` inside the ``tests`` directory and save output as JSON in the current directory (``.``)::

      pycookieparser -i tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c -t json -o .

   **Parsing a single cookie file with summary statistics:**:

      pycookieparser -i tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c -t json -o . --summary

   **Batch processing a directory:**

   To parse all cookie files in a directory ``dataset`` and output CSV files to ``dist``::

      pycookieparser -d dataset -t csv -o dist --summary

6. Wait for the tool to process:

   After entering the command, the tool will process the cookie file, save the output file in the specified output directory, and optionally display summary statistics.

