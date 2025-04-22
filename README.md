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

Note: The css is not included in the code snippet. It is linked from `public/style.css` in the code.

![image](https://github.com/user-attachments/assets/094ff17c-79f7-47fb-bab2-ad6c84a9d3c6)
![plot](https://github.com/user-attachments/assets/b4ca4218-89b2-48ed-94dd-a84b4717f4c1)

