from typing import Any, Dict, List, Optional, Union

from .style import CSS


class HTMLElement:
    def __init__(self, tag: str, *, id:str = None, self_enclosing: bool = False):
        self.tag = tag
        self.attributes: Dict[str, Any] = {}
        self.id = id
        self.children: List[Union["HTMLElement", str]] = []
        self.self_closing: bool = self_enclosing
        self.style: CSS = CSS()
        self.handlers = {}

    def append(self, *children: Union["HTMLElement", str]) -> "HTMLElement":
        self.children.extend(children)
        return self

    def set(self, **attrs: str) -> "HTMLElement":
        self.attributes.update(attrs)
        return self

    def __str__(self) -> str:
        if self.id:
            self.attributes["id"] = self.id
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

# noinspection PyShadowingBuiltins
def input(
    *,
    field: str = "",
    value: Any = None,
    placeholder: str = "",
    type: str = "text",
    css: Optional[str] = None,
    id: Optional[str] = None,
    **styles: Any,
) -> HTMLElement:
    el = HTMLElement("input", self_enclosing=True, id=id)
    if field:
        el.set(name=field)
    if value:
        el.set(value=value)
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
    id: Optional[str] = None,
    *children: Union[HTMLElement, str], css: Optional[str] = None, **styles
) -> HTMLElement:
    el = HTMLElement("div", id=id)
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


def img(src: str, alt: str = "alt", **styles) -> HTMLElement:
    el = HTMLElement("img", self_enclosing=True)
    el.set(src=src)
    el.style = CSS(**styles)
    el.set(alt=alt)
    return el


def form(*children: Union[HTMLElement, str], **styles) -> HTMLElement:
    el = HTMLElement("form")
    el.style = CSS(**styles)
    el.children = list(children)
    return el
