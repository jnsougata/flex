from enum import StrEnum
from typing import Literal


class Swapping(StrEnum):
    innerHTML = "innerHTML"
    outerHTML = "outerHTML"
    afterbegin = "afterbegin"
    beforebegin = "beforebegin"
    afterend = "afterend"
    beforeend = "beforeend"
    delete = "delete"
    none = "none"


class EventModifier:

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def once(cls) -> "EventModifier":
        return cls("once")

    @classmethod
    def changed(cls) -> "EventModifier":
        return cls("changed")

    @classmethod
    def delay(cls, ms: int) -> "EventModifier":
        return cls(f"delay:{ms}ms")

    @classmethod
    def throttle(cls, ms: int) -> "EventModifier":
        return cls(f"throttle:{ms}ms")

    @classmethod
    def selector(cls, selector: str) -> "EventModifier":
        return cls(f"from:{selector}")


class DOMEvent:

    def __init__(self, name: str):
        self.name = name
        self._path = None
        self._method = None
        self._target = None
        self._swap = None
        self._form_expr = {}

    @classmethod
    def polling(cls, interval: int) -> "DOMEvent":
        return cls(f"every {interval}ms")

    @classmethod
    def load_polling(cls, interval: int, swap: Swapping) -> "DOMEvent":
        ev = cls(f"load delay:{interval}ms")
        ev.swap(swap)
        return ev

    def path(self, path: str) -> "DOMEvent":
        self._path = path
        return self

    def method(self, method: str) -> "DOMEvent":
        self._method = method
        return self

    def target(self, target: str) -> "DOMEvent":
        self._target = target
        return self

    def swap(self, swap: Swapping) -> "DOMEvent":
        self._swap = swap
        return self

    def form(self, **expr: str) -> "DOMEvent":
        self._form_expr.update(expr)
        return self

    def filters(self, *expr: str, logic: Literal["&&", "||"] = "&&") -> "DOMEvent":
        if logic not in ("&&", "||"):
            raise ValueError("Invalid logic operator")
        self.name += f"[{logic.join(expr)}]"
        return self

    def modifiers(self, *evm: EventModifier) -> "DOMEvent":
        self.name = f"{self.name} {' '.join([m.name for m in evm])}"
        return self

    def merge(self, event: "DOMEvent") -> "DOMEvent":
        self.name += f", {event.name}"
        return self

    def __str__(self) -> str:
        return self.name
