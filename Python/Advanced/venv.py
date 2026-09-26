# venv creates an isolated environment around Python so that your project's packages, scripts, and dependencies are separated from other projects.




# 1. to create a virtual environment: 
# command: python -m venv myEnv

# 2. activate your venv
# command: myEnv\Scripts\activate

# 3. install dependencies
# command: pip install pandas numpy

# 4. list the dependencies
# command: pip list

# 5. list all the dependencies with their versions in a requirements.txt file
# command: pip freeze > requirements.txt

# if someone else wants to use your project, they can install the dependencies from the requirements.txt file using the following command:
# command: pip install -r requirements.txt

# deactivate your venv
# command: deactivate
