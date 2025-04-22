from logging import Handler
from typing import Any, Union


from pulse.style import CSS
from .html import HTMLElement, Handler


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
        return child
    return decorator

def input(
    *,
    placeholder: str = "",
    input_type: str = "text",
    **styles: Any,
) -> HTMLElement:
    el = HTMLElement("input", self_enclosing=True)
    el.set(type=input_type)
    el.set(placeholder=placeholder)
    el.style = CSS(**styles)
    return el

def p(
    *children: Union[HTMLElement, str],
    **styles
) -> HTMLElement:
    el = HTMLElement("p")
    el.style = CSS(**styles)
    el.children = list(children)
    return el

def button(
    *children: Union[HTMLElement, str],
    **styles
) -> HTMLElement:
    el = HTMLElement("button")
    el.children = list(children)
    el.style = CSS(**styles)
    return el

def div(
    *children: Union[HTMLElement, str],
    **styles
) -> HTMLElement:
    el = HTMLElement("div")
    el.style = CSS(**styles)
    el.children = list(children)
    return el