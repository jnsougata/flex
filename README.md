# Pulse

An ASGI web framework for building simple, fast and scalable web applications.


## Installation
```bash
pip install git+https://github.com/jnsougata/pulse.git
```

## Features
- [x] Auto Routing
- [x] DOM Templating
- [x] HTMX Triggers
- [ ] Middleware
- [ ] Static Files
- [ ] Websockets
- [ ] Sessions
- [ ] Cookies
- [ ] Database
- [ ] Authentication
- [ ] Authorization
- [ ] Rate Limiting
- [ ] Caching
- [ ] Testing
- [ ] Documentation

## Quick Start
```python
import uvicorn

import pulse

app = pulse.Document()
app.head.append(pulse.HTMLElement("title").append("Pulse!"))
app.head.append(pulse.HTMLElement("meta", self_closing=True).set_attribute("charset", "utf-8"))
app.head.append(pulse.HTMLElement("meta", self_closing=True)
                .set_attribute("name", "viewport")
                .set_attribute("content", "width=device-width, initial-scale=1.0"))
elem = pulse.HTMLElement("div")
elem.set_attribute("id", "container")
elem.style.set(**{
    "background-color": "#333",
    "color": "white",
    "padding": "10px",
    "margin": "10px",
    "border-radius": "5px",
    "text-align": "center",
    "height": "100px",
})

button_css = pulse.CSS(**{
    "margin": "10px",
    "padding": "10px",
    "border-radius": "5px",
    "background-color": "teal",
    "color": "white",
    "border": "none",
    "cursor": "pointer",
})


elem.append(pulse.HTMLElement("h1").append("Greetings"))
app.body.append(elem)


incr = pulse.HTMLElement("button").append("+1")
incr.style = button_css

app.counter = 0


@incr.listen(
    app,
    event=pulse.DOMEvent("click")
    .modifiers(pulse.EventModifier.delay(200))
    .method("GET")
    .path("/clicked-p")
    .target("#container h1")
)
async def clicked(_):
    app.counter += 1
    return str(app.counter)


inp = pulse.HTMLElement("input", self_closing=True)
inp.set_attribute("type", "text")
inp.set_attribute("placeholder", "Enter your name")
inp.style = pulse.CSS(**{
    "margin": "10px",
    "padding": "10px",
    "border-radius": "5px",
    "border": "1px solid teal",
    "width": "200px",
    "text-align": "center",
    "font-size": "14px",
    "font-family": "Arial",
    "outline": "none",
})


@inp.listen(
    app,
    event=pulse.DOMEvent("input")
    .modifiers(pulse.EventModifier.delay(0))
    .path("/echo")
    .method("POST")
    .target("#container h1")
    .form(value='event.target.value')
)
async def name(request: pulse.Request):
    data = await request.form()
    return f"Hello, {data['value']}!"


app.body.append(incr)
app.body.append(inp)


if __name__ == "__main__":
    uvicorn.run(app)
```