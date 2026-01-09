from webview import Window, Event
from typing import Callable, Any, Literal, List


# allowed wrapped operations are
# 'append', 'attributes', 'blur', 'children', 'classes', 'copy',
# 'empty', 'events', 'focus', 'focused', 'hide', 'id', 'move', 'next',
# 'node', 'off', 'on', 'parent', 'previous', 'remove', 'show', 'style',
# 'tabindex', 'tag', 'text', 'toggle', 'value', 'visible'

class DOMElement:

    def __init__(self, selector: str):
        self.selector = selector
        self.events = {}
        self._internal = None

    def append(self, element: str):
        return self._internal.append(element)

    @property
    def attributes(self) -> Any:
        return self._internal.attributes

    def set_attribute(self, key: str, value: str):
        self._internal.attributes[key] = value

    def get_attribute(self, key: str):
        return self._internal.attributes.get(key)

    @property
    def classes(self):
        return self._internal.classes

    def blur(self):
        return self._internal.blur()

    @property
    def children(self) -> List[Any]:
        return self._internal.children  # TODO: Parse to appropriate type

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
