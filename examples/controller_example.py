from miniweb import app, filter


params = {
    "port": 8000,
    "host": "0.0.0.0",
    "log": Log.INFO,
    "buffer": 128
}


app = app(params)


#define controller for users
user_controller = Controller("/user")


#we can do middleware function only for controllers route
@filter(user_controller)
def is_logged_in(req, res):
    #in this example we want only for routes in user_controller to be checked, if the user is logged in
    return True


@app.get("/hello")
def hello(req, res):
    #doesnt belong to user_controller
    pass


#path will be "/user/password"
@app.put("/password", controller=user_controller)
def change_password(req, res):
    pass


app.run()
