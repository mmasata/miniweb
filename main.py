from miniweb import miniweb, Controller, filter, Method, Mime, Status

app = miniweb()
userController = Controller("/user/")

#filter vraci boolean, pokud chce poslat i nejakou response naplni ji a vrati False
@filter()
def globalFilter(req, res):
    #implementace logiky middleware
    #res.status(Status.FORBIDDEN).type(Mime.HTML).entity("Neprosel middleware!").build()
    return True

@filter(userController)
def isLoggedIn(req, res):
    #implementace logiky middleware
    return True

@app.route("/alone", [Method.GET, Method.DELETE])
def noClassFc(req, res):
    res.status(Status.BAD_GATEWAY).build()

@app.get("foo", userController)
def foo(req, res):
    res.status(Status.OK).type(Mime.HTML).entity("foo").build()

@app.post("bar/{user}/user/{id}/", userController)
def bar(req, res, var):
    query_params_string = ""
    path_params_string = ""
    for key in req.params:
        query_params_string += "["+key+"]: "+req.params[key]+"<br>"
    for key in var:
        path_params_string += "[" + key + "]: " + var[key] + "<br>"
    res.status(Status.ACCEPTED).type(Mime.HTML).entity("Path variable jede <br> QueryParams: <br>"+query_params_string+"<br> Path params: <br>"+path_params_string).build()


params = {
    "port": 8000,
    "log": "debug"
}
app.run(params)

