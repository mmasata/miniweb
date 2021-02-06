import miniweb

#optional parametry portu a ostatnich parametru
#pokud budou prazdne, budou dotazeny z env_file.json
app = miniweb.start(8000)
userController = miniweb.Controller("/user/")


@miniweb.filter()
def globalFilter():
    #implementace logiky middleware
    return True

@miniweb.filter(userController)
def isLoggedIn():
    #implementace logiky middleware
    return True



@app.media(consumes="JSON", produces="XML")
@app.route("/alone", ["GET", "DELETE"])
def noClassFc(req):
    print("ALONE")
    return 0


@app.media(consumes="JSON", produces="XML")
@app.get("foo", userController)
def foo(req):
    print("FOO")
    return 0


@app.media(consumes="JSON", produces="XML")
@app.post("bar/{id}", userController)
def bar(req):
    print("BAR")
    return 0

bar(None)