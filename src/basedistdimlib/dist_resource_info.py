"""
dist_resource_info.py - Distributed simulation resource information

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

class dist_resource_info(base_dist_resc):
    """Distributed resource info class."""
    
    def __init__(self, 
                 resc_name: str, 
                 ip_addr: str, 
                 port: int,
                 auth_ket: str):
        self.resc_name: str = resc_name
        self.ip_addr: str = ip_addr
        self.port: int = port
        self.auth_key: str = auth_key
