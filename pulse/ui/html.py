import secrets
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Optional, Union

from starlette.requests import Request
from starlette.responses import HTMLResponse

from pulse.events import Event
from pulse.style import CSS

if TYPE_CHECKING:
    from pulse.client import App


Handler = Callable[[Request], Coroutine[Any, Any, "HTMLElement"]]


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

    # noinspection PyProtectedMember
    def listener(self, app: "App", event: Event, **hxattrs: str):
        self.attributes["hx-trigger"] = event.name
        if event._method:
            hxattrs[f"{event._method.lower()}"] = event._path
        if event._target:
            hxattrs["target"] = event._target
        if event._swap:
            hxattrs["swap"] = event._swap
        if event._form_expr:
            hxattrs["vals"] = (
                "js:{ "
                + ", ".join(
                    [f"{key}: {value}" for key, value in event._form_expr.items()]
                )
                + " }"
            )
        self.attributes.update(**{f"hx-{key}": value for key, value in hxattrs.items()})

        if self.handler:

            async def callback(request: Request):
                elem = await self.handler(request)
                return HTMLResponse(str(elem))

            app.add_route(
                hxattrs[event._method.lower()],
                callback,
                methods=[event._method.upper()],
            )
