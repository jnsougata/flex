import uvicorn

import pulse

dom = pulse.Document()
dom.head.append(pulse.HTMLElement("title").append("Libra!"))
dom.head.append(pulse.HTMLElement("meta", self_closing=True).set_attribute("charset", "utf-8"))
dom.head.append(pulse.HTMLElement("meta", self_closing=True)
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
dom.body.append(elem)


incr_button = pulse.HTMLElement("button").append("+1")
incr_button.style = button_css

decr_button = pulse.HTMLElement("button").append("- 1")
decr_button.style = button_css

dom.counter = 0


@incr_button.trigger(dom, pulse.Htmx("click", method="get", path="/clicked-p", target="#container h1"))
async def clicked(_):
    dom.counter += 1
    return str(dom.counter)


@decr_button.trigger(dom, pulse.Htmx("click", method="get", path="/clicked-m", target="#container h1"))
async def minus(_):
    if dom.counter > 0:
        dom.counter -= 1
    return str(dom.counter)


input_elem = pulse.HTMLElement("input", self_closing=True)
input_elem.set_attribute("type", "text")
input_elem.set_attribute("placeholder", "Enter your name")
input_elem.style = pulse.CSS(**{
    "margin": "10px",
    "padding": "10px",
    "border-radius": "5px",
    "border": "1px solid teal",
    "width": "200px",
    "text-align": "center",
    "font-size": "16px",
    "font-family": "Arial",
    "outline": "none",
})


@input_elem.trigger(dom, pulse.Htmx(
    "keyup changed delay:500ms",
    method="POST",
    path="/echo",
    target="#container h1",
    vals='js:{value: event}'
))
async def name(request: pulse.Request):
    data = await request.form()
    return f"Hello, {data}!"


dom.body.append(incr_button)
dom.body.append(decr_button)
dom.body.append(input_elem)


if __name__ == "__main__":
    uvicorn.run(dom)
