# Table of Contents
* [Basic information](#basic-information)
* [Third party used libraries](#third-party-used-libraries)
* [API](#api)
    * [Route](#route)
        * [Request](#request)
        * [Response](#response)
    * [Static routers](#static-routers)
    * [Middleware function](#middleware-function)
    * [Controllers](#controllers)
    * [Configuration](#configuration)
        * [List of configuration parameters](#list-of-configuration-parameters)
    * [Enums](#enums)



## Basic information
Miniweb is a simple web application framework designed for microchips (primary ESP8266 and possibly ESP32) with an emphasis on performance. It was created as a Bachelor's thesis, but will be further developed.

## Third party used libraries
**Attention: The framework runs on micropython version 1.14!**
 - uasyncio
 - micropython-logging
 - micropip
 - ujson
 - ure

## API

### Inicialization

Initialization is performed by first importing the miniweb and then storing the Miniweb instance in a variable.
This is done through the app() function, which returns just one instance (Singleton).

```python
import miniweb


app = miniweb.app()
```


### Run and Stop

Starting the server and shutting it down is possible through the run() and stop() methods of the same name.
The start must be called only after all Route/Controllers/Filters have been defined.

The server shutdown has an optional parameter - delay. If it is not filled in, then the Server is terminated immediately,
otherwise it will not end until the specified time (in milliseconds).

*More in example [stop_server_example.py](../examples/stop_server_example.py)*


### Route

It is defined through the decorator. It contains 4 universal functions and one general - *get()*, *post()*, *put()*, *delete()* and *route()*. For general, it is necessary to define an HTTP method (or more HTTP methods).

The required parameter for all is the path. An optional parameter is the **controller**, which can clusters routes into groups. Another optional parameter is **consumes**, which defines the array of acceptable incoming Content-Type.

```python
import miniweb


app = miniweb.app()


@app.route("/foo", [Method.GET, Method.POST])
def foo(req, res):
   pass


@app.get("/bar")
def bar(req, res):
   pass


@app.post("/bar")
def bar(req, res):
   pass


@app.put("/bar")
def bar(req, res):
   pass


@app.delete("/bar")
def bar(req, res):
   pass
``` 

**Route can work with query parameters and also with path parameters**. More in the examples.
- [example of path parameters](../examples/path_param_example.py)
- [example of query parameters](../examples/query_param_example.py)
- [example of using controller inside of route](../examples/controller_example.py)
- [example of defining HTTP response](../examples/http_response_example.py)
- [example of using consumes inside of route](../examples/consumes_example.py)

#### Request
From the request it is possible to access headers, query parameters, or content from the body of the request. The request can process Json and Form Data into an object to make it easy for developers to use. If the miniweb does not know the incoming content-type, the data is only accessible as a String.
```python
   from miniweb import app
  

    #/foo?key=1
    #body: {id: 2, arr: ["a", "b", "c"]}
    @app.post("/foo"):
    def foo(request, res):

      query_parameter_key = request.params["key"]
      request_content = request.content
    
      #its possible to access through the keys if content is json
      json_key_id = request.content["id"]

    
    #Content-Type: "multipart/form-data"
    # file: image.jpg
    # value: 22
    # multilinevalue: line1
    #                 line2
    @app.post("/bar")
    def bar(request, res):

      #if content is multipart/form-data, then its accesed via object attributes
      file = request.content.file
      value = request.content.value
      multilinevalue = request.content.multilinevalue
    
      #access to headers
      headers = request.headers
      content_type = headers["Content-Type"]
``` 

#### Response
For response, it is possible to define the status, content-type and the entity itself. Everything happens through the builder. When the Response is final, the *build()* method must be used
```python
from miniweb import Status, Mime
    Response().status(Status.OK).type(Mime.HTML).entity("<h1>Ahoj, světe!</h1>").build()

    @app.get("/foo")
    def foo(req, res):

       #its possible send dictionary, framework will sent JSON string to client
       dict = {
         "key": "value",
         "arr": [1, 2, 3, 4] 
       }
       res.status(Status.OK).type("application/json").entity(dict).build()
``` 

### Static routers
Static routers are used to manage the serving of static files on the server. More can be defined. They accept two mandatory parameters - **root**, **path** and one optional parameter- **controller**. The **root** parameter defines which folder on the device you are using is the default (for example, "/var/www"). The parameter **path**, on the other hand, defines a kind of alias under which the given root path will be entered in the endpoint *(for example we have root "/var/www/subfolder/" and path "/file/", when we enter "/file/index.html", then the file "/var/www/subfolder/index.html")* is returned.
```python
from miniweb import app
    app = app()

    
    app.static_router(root="/var/www/", path="/file/")
    #http://localhost/file/subfolder/index.html
    # will return
    #/var/www/subfolder/index.html


    app.static.router(root="/var/user/www/", path="/")
    #http://localhost/index.html
    # will return
    #/var/user/www/index.html
``` 

As with regular routes, global middleware functions and possibly also middleware functions of the given controller are applied to Static routers. More in the example:
- [example of static router](../examples/static_route_example.py)

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
from miniweb import Controller, app

app = app()
user_controller = Controller("/user")

@app.get("/id", controller=user_controller)
def get_user_id(req, res):
    #path is "/user/id"
    pass
``` 
### Configuration
It can be configured in two ways - in the code via the constructor or via the configuration file. If both variants are filled in, parameterization through the constructor takes precedence. When configuring via a file, it is necessary that the defined file has an extension *.env*.
```python
from miniweb import app, Log

params = {
    "port": 8000,
    "log": Log.DEBUG,
    "host": "localhost",
    "buffer": 512
}

app = app(params)

``` 
This example describes the first method, the following will be from the second, inside the *.env* file.
```bash
#config.env file
port=8000
log=DEBUG
host=127.0.0.1
buffer=512
``` 
The log level is specified by the String and all letters must be uppercase.


#### List of configuration parameters
| Name       | Description          | Required  |
| ------------- |:-------------:| -----:|
| port      | The port of the server on which it will listen. | &#x2611; |
| log      | Framework log level.      |   &#x2611; |
| host | IP address for the server. (If it connects to wi-fi via boot.py, then enter "0.0.0.0")     |    &#x2611; |
| buffer | The size of the array read file. (Dependent on the chip used - 128,256,512, ...)     |    &#x2611; |

*Note: In the future, the framework will be more robust, more parameters will be added.*


### Enums
Miniweb uses enumerators for Log, HTTP methods, Mime types and HTTP statuses. It is also possible to state exact values.
```python
 #instead of Log.DEBUG you can write 10
 params = {
     "log": 10
 }
 
 #instead of Mime.JSON you can enter "application / json"
 #This same applies to Statuses, instead of Status.OK can be expressed by code numbers - 200
 }
``` 
