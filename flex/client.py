import webview

from webview import Window
from .handler import Handler
from .ui import HTMLElement


class App:
    def __init__(
        self,
        title: str = "Flex",
        size: tuple[int, int] = (800, 600),
        resizeable: bool = True,

    ):
        super().__init__()
        self.title = title
        self.size = size
        self.resizable = resizeable
        self.head = HTMLElement("head")
        self.head.append(HTMLElement("title").append(title))
        self.head.append(
            HTMLElement("meta", self_enclosing=True).set(charset="utf-8")
        )
        self.head.append(
            HTMLElement("meta", self_enclosing=True).set(
                name="viewport", content="width=device-width, initial-scale=1.0"
            )
        )
        self.body = HTMLElement("body")
        self.window = webview.create_window(
            self.title,
            resizable=self.resizable,
            width=self.size[0],
            height=self.size[1],
            min_size=(self.size[0], self.size[1]),
        )
        self.global_handler_map = {}

    def stylesheet(self, path: str):
        """
        Add CSS styles to the document.
        """
        # read the file content
        with open(path, "r") as f:
            style = HTMLElement("style").append(f.read())
            self.head.append(style)

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

    def get_element(self, selector: str) -> Handler:
        handler = Handler(selector)
        self.global_handler_map[selector] = handler
        return handler

    @property
    def html(self) -> HTMLElement:
        return HTMLElement("html").append(self.head).append(self.body)

    def __str__(self) -> str:
        return f"<!DOCTYPE html>{self.html}"

    def _bind(self, window: Window):
        for selector, handler in self.global_handler_map.items():
            handler.this = self.window.dom.get_element(selector)
            for event, func in handler.events.items():
                js_event = handler.this.events.__dict__[event.lower()]
                js_event += lambda e: func(window, e)

    def run(self):
        self.window.html = str(self)
        webview.start(self._bind, self.window)
