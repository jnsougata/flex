from typing import List, Dict, Any, Union, Callable, Coroutine, TYPE_CHECKING

from starlette.requests import Request
from starlette.responses import HTMLResponse

from .event import DOMEvent
from .style import CSS

if TYPE_CHECKING:
    from .dom import Document


Handler = Callable[[Request], Coroutine[Any, Any, "HTMLElement"]]


class HTMLElement:
    def __init__(self, tag: str, self_enclosing: bool = False):
        self.tag = tag
        self.children: List[Union["HTMLElement", str]] = []
        self.attributes: Dict[str, Any] = {}
        self.self_closing: bool = self_enclosing
        self.__style: CSS = CSS()

    def append(self, *children: Union["HTMLElement", str]) -> "HTMLElement":
        self.children.extend(children)
        return self

    def set(self, **attrs: str) -> "HTMLElement":
        self.attributes.update(attrs)
        return self

    @property
    def style(self) -> CSS:
        return self.__style

    @style.setter
    def style(self, value: CSS):
        self.__style = value

    def __str__(self) -> str:
        attrs = ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])
        if str(self.__style):
            attrs += f' style="{self.__style}"'
        children = ''.join([str(child) if isinstance(child, HTMLElement) else child for child in self.children])
        if self.self_closing:
            return f'<{self.tag} {attrs} />'
        else:
            return f'<{self.tag} {attrs}>{children}</{self.tag}>'

    # noinspection PyProtectedMember
    def listen(self, dom: "Document", event: DOMEvent, **hx_attrs: str):
        if event._method:
            hx_attrs[f"{event._method.lower()}"] = event._path
        if event._target:
            hx_attrs["target"] = event._target
        if event._swap:
            hx_attrs["swap"] = event._swap
        if event._form_expr:
            hx_attrs["vals"] = ("js:{ "
                                + ", ".join([f"{key}: {value}" for key, value in event._form_expr.items()]) + " }")
        hx_attrs["trigger"] = event.name
        for key, value in hx_attrs.items():
            self.set(**{f"hx-{key}": str(value)})

        # noinspection PyProtectedMember
        def wrapper(handler: Handler):

            async def callback(request: Request):
                elem = await handler(request)
                return HTMLResponse(str(elem))
            dom.add_route(hx_attrs[event._method.lower()], callback, methods=[event._method.upper()])
            return handler

        return wrapper
