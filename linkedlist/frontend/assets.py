from flask_assets import Environment, Bundle

css_all = Bundle("css/bootstrap.css",
                 "css/bootstrap-theme.css",
                 "css/linkedlist.css",
                 filters="cssmin", output="css/linkedlist_all.min.css")

js_all = Bundle("js/jquery-1.11.1.min.js",
                "js/bootstrap.js",
                filters="jsmin", output="js/linkedlist_all.min.js")


def init_app(app):
    assets = Environment(app)
    assets.register("css_all", css_all)
    assets.register("js_all", js_all)
    assets.manifest = 'cache' if not app.debug else False
    assets.cache = not app.debug
    assets.debug = app.debug
