# Simple wsgi framework

Script written for training.\
This http server can parse request and give response.

# How to install
Script used only python3 stdlib. Nothing to install.

# How to run
Server might be runner with default config (`localhost:9005`) or you can specify yourself it.

Example code run server on localhost with port `9004`:
```python
from webby import App

app = App()

@app.add_to_url_map(url='/bar')
def bar_page():
    s ='Bar here!'
    return s

@app.add_to_url_map(url='/foo')
def foo_page():
    s = 'Foo here!'
    return s

app.run_server(port=9004)
```
Then go to `http://127.0.0.1:9004/bar` or `http://127.0.0.1:9004/foo` and you should see `Bar here!` or `Foo here!` 
