"""
dist_hash_table.py - Distributed hash table

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import socket
import ssl

class dist_hash_peer():

    def __init__(self,
                 ranking: int,
                 target_host: str,
                 target_port: str):
        self._ranking = ranking
        self._target_host = target_host
        self._target_port = target_port
                 
class dist_hash_table():
    """Distributed hash table."""
    
    def __init__(self, 
                 my_ranking: int,
                 expected_total: int):
        self._finger_table = {}
        self._my_ranking = my_ranking
        self._expected_total = expected_total
    
