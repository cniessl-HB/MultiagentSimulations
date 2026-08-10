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
                 target_host_name: str, 
                 target_ip_addr: str,
                 target_port: int,
                 auth_cert: str,
                 require_online = False):
        self.resc_name: str = resc_name
        self.target_host_name: str = target_host_name
        self.target_ip_addr: str = target_ip_addr
        self.port: int = port
        self.auth_cert: str = auth_cert
        self.require_online: bool = require_online
        self._is_connected: bool = False
    
    def __del__(self):
        if self._is_connected:
            self.disconnect()
    
    def is_connected(self) -> bool:
        """Return connection state."""
        return self._is_connected
    
    def connect(self) -> bool:
        """Attempt handshake connection with resource."""
        self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        unwrapped_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket = self.tls_context.wrap_socket(unwrapped_socket, server_hostname=self.target_host_name)
        self._is_connected = self.secure_socket.connect((self.target_ip_addr, self.target_port))
        return self._is_connected
    
    def disconnect(self) -> None:
        """Tear down connection if present."""
        if not self._is_connected:
            return
        self.secure_socket.shutdown(socket.SHUT_RDWR)
        self.secure_socket.close()
        self._is_connected = False

