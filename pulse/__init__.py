"""
Pulse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An ASGI web framework for building simple, fast and scalable web applications.

:copyright: (c) 2024-present Sougata Jana
:license: MIT, see LICENSE for more details.

"""

__title__ = "pulse"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present Sougata Jana"
__author__ = "Sougata Jana"
__version__ = "0.0.1a"


from .doc import Document
from pulse.event import DOMEvent, EventModifier, Swapping
from .html import HTMLElement
from .style import CSS

from starlette.requests import Request
