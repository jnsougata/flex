from typing import Callable, Any

import webview

from webview import Window, Event
from .dom import DOMElement



class App:
    def __init__(
        self,
        path: str = "index.html",
        *,
        title: str = "Flex",
        stylesheet: str = None,
        size: tuple[int, int] = (800, 600),
        resizeable: bool = True,
    ):
        self.title = title
        self.path = path
        self.size = size
        self.resizable = resizeable
        self.stylesheet = stylesheet
        self.window = webview.create_window(
            self.title,
            resizable=self.resizable,
            width=self.size[0],
            height=self.size[1],
            min_size=(self.size[0], self.size[1]),
        )
        self.element_map = {}

    def listen(self, event: str):
        def decorator(func: Callable[[Window, Event], Any]):
            window_event = self.window.events.__dict__[event.lower()]
            window_event += func
        return decorator

    def get_element(self, selector: str) -> DOMElement:
        element = DOMElement(selector)
        self.element_map[selector] = element
        return element

    def _bind(self, window: Window):
        if self.stylesheet:
            with open(self.stylesheet, "r") as f:
                window.dom.get_element(selector="head").append(f"<style>{f.read()}</style>")

        for selector, element in self.element_map.items():
            element._internal = self.window.dom.get_element(selector)
            if not element._internal:
                raise RuntimeWarning(f"Element with selector '{selector}' not found in the DOM.")
            for event, func in element.events.items():
                element_event = element._internal.events.__dict__[event.lower()]
                element_event += lambda e: func(window, e)

    def run(self):
        with open(self.path, "r") as f:
            self.window.html = f.read()

            webview.start(self._bind, self.window)
