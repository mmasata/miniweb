## Basic information
Miniweb is a simple web application framework designed for microchips (primary ESP8266 and possibly ESP32) with an emphasis on performance. It was created as a Bachelor's thesis, but will be further developed.

## Third party used libraries
 - uasyncio
 - micropython-logging
 - micropip
 - ujson

## API

### Route

It is defined through the decorator. It contains 4 universal functions and one general - *get()*, *post()*, *put()*, *delete()* and *route()*. For general, it is necessary to define an HTTP method (or more HTTP methods).
The required parameter for all is the path. An optional parameter is the **controller**, which can clusters routes into groups. Another optional parameter is **consumes**, which defines the array of acceptable incoming Content-Type.

```python
import miniweb

app = miniweb.miniweb()

@app.route("/foo", [Method.GET, Method.POST])
def foo(req, res):
   pass

@app.get("/bar")
def bar(req, res):
   pass
``` 

**Route can work with query parameters and also with path parameters**. More in the examples.
- [example of path parameters]()
- [example of query parameters]()
- [example of using controller inside of route]()
- [example of defining HTTP response]()
- [example of using consumes inside of route]()

### Middleware function
It is defined through decorators. It contains one optional parameter - **controller**. Middleware functions are functions that are performed before the actual execution of the route function, used for control and protection. If they do not have a controller, then they are called before all routes, for controllers, on the contrary, only for routes that belong to the controller.

```python
from miniweb import filter

@filter()
def middleware(req, res):
    return True
    
@filter(userController)
def is_logged(req, res):
    return False
``` 

### Controllers
Controllers are used to collect routes into groups. Their path is defined. The resulting route with controller * is controller_path + route_path *. In addition to the path prefix, it is also used to define middleware functions just for controllers.
```python
from miniweb import Controller, miniweb

app = miniweb()
user_controller = Controller("/user")

@app.get("/id", controller=user_controller)
def get_user_id(req, res):
    #path is "/user/id"
    pass
``` 
