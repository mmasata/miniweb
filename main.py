from miniweb import miniweb, Controller, filter, Method, Mime

app = miniweb()
userController = Controller("/user/")

#filter vraci boolean, pokud chce poslat i nejakou response naplni ji a vrati False
@filter()
def globalFilter(req, res):
    #implementace logiky middleware
    return True

@filter(userController)
def isLoggedIn(req, res):
    #implementace logiky middleware
    return True

@app.route("/alone", [Method.GET, Method.DELETE])
def noClassFc(req, res):
    print("TEST ENDPOINT 1")

@app.get("foo", userController)
def foo(req, res):
    print("TEST ENDPOINT 2")

@app.post("bar/{id}", userController)
def bar(req, res):
    print("TEST ENDPOINT 3")


params = {
    "port": 8000,
    "log": "debug"
}
app.run(params)


#test volani endpointu z mapy routes
app.routes[2][2]("REQ", "RES")
