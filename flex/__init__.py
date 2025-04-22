"""
Flex
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An ASGI web framework for building simple, fast and scalable web applications.

:copyright: (c) 2024-present Sougata Jana
:license: MIT, see LICENSE for more details.

"""

__title__ = "flex"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present Sougata Jana"
__author__ = "Sougata Jana"
__version__ = "0.0.1a"


from flex.events import Event, EventModifier, Swapping

from . import ui
from .client import App
from .style import CSS
