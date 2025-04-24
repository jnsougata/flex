# Flex

A fast, minimal ASGI framework for building htmx-powered web apps.


## Installation
```bash
pip install git+https://github.com/jnsougata/flex.git
```

## Features
- [x] Auto Routing
- [x] DOM Templating
- [x] HTMX Triggers
- [ ] Testing
- [ ] Documentation

## Quick Start

```python
import flex
from flex import ui, htmx

app = flex.App()
app.stylesheet("/public/style.css")
app.htmx("https://unpkg.com/htmx.org@2.0.4")
app.static("public", "/public")
app.counter = 0

view = ui.div(
    "Hello, World!",
    ui.p(
        "Click the button to increment the counter.",
        font_size="15px",
        margin="10px",
        font_weight="400"
    ),
    css="view"
)

@app.register
@htmx.click(target=view)
@ui.compose(ui.button("+1", css="increment"))
async def increment(_):
    app.counter += 1
    return str(app.counter)


app.render(
    ui.section(
        ui.section(
            ui.ul(
                ui.li(ui.a("Home", href="/")),
                ui.li(ui.a("About", href="/about")),
                ui.li(ui.a("Contact", href="/contact")),
            ),
            css="navbar"
        ),
        ui.main(view, increment),
        css="app"
    )
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
```
The above code will create the following web app:

- Note: The css is not included in the code snippet. It is linked from `public/style.css` in the code.

![image](https://github.com/user-attachments/assets/094ff17c-79f7-47fb-bab2-ad6c84a9d3c6)

- #### Find the code for following graph plotting app [here.](/examples/graph.py)
![Screenshot From 2025-04-24 22-52-49](https://github.com/user-attachments/assets/bdea655e-bd77-4398-a285-cd4a97c9ef65)
![Screenshot From 2025-04-24 22-53-31](https://github.com/user-attachments/assets/498891b4-ff0c-4e2b-bd56-bb99e2e7ebd5)

