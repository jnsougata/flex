from typing import List, Optional

from starlette.applications import Starlette
from starlette.responses import HTMLResponse

from .html import HTMLElement


class Document(Starlette):
    def __init__(self, *, path: str = "/", methods: Optional[List[str]] = None):
        super().__init__()
        self.__html = HTMLElement("html")
        self.__head = HTMLElement("head")
        self.__head.append(
            HTMLElement("script").set_attribute("src", "https://unpkg.com/htmx.org@1.9.12"))
        self.__body = HTMLElement("body")
        self.html.append(self.head, self.body)
        self.add_route(path, lambda _: HTMLResponse(str(self)), methods=methods)
        self._handlers = {}

    @property
    def html(self) -> HTMLElement:
        return self.__html

    @property
    def head(self) -> HTMLElement:
        return self.__head

    @property
    def body(self) -> HTMLElement:
        return self.__body

    def __str__(self) -> str:
        return f"<!DOCTYPE html>{self.__html}"
