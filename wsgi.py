from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from linkedlist import api, frontend

application = DispatcherMiddleware(frontend.create_app(), {
    "/api": api.create_app(),
})

if __name__ == "__main__":
    import os
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        port = 5000
    run_simple(host, port, application,
               use_reloader=True,
               use_debugger=True)
