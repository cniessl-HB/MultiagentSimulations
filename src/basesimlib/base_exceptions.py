"""
base_exceptions.py - Package and basic excpetion definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class DuplicateAgentError(Exception):
    """Two agents were found with the same agent ID when they should be unique."""
    pass
