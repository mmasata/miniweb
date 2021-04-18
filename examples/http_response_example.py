from miniweb import app, Mime, Method, Status, Log


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.WARNING,
    "buffer": 128
}


app = app(params)


@app.get("/hello")
def hello(req, res):
    #responses are not required, if they will not be build, then client - server communication will wait until timeout
    #they can be defined by Enumerators
    res.status(Status.OK).type(Mime.HTML).entity("<h1>Hello</h1>").build()
    #build on the end is important, its say that response is ready for send


@app.get("/goodbye")
def goodbye(req, res):
    #its also possible to define without Enumerators
    res.status(200).type("text/html").entity("<h1>Goodbye</h1>").build()


@app.get("/json")
def get_json(req, res):
    #its possible send python dictionary like json
    #miniweb will parse to json string and sent it
    json_dict = {
        "key": "value",
        "arr": [1, 2, 3]
    }
    res.status(Status.OK).type(Mime.JSON).entity(json_dict).build()


app.run()
