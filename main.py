from miniweb import miniweb, Controller, filter

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

@app.media(consumes="JSON", produces="XML")
@app.route("/alone", ["GET", "DELETE"])
def noClassFc(req, res):
    print("TEST ENDPOINT")

@app.media(consumes="JSON", produces="XML")
@app.get("foo", userController)
def foo(req, res):
    print("TEST ENDPOINT")

@app.media(consumes="JSON", produces="XML")
@app.post("bar/{id}", userController)
def bar(req, res):
    print("TEST ENDPOINT")


params = {
    "port": 8000,
    "log": "debug"
}
app.run(params)

#Test volani endpointu
bar("REQ", "RES")
