# LinkedList source code

LinkedList is an easy-to-use link saving/reading queue webapp. 
It is developed in Python using the Flask framework.

## Developing

### Running the development server

1. Install Python 2.7 and required packages (see requirements.txt).
	* Run `pip install -r requirements.txt` to install everything in one go.
2. Create a config.py file in the `instance` folder, located at the project root.
	* This file must at least contain values for the `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` config keys.
	* To get started quickly, use `sqlite:///:memory:` for SQLALCHEMY_DATABASE_URI, which is a in-memory sqlite database.
3. Run `python wsgi.py`
	* This will start the development server with debugging and reloading enabled.

There is also a `manage.py` script, which provides some CRUD functionality (user management, pep8 compliance testing).

### Deploying

LinkedList is currently deployed at http://linkedlist2.herokuapp.com

## Links

Code for https://bitbucket.org/rthome/softwareengineering

JIRA: http://193.196.7.46:8080/browse/LIN