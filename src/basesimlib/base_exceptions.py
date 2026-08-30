"""
base_exceptions.py - Package and basic excpetion definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""


class AgentNotFoundError(Exception):
    """Passed an agent ID for fetching an agent that was not added."""



class AgentAssignedNoneError(Exception):
    """A None value was inserted as an object in an agent dict."""



class DeactivateInactiveAgentError(Exception):
    """An agent ID was already set to deactivated when provided for deactivation."""



class DuplicateAgentError(Exception):
    """Two agents were found with the same agent ID when they should be unique."""

