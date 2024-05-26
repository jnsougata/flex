from typing import List, Dict, Any, Union, Callable, Coroutine, TYPE_CHECKING

from starlette.requests import Request
from starlette.responses import HTMLResponse

from .htmx import Htmx
from .style import CSS

if TYPE_CHECKING:
    from .doc import Document


Handler = Callable[[Request], Coroutine[Any, Any, "HTMLElement"]]


class HTMLElement:
    def __init__(self, tag: str, self_closing: bool = False):
        self.tag = tag
        self.children: List[Union["HTMLElement", str]] = []
        self.attributes: Dict[str, Any] = {}
        self.self_closing: bool = self_closing
        self.__style: CSS = CSS()

    def append(self, *children: Union["HTMLElement", str]) -> "HTMLElement":
        self.children.extend(children)
        return self

    def set_attribute(self, key: str, value: str) -> "HTMLElement":
        self.attributes[key] = value
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

    def trigger(self, dom: "Document", htmx: Htmx):

        for key, value in htmx.attributes.items():
            self.set_attribute(f'hx-{key}', value)

        if htmx.target:
            self.set_attribute('hx-target', htmx.target)

        if htmx.filters:
            tf = ' '.join(htmx.filters)
        else:
            tf = ''
        self.set_attribute('hx-trigger', f'{htmx.event} {tf}')

        def wrapper(handler: Handler):

            async def callback(request: Request):
                elem = await handler(request)
                return HTMLResponse(str(elem))

            if htmx.method:
                self.set_attribute(f'hx-{htmx.method.lower()}', htmx.path)
                dom.add_route(htmx.path, callback, methods=[htmx.method])
            return handler

        return wrapper
