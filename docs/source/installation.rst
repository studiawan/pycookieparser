Installation 
============

Prerequisites
---------------
Ensure you have the following installed:

- Anaconda or Miniconda
- Git

Steps
------

1. Create an Anaconda virtual environment
   
   Open your terminal or command prompt.
   Run the command::
      
        conda create --name pycookieparser

2. Activate the virtual environment
   
   Once the virtual environment is created successfully, activate it with::
      
        conda activate pycookieparser

3. Clone the `pycookieparser` repository

   In your terminal, navigate to a directory where you'd like to clone the repository. Execute the following command to clone the `pycookieparser` repository::
      
        git clone https://github.com/studiawan/pycookieparser.git

4. Navigate to the root project directory:

   After cloning, you'll have a new directory named `pycookieparser`. Change to this directory with::
      
        cd pycookieparser

5. Install the package
   
   Now that you're in the root project directory, install the package using::
      
        pip install .

6. Verify installation (optional):
   
   You can check if the package is successfully installed in your virtual environment using::
      
        pip list
      
   Look for `pycookieparser` in the list to confirm.
   
   In addition, run `pycookieparser` command on your terminal. It should print `Usage: pycookieparser cookie-file-name`.

7. Completion

   You have successfully installed the `pycookieparser` package in your Anaconda virtual environment.

Remember, every time you need to use this package, ensure that you activate the virtual environment using `conda activate pycookieparser`.
