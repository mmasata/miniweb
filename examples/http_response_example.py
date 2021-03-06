from miniweb import miniweb, Mime, Method, Status

app = miniweb()


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


app.run()