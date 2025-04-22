from logging import Handler
from typing import Any, Optional, Union

from flex.style import CSS

from .html import Handler, HTMLElement


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
