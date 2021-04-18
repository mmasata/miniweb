from miniweb import app, Log, Mime


params = {
    "port": 8000,
    "host": "localhost",
    "log": Log.DEBUG,
    "buffer": 512
}


app = app(params)


#we say that this route can accept only "application/json"
@app.post("/data/json", consumes=[Mime.JSON])
def get_data(req, res):
    #if request Content-Type is something else, than return error 400 - Bad Request with message
    pass


@app.post("/data/everything")
def get_something(req, res):
    #this route dont check incoming content-type
    pass


app.run()
