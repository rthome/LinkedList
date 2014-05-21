from flask_assets import Environment, Bundle

css_vendor = Bundle("css/bootstrap.css",
                    "css/bootstrap-theme.css",
                    filters="cssmin", output="css/linkedlist_vendor.min.css")

js_vendor = Bundle("js/jquery-1.11.1.min.js",
                   "js/bootstrap.js",
                   filters="jsmin", output="js/linkedlist_vendor.min.js")

css_linkedlist = Bundle("css/linkedlist.css")


def init_app(app):
    assets = Environment(app)
    assets.register("css_vendor", css_vendor)
    assets.register("js_vendor", js_vendor)
    assets.register("css_linkedlist", css_linkedlist)
    assets.manifest = 'cache' if not app.debug else False
    assets.cache = not app.debug
    assets.debug = app.debug
