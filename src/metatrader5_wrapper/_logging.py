"""Logging utilities for metatrader5_wrapper.

The wrapper does not install handlers or configure logging. Applications can
enable output with the standard library logging configuration they already use.
"""

import logging

logger = logging.getLogger("metatrader5_wrapper")
