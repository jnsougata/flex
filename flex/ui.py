import secrets
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

from starlette.requests import Request
from starlette.responses import HTMLResponse

from .htmx import Event
from .style import CSS

Handler = Callable[[Request, ...], Coroutine[Any, Any, "HTMLElement"]]


class HTMLElement:
    def __init__(self, tag: str, self_enclosing: bool = False, auto_id: bool = True):
        self.tag = tag
        self.attributes: Dict[str, Any] = {}
        if auto_id:
            self.id = f"{tag}-{secrets.token_hex(8)}"
            self.attributes["id"] = self.id
        else:
            self.id = None
        self.children: List[Union["HTMLElement", str]] = []
        self.self_closing: bool = self_enclosing
        self.style: CSS = CSS()
        self.handler: Optional[Handler] = None
        self.event: Optional[Event] = None

    def load_event(self, event: Event, **hxattrs: str):
        self.event = event
        self.attributes["hx-trigger"] = event.name
        if event.hx_method:
            hxattrs[event.hx_method.lower()] = event.hx_path
        if event.hx_target:
            hxattrs["target"] = event.hx_target
        if event.hx_swap:
            hxattrs["swap"] = event.hx_swap
        if event.hx_form:
            vals = ", ".join(
                [f"{key}: {value}" for key, value in event.hx_form.items()]
            )
            hxattrs["vals"] = f"js:{{{vals}}}"
        self.attributes.update(**{f"hx-{key}": value for key, value in hxattrs.items()})

    def route(self):
        """
        Create a route for the element.
        """
        if not self.handler:
            raise ValueError("Handler is not set")
        if not self.event:
            raise ValueError("Event is not set")

        async def callback(request: Request, *args, **kwargs):
            elem = await self.handler(request, *args, **kwargs)
            return HTMLResponse(str(elem))

        return self.event.hx_path, callback, [self.event.hx_method]

    def append(self, *children: Union["HTMLElement", str]) -> "HTMLElement":
        self.children.extend(children)
        return self

    def set(self, **attrs: str) -> "HTMLElement":
        self.attributes.update(attrs)
        return self

    def __str__(self) -> str:
        attrs = " ".join([f'{key}="{value}"' for key, value in self.attributes.items()])
        if str(self.style):
            attrs += f' style="{self.style}"'
        children = "".join(
            [
                str(child) if isinstance(child, HTMLElement) else child
                for child in self.children
            ]
        )
        if self.self_closing:
            return f"<{self.tag} {attrs} />"
        else:
            return f"<{self.tag} {attrs}>{children}</{self.tag}>"


def compose(
    child: Union[HTMLElement, str],
    **attrs: str,
):
    """
    Compose a function that listens to a DOM event and returns an HTML element.
    """
    if not isinstance(child, HTMLElement):
        raise TypeError("child must be an instance of HTMLElement")

    def decorator(func: Handler):
        child.handler = func  # noqa
        child.set(**attrs)
        return child

    return decorator


def main(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("main")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


# noinspection PyShadowingBuiltins
def input(
    *,
    placeholder: str = "",
    type: str = "text",
    css: Optional[str] = None,
    **styles: Any,
) -> HTMLElement:
    el = HTMLElement("input", self_enclosing=True)
    el.set(type=type)
    el.set(placeholder=placeholder)
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    return el


def p(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("p")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


def button(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("button")
    el.children = list(children)
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    return el


def div(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("div")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


def ul(*children: Union[HTMLElement, str], css: Optional[str] = None, **styles):
    el = HTMLElement("ul")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


def li(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("li")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


def section(
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("section")
    el.style = CSS(**styles)
    if css:
        el.set(**{"class": css})
    el.children = list(children)
    return el


def span(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("span")
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def h1(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("h1")
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def h2(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("h2")
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def h3(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("h3")
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def h4(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("h4")
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def a(*children: Union[HTMLElement, str], href: str = "#", **styles) -> HTMLElement:
    el = HTMLElement("a")
    el.set(href=href)
    el.style = CSS(**styles)
    el.children = list(children)
    return el


def img(src: str, **styles) -> HTMLElement:
    el = HTMLElement("img", self_enclosing=True)
    el.set(src=src)
    el.style = CSS(**styles)
    return el


def form(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("form")
    el.style = CSS(**styles)
    el.children = list(children)
    return el
