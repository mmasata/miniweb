from miniweb import app, Controller, filter, Log


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.INFO,
    "buffer": 128
}


app = app(params)


file_controller = Controller("/file")


@filter()
def global_filter(req, res):
    #global filters are also applied to static routers
    pass


@filter(file_controller)
def some_filter_for_file(req, res):
    #as classic route we also can validate static router requests
    pass


#through home router we also can access to subfolders, so in this example is "/subf" redundant
app.static_router(root="/var/www/", path="/home/", controller=file_controller)
app.static_router(root="/var/www/subfolder/", path="/subf/", controller=file_controller)


#controller is optional parameter, we dont have to define it
app.static_router(root="/etc/", path="/etc/")


app.run()
