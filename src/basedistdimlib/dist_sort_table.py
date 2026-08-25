"""
dist_hash_table.py - Distributed hash table

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from queue import Queue
from BTrees.OOBTree import OOBTree

import socket
import ssl


class dist_sort_peer():

    def __init__(self,
                 ranking: int,
                 min_key: str,
                 max_key: str,
                 target_host: str,
                 target_port: str):
        self._ranking = ranking
        self._min_key = min_key
        self._max_key = max_key
        self._target_host = target_host
        self._target_port = target_port
        self._socket = None
    
    def handshake_peer(self):
        raise NotImplementedError
        
    def query_agent(self, target_key: str):
        raise NotImplementedError
    

class dist_hash_task():
 
    def __init__(self,
                 
         
class dist_sort_table():
    """Distributed sorted table."""
    
    def __init__(self, 
                 my_ranking: int,
                 expected_num_agents: int,
                 parent_object,
                 comms_socket):
        self._inbound_message_queue = Queue(maxsize=32)
        self._outstanding_tasks = {}
        
        self._dist_key_table = OOBTree()
        
        self._my_ranking = my_ranking
        self.expected_num_agents = expected_total
        
        self._parent_object = parent_object
        self._my_socket = comms_socket
    
    
    
    def find_resource(self, target_key: str) -> str:
        raise NotImplementedError
    
    def get_min_key(self) -> str:
        return self._dist_key_table.minKey()
    
    def get_max_key(self) -> str:
        return self._dist_key_table.maxKey()
    
    def _handshake_peer(self, target_host, target_port) -> bool:
        raise NotImplementedError
    
    def _pass_request_on(self, target) -> str:
        raise NotImplementedError
    
    def _give_my_info(self) -> str:
        """return JSON string containing target information."""
        ret_dict = {"ranking": self._my_ranking,
                    "min_key": self
                    "hostname": self._my_host,
                    "port": self._my_port
        
        return json.dumps(ret_dict)
        
        
    def _comms_loop(self):
        raise NotImplementedError
