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

dom = pulse.App()

dom.head.append(pulse.HTMLElement("title").append("Pulse!"))

container = pulse.HTMLElement("div")
container.set(id="container")
container.stylesheet.set(
    background_color="teal",
    color="white",
    padding="10px",
    margin="10px",
    border_radius="5px",
    text_align="center",
)
container.append(pulse.HTMLElement("h1").append("Greetings"))
dom.body.append(container)

button_style = pulse.CSS(
    margin="10px",
    padding="10px",
    border_radius="5px",
    background_color="teal",
    color="white",
    border="none",
    cursor="pointer"
)

counter = pulse.HTMLElement("button").append("+1")
counter.stylesheet = button_style

dom.counter = 0


@counter.listener(
    dom,
    pulse.Event("click")
    .method("GET")
    .path("/clicked-p")
    .target("#container h1")
)
async def clicked(_):
    dom.counter += 1
    return str(dom.counter)


name_input = pulse.HTMLElement("input", self_enclosing=True)
name_input.set(type="text", placeholder="Enter your name...")
name_input.stylesheet = pulse.CSS(
    margin="10px",
    padding="10px",
    border_radius="5px",
    border="1px dashed teal",
    width="200px",
    text_align="center",
    font_size="14px",
    outline="none",
    cursor="pointer"
)


@name_input.listener(
    dom,
    pulse.Event("input")
    .path("/echo")
    .method("POST")
    .target("#container h1")
    .form(name='event.target.value')
)
async def echo(request: pulse.Request):
    name = (await request.form()).get("name")
    return f"Hello, {name}!"


dom.body.append(counter)
dom.body.append(name_input)

if __name__ == "__main__":
    uvicorn.run(dom)
```