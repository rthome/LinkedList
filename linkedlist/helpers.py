import pkgutil
import importlib

from flask import Blueprint


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the given flask app
    found in all modules of the given package
    """
    result = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if (isinstance(item, Blueprint)):
                app.register_blueprint(item)
            result.append(item)
    return result
