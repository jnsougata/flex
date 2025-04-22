import base64
from io import BytesIO

import matplotlib.pyplot as plt

import flex
from flex import htmx, ui

app = flex.App()
app.stylesheet("/public/style.css")
app.htmx("https://unpkg.com/htmx.org@2.0.4")
app.static("public", "/public")

view = ui.div(
    ui.p("Plot!", font_size="50px", margin="10px", font_weight="600"),
    ui.p("Powered by Matplotlib.", font_size="15px", margin="10px", font_weight="400"),
    css="view",
)


@app.register
@htmx.click(
    target=view,
    expr={
        "x": "document.querySelectorAll('.plot-input')[0].value",
        "y": "document.querySelectorAll('.plot-input')[1].value",
    },
    # It's currently hacky to get the values from the input fields over button click.
    # use form submission instead.
)
@ui.compose(ui.button("Plot", css="plot-button"))
async def plot_button(request):
    form = await request.form()
    x_values = form.get("x")
    y_values = form.get("y")
    if not x_values or not y_values:
        return ui.p("Please enter both X and Y values.", color="red")
    x_values = [float(i) for i in x_values.split(",")]
    y_values = [float(i) for i in y_values.split(",")]
    if len(x_values) != len(y_values):
        return ui.p("X and Y values must have the same length.", color="red")

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker="o")
    plt.title("Plot")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode("utf-8")
    img.close()
    return ui.img(
        src=f"data:image/png;base64,{plot_url}",
        alt="Plot",
        width="100%",
        height="auto",
        objec_fit="contain",
    )


app.render(
    ui.div(
        view,
        ui.input(placeholder="X values (comma separated)", css="plot-input"),
        ui.input(placeholder="Y values (comma separated)", css="plot-input"),
        plot_button,  # type: ignore
        css="app",
    )
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
