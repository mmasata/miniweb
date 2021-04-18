from miniweb import app, filter, Status, Log


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.INFO,
    "buffer": 128
}


app = app(params)


user_controller = Controller("/user")


@filter()
def global_middleware(req, res):
    #this middleware will be called before every route function

    #middleware passed
    return True


@filter(user_controller)
def user_middleware(req, res):
    #this middleware will be called before routes grouped in user_controller

    #middleware failed, route function will not be called.
    #without response, so client will wait until timeout
    return False


@filter()
def another_middleware(req, res):
    #client get response message
    res.status(Status.UNAUTHORIZED).build()

    #middleware failed, route function will not be called
    return False


app.run()
