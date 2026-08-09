"""
dist_resource_info.py - Distributed simulation resource information

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import socket
import ssl

class dist_resource_info(base_dist_resc):
    """Distributed resource info class."""
    
    def __init__(self, 
                 resc_name: str, 
                 target_host: str, 
                 target_port: int,
                 auth_cert: str,
                 require_online = False):
        self.resc_name: str = resc_name
        self.ip_addr: str = ip_addr
        self.port: int = port
        self.auth_cert: str = auth_cert
        self.require_online: bool = require_online
    
    def connect(self) -> bool:
        """Attempt handshake connection with resource."""
        self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        unwrapped_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = context.wrap_socket(raw_socket, server_hostname='localhost') as secure_socket:
        return self.secure_socket.connect((target_host, target_port))

