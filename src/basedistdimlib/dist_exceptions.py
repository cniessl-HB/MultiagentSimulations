"""
dist_exceptions.py - Package for distributed excpetion definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""


class SubsimNotFoundError(Exception):
    """Passed a subsim ID for fetching a subsim that was not added."""


class SubsimDisconnectedError(Exception):
    """Attempted an operation on a disconnected subsim."""
