## Základní informace
Miniweb je jednoduchý web aplikační framework určený pro mikročipy (primárně ESP8266 a popřípadě ESP32) s důrazem na výkon. Byl vyvinut jako Bakalářská práce, ale bude i dále rozvíjen.

## Používané knihovny třetích stran
 - uasyncio
 - micropython-logging
 - micropip
 - ujson

## API

### Route

Definuje se skrze dekorátor. Obsahuje 4 univerzální funkce a jednu obecnou - *get()*, *post()*, *put()*, *delete()* a *route()*. U obecné je nutné nadefinovat HTTP metodu (či více HTTP metod).
Povinný parametr pro všechny je **path**. Nepovinný parametr je **controller**, který může shlukovat route do skupin. Dalším nepovinným parametrem je **consumes**, které nadefinuje pole akceptovatelných příchozích Content-Type.

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

**Route umí pracovat s path parametry i query parametry**. Více v příkladech.
- [ukázka path parametrů]()
- [ukázka query parametrů]()
- [ukázka použití controlleru v route]()
- [ukázka HTTP response]()
- [ukázka použití consumes v route]()

### Middleware funkce
Definuje se skrze dekorátory. Obsahuje jeden nepovinný parametr -  **controller**. Middleware funkce jsou funkce, které jsou vykonávány před samotným vykonáváním route funkce, slouží pro kontrolu a ochranu. Pokud nemají controller, pak jsou volány před všemi routami, u controllerů naopak jen u route, které patří pod controller.

```python
from miniweb import filter

@filter()
def middleware(req, res):
    return True
    
@filter(userController)
def is_logged(req, res):
    return False
``` 
### Controllery
Controllery slouží pro shromažďování route do skupin. Definuje se jejich cesta. Výsledná cesta route s controllerem *je controller_path+route_path*. Mimo prefix cesty také slouží pro definice middleware funkcí právě jen pro controllery.
```python
from miniweb import Controller, miniweb

app = miniweb()
user_controller = Controller("/user")

@app.get("/id", controller=user_controller)
def get_user_id(req, res):
    #cesta je "/user/id"
    pass
``
