from miniweb import app, Log, Mime


params = {
    "port": 8000,
    "host": "localhost",
    "log": Log.DEBUG,
    "buffer": 512
}


app = app(params)


@app.get("/stop/server/{ms}")
def stop_server(req, res, var):
    res.status(200).type(Mime.HTML).entity("Will be stopped in {m}".format(m=var["ms"])).build()

    #response method stop will set stop miniweb after delay
    app.stop(var["ms"])
    #stop will start after response sending


@app.get("/stop/server/now")
def stop_server_now(req, res):
    res.status(200).type(Mime.HTML).entity("Stop now.").build()

    #if no parameter given then will be stop immediately
    app.stop()


app.run()
