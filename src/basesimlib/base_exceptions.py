"""
base_exceptions.py - Package and basic excpetion definitions

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class AgentNotFoundError(Exception):
    """Passed an agent ID for fetching an agent that was not added."""
    pass

class DeactivateInactiveAgentError(Exception):
    """An agent ID was already set to deactivated when provided for deactivation."""
    pass
    
class DuplicateAgentError(Exception):
    """Two agents were found with the same agent ID when they should be unique."""
    pass
