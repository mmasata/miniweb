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
- [ukázka path parametrů](../examples/path_param_example.py)
- [ukázka query parametrů](../examples/query_param_example.py)
- [ukázka použití controlleru v route](../example/controller_example.py)
- [ukázka HTTP response](../example/http_response_example.py)
- [ukázka použití consumes v route](../example/consumes_example.py)

#### Request
Z requestu je možné přistoupit k headers, query parametrům, či kontentu z těla requestu. Request umí zpracovávat Json a Form Data do objektu, aby byla lehce použitelná pro vývojáře. Když miniweb příchozí content-type nezná, jsou data přístupná pouze jako String.
```python
    query_parameter_key = request.params["key"]
    request_content = request.content
    
    #pokud je content json lze pristupovat pres klice
    json_key_id = request.content["id"]
    
    #pokud je content multipart/form-data pristupuje se pres atributy objektu
    file = request.content.file
    value = request.content.value
    multilinevalue = request.content.multilinevalue
    
    #pristup k headers
    headers = request.headers
    content_type = headers["Content-Type"]
``` 

#### Response
U response je možné nadefinovat status, content-type a samotnou entitu. Vše se děje přes builder. Když už je Response finální, musí být použita metoda *build()*.
```python
from miniweb import Status, Mime
    Response().status(Status.OK).type(Mime.HTML).entity("<h1>Ahoj, světe!</h1>").build()
``` 

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
``` 
### Konfigurace
Konfigurovat lze dvěmi způsoby - v kódu přes konstruktor, nebo přes konfigurační soubor. Pokud jsou vyplněny obě varianty, přednost má parametrizace skrze konstruktor. Při konfiguraci přes soubor je nutné aby nadefinovaný soubor měl koncovku *.env*.
```python
from miniweb import miniweb, Log

params = {
    "port": 8000,
    "log": Log.DEBUG,
    "host": "localhost"
}

app = miniweb(params)

``` 
V této ukázce je popsán první způsob, v následující bude z druhé, uvnitř *.env* souboru.
```bash
#config.env soubor
port=8000
log=DEBUG
host=127.0.0.1
``` 
Úroveň logu je uváděna Stringu a všechna písmena musí být velká.

### Enumerátory
Miniweb používá enumerátory pro Log, HTTP metody, Mime typy a HTTP statusy. Je možné uvádět i přesnými hodnotami
```python
 #místo Log.DEBUG lze zapsat 10
 params = {
     "log": 10
 }
 
 #místo Mime.JSON lze zadat "application/json"
 #To stejné platí pro Statusy, místo Status.OK lze vyjádřit čísly kódu - 200
 }
``` 
