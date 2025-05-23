from typing import Callable, Dict, List, Optional, Union

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from .htmx import Event, Swapping
from .style import CSS
from .ui import HTMLElement


class App(Starlette):
    def __init__(
        self,
        title: str = "Flex",
        *,
        path: str = "/",
        methods: Optional[List[str]] = None,
    ):
        super().__init__()
        self.title = title
        self.head = HTMLElement("head", auto_id=False)
        self.head.append(HTMLElement("title", auto_id=False).append(title))
        self.head.append(
            HTMLElement("meta", self_enclosing=True, auto_id=False).set(charset="utf-8")
        )
        self.head.append(
            HTMLElement("meta", self_enclosing=True, auto_id=False).set(
                name="viewport", content="width=device-width, initial-scale=1.0"
            )
        )
        self.body = HTMLElement("body", auto_id=False)
        self.add_route(path, lambda _: HTMLResponse(str(self)), methods=methods)

    def static(self, directory: str, route: str) -> None:
        """
        Mount a static files app to serve static files.
        """
        self.mount(route, StaticFiles(directory=directory), name="static")

    def style(self, **styles: str):
        """
        Add CSS styles to the document.
        """
        self.body.style = CSS(**styles)

    def htmx(self, src: str = "https://unpkg.com/htmx.org@2.0.4"):
        self.head.append(HTMLElement("script", auto_id=False).set(src=src))

    def link(self, rel: str, href: str, **attrs) -> HTMLElement:
        link = HTMLElement("link").set(rel=rel, href=href)
        link.set(**attrs)
        self.head.append(link)
        return link

    def script(self, src: str, **attrs) -> HTMLElement:
        script = HTMLElement("script").set(src=src)
        script.set(**attrs)
        self.head.append(script)
        return script

    def stylesheet(self, href: str, **attrs) -> HTMLElement:
        style = HTMLElement("link", auto_id=False).set(rel="stylesheet", href=href)
        style.set(**attrs)
        self.head.append(style)
        return style

    def register(self, elem: HTMLElement):
        """
        Load an HTML element into the body of the document.
        """
        path, callback, methods = elem.route()
        self.add_route(path, callback, methods=methods)
        return elem

    def render(self, *children: Union[HTMLElement, str]) -> HTMLElement:
        """
        Write HTML elements to the body of the document.
        """
        for child in children:
            if isinstance(child, HTMLElement):
                self.body.append(child)
            else:
                self.body.append(str(child))
        return self.body

    @property
    def html(self) -> HTMLElement:
        return HTMLElement("html", auto_id=False).append(self.head).append(self.body)

    def __str__(self) -> str:
        return f"<!DOCTYPE html>{self.html}"
