import markdown
from google import genai

import flex
from flex import htmx, ui

client = genai.Client(api_key="GENAI_API_KEY")

app = flex.App()
app.stylesheet("/public/style.css")
app.htmx("https://unpkg.com/htmx.org@2.0.4")
app.static("public", "/public")

view = ui.div(
    ui.p("Ask Gemini!", font_size="50px", margin="10px", font_weight="600"),
    ui.p("Flash 2.0", font_size="15px", margin="10px", font_weight="400"),
    css="view",
)


@app.register
@htmx.click(
    target=view, expr={"prompt": "document.querySelector('.promptinput').value"}
)
@ui.compose(ui.button("Send", css="sendbutton"))
async def send_button(request):
    form = await request.form()
    prompt = form.get("prompt")
    if not prompt:
        return ui.p("Please enter a prompt.", color="red")

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}\n\n(In about 100 words)"
    )
    md = markdown.Markdown()
    md = md.convert(response.text)
    return md


app.render(
    ui.div(
        view,
        ui.row(
            ui.input(placeholder="Ask anything", css="promptinput"),
            send_button,
            height="70px",
        ),
        css="app",
    )
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
