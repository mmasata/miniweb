import miniweb

#optional parametry portu a ostatnich parametru
#pokud budou prazdne, budou dotazeny z env_file.json
app = miniweb.start(8000)
userController = miniweb.Controller("/user/")

@app.media(consumes="JSON", produces="XML")
@app.route("/alone", ["GET", "DELETE"])
def noClassFc(req):
    print("alone")
    return 0


@app.media(consumes="JSON", produces="XML")
@app.get("foo", userController)
def foo(req):
    print("foo")
    return 0


@app.media(consumes="JSON", produces="XML")
@app.post("bar/{id}", userController)
def bar(req):
    print("bar")
    return 0

bar(None)