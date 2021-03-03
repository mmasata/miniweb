# Czech

## Základní informace
Miniweb je jednoduchý web aplikační framework určený pro mikročipy (primárně ESP8266 a popřípadě ESP32) s důrazem na výkon. Byl vyvinut jako Bakalářská práce, ale bude i dále rozvíjen.

## Používané knihovny třetích stran
 - uasyncio
 - micropython-logging
 - micropip
 - ujson

## API

### Route

Definuje se skrze dekorátor. Obsahuje 4 univerzální funkce a jednu obecnou - get(), post(), put(), delete() a route(). U obecné je nutné nadefinovat HTTP metodu (či více HTTP metod).
Povinný parametr pro všechny je cesta. Nepovinný parametr je controller, který může shlukovat route do skupin.

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

Route umí pracovat s path parametry i query parametry. Více v příkladech.
- [ukázka path parametrů]()
- [ukázka query parametrů]()
- [ukázka použití controlleru v route]()
- [ukázka HTTP response]()

# English

## Basic information
Miniweb is a simple web application framework designed for microchips (primary ESP8266 and possibly ESP32) with an emphasis on performance. It was created as a Bachelor's thesis, but will be further developed.

## Third party used libraries
 - uasyncio
 - micropython-logging
 - micropip
 - ujson

## API

### Route

It is defined through the decorator. It contains 4 universal functions and one general - get(), post(), put(), delete() and route(). For general, it is necessary to define an HTTP method (or more HTTP methods).
The required parameter for all is the path. An optional parameter is the controller, which can clusters routes into groups.

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

Route can work with query parameters and also with path parameters.
- [example of path parameters]()
- [example of query parameters]()
- [example of using controller inside of route]()
- [example of defining HTTP response]()
