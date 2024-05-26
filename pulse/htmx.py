from typing import List, Optional


class Htmx:
    def __init__(
        self,
        event: str,
        *,
        method: Optional[str] = None,
        path: Optional[str] = None,
        filters: Optional[List[str]] = None,
        target: Optional[str] = None,
        **attributes: str
    ):
        self.event = event
        self.filters = filters
        self.attributes = attributes
        self.method = method
        self.path = path
        self.target = target
