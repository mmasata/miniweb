from miniweb import app, Log


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.INFO,
    "buffer": 128
}


app = app(params)


#in this example we get HTTP request with endpoint /user?name=John&surname=Smith
@app.get("/user")
def example(req, res):
    #query parameters are stored inside of req
    #params are dictionary
    params = req.params

    name = req.params["name"]  #will return John
    surname = req.params["surname"]  #will return Smith


app.run()
