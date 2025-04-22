from typing import Callable, Dict, List, Optional, Union

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from pulse.ui import HTMLElement

from .events import Event
from .style import CSS


class App(Starlette):
    def __init__(
        self,
        title: str = "Pulse",
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

    def write(self, *children: Union[HTMLElement, str]) -> HTMLElement:
        """
        Write HTML elements to the body of the document.
        """
        for child in children:
            if isinstance(child, HTMLElement):
                self.body.append(child)
            else:
                self.body.append(str(child))
        return self.body

    def trigger(
        self,
        event: str,
        method: Optional[str] = "GET",
        target: Optional[HTMLElement] = None,
        form: Optional[Dict[str, str]] = None,
        **hxattrs: str,
    ) -> Callable[[HTMLElement], HTMLElement]:
        def decorator(child: HTMLElement) -> HTMLElement:
            ev = Event(event).path(f"/ui/events/{child.id}").method(method)
            if target:
                ev.target(f"#{target.id}")
            if form:
                ev.form(**form)
            child.listener(self, ev, **hxattrs)
            return child

        return decorator

    @property
    def html(self) -> HTMLElement:
        return HTMLElement("html", auto_id=False).append(self.head).append(self.body)

    def __str__(self) -> str:
        return f"<!DOCTYPE html>{self.html}"
