from webview import Window, Event
from typing import Callable, Any, Literal

class Handler:

    def __init__(self, selector: str):
        self.selector = selector
        self.events = {}
        self.this = None

    def on(self, event: Literal[
        "CLICK",
        "DBLCLICK",
        "MOUSEDOWN",
        "MOUSEUP",
        "MOUSEOVER",
        "MOUSEOUT",
        "MOUSEMOVE",
        "KEYDOWN",
        "KEYUP",
        "KEYPRESS",
        "FOCUS",
        "BLUR",
        "CHANGE",
        "INPUT",
        "SUBMIT",
        "LOAD",
        "RESIZE",
        "SCROLL",
    ]):
        def decorator(func: Callable[[Window, Event], Any]) -> Callable[[Window, Event], Any]:
            self.events[event] = func
            return func
        return decorator
