from miniweb import app, Log


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.INFO,
    "buffer": 128
}


app = app(params)


#path parameters are wrapped in {}
@app.get("name/{name}/surname/{surname}")
def example(req, res, var):
    #if route has path parameters, then route function will have 3 parameters
    #path parameters values will be stored inside of var
    name = var["name"]
    surname = var["surname"]
    pass


#route without path parameter
@app.post("/foo")
def foo(req, res):
    #this route is without path parameter, so route function will have only 2 parameters - req and res
    pass


app.run()
