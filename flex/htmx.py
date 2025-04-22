from enum import StrEnum
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .ui import HTMLElement


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


class Event:

    def __init__(self, name: str):
        self.name = name
        self.hx_path = None
        self.hx_method = None
        self.hx_target = None
        self.hx_swap = Swapping.innerHTML
        self.hx_form = {}

    @classmethod
    def polling(cls, interval: int) -> "Event":
        return cls(f"every {interval}ms")

    @classmethod
    def load_polling(cls, interval: int, swap: Swapping) -> "Event":
        ev = cls(f"load delay:{interval}ms")
        ev.swap(swap)
        return ev

    def path(self, uid: str) -> "Event":
        self.hx_path = f"/ui/events/{uid}"
        return self

    def method(self, method: str) -> "Event":
        self.hx_method = method
        return self

    def target(self, target: str) -> "Event":
        self.hx_target = target
        return self

    def swap(self, swap: Swapping) -> "Event":
        self.hx_swap = swap
        return self

    def form(self, **expr: str) -> "Event":
        self.hx_form.update(expr)
        return self

    def filters(self, *expr: str, logic: Literal["&&", "||"] = "&&") -> "Event":
        if logic not in ("&&", "||"):
            raise ValueError("Invalid logic operator")
        self.name += f"[{logic.join(expr)}]"
        return self

    def modifiers(self, *evm: EventModifier) -> "Event":
        self.name = f"{self.name} {' '.join([m.name for m in evm])}"
        return self

    def merge(self, event: "Event") -> "Event":
        self.name += f", {event.name}"
        return self

    def __str__(self) -> str:
        return self.name


from typing import Callable, Optional, Dict


def click(
    delay: float = 0,
    target: Optional["HTMLElement"] = None,
    **hxattrs: str
):
    """
    Click event decorator for HTMX events.
    """

    def decorator(child: "HTMLElement") -> "HTMLElement":
        event = "click"
        if delay > 0:
            event = f"click delay:{delay}ms"
        ev = Event(event).method("POST").path(child.id)
        if target:
            ev.target(f"#{target.id}")
        child.load_event(ev, **hxattrs)
        return child

    return decorator


def load_polling(
    delay: float = 0,
    *,
    swapping: Swapping = Swapping.innerHTML,
    target: Optional["HTMLElement"] = None,
    **hxattrs: str
):
    """
    Load polling decorator for HTMX events.
    """

    def decorator(child: "HTMLElement") -> "HTMLElement":
        ev = Event.load_polling(delay, swapping).method("GET").path(child.id)  # noqa
        if target:
            ev.target(f"#{target.id}")
        child.load_event(ev)
        return child

    return decorator


def change(
    target: Optional["HTMLElement"] = None,
    form: Optional[Dict[str, str]] = None,
    **hxattrs: str
) -> Callable[["HTMLElement"], "HTMLElement"]:
    """
    Only issue a request if the value of the element has changed.
    """
    _delay = 0  # delay is not working
    event = "change changed"

    # assert not (delay and throttle), "Cannot use both delay and throttle at the same time"
    # if delay > 0:
    #     event += f" delay:{delay}ms"
    # if throttle > 0:
    #     event += f" throttle:{throttle}ms"
    def decorator(child: "HTMLElement") -> "HTMLElement":
        ev = Event(event).method("POST").path(child.id)
        if target:
            ev.target(f"#{target.id}")
        if form:
            ev.form(**form)
        child.load_event(ev, **hxattrs)
        return child

    return decorator


def trigger(
    event: str,
    method: Optional[str] = "GET",
    target: Optional["HTMLElement"] = None,
    form: Optional[Dict[str, str]] = None,
    **hxattrs: str,
) -> Callable[["HTMLElement"], "HTMLElement"]:
    def decorator(child: "HTMLElement") -> "HTMLElement":
        ev = Event(event).path(child.id).method(method)
        if target:
            ev.target(f"#{target.id}")
        if form:
            ev.form(**form)
        child.load_event(ev, **hxattrs)
        return child

    return decorator


def polling(
    interval: int,
    *,
    target: Optional["HTMLElement"] = None,
    swapping: Swapping = Swapping.innerHTML,
    **hxattrs: str
) -> Callable[["HTMLElement"], "HTMLElement"]:
    """
    Polling decorator for HTMX events.
    """

    def decorator(child: "HTMLElement") -> "HTMLElement":
        event = Event.polling(interval).swap(swapping).method("GET").path(child.id)
        if target:
            event.target(f"#{target.id}")
        child.load_event(event, **hxattrs)
        return child

    return decorator
