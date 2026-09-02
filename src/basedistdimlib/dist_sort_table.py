"""
dist_sort_table.py - Distributed organized table.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from queue import Queue
import threading
from BTrees.IOBTree import IOBTree

import socket
import ssl

from network_call_manager import network_call_manager

class dist_sort_peer():

    def __init__(self,
                 ranking: int,
                 target_host: str,
                 target_port: str):
        self._ranking = ranking
        self._target_host = target_host
        self._target_port = target_port
        self._socket = None
    
    def handshake_peer(self):
        raise NotImplementedError
    
    def query_resc(self, target_key: str):
        raise NotImplementedError
        
    def query_max_key(self):
        raise NotImplementedError
    
    def _send_query(self, target_key: str):
        raise NotImplementedError
    

class dist_hash_task():
 
    def __init__(self, task_name: str):
        self.task_name = task_name
                 
         
class dist_sort_table():
    """Distributed sorted table."""
    
    def __init__(self, 
                 my_ranking: int,
                 expected_num_agents: int,
                 parent_object,
                 listening_port):
        
        # Communication related variables
        self._listening_port = listening_port
        self._inbound_message_queue = Queue(maxsize=expected_num_agents)
        
        # Task related variables
        self._network_call_manager = network_call_manager()
        
        # Distributed peer talk table
        self._my_ranking = my_ranking
        self._expected_num_agents = expected_total
        self._obj_key_table = IOBTree()
        self._peer_table = IOBTree()
        
        # Callback to manager.
        self._parent_object = parent_object
    
    def add_resource(self, resource) -> bool:
        new_key = self._find_next_key_to_use()
        if new_key % my_ranking == 0:
            self._add_to_my_table(new_key, resource)
        else:
            raise NotImplementedError
        
    
    def find_resource(self, target_key: str) -> str:
        if self._dist_key_table.has_key(target_key):
            return self._dist_key_table[target_key]
        # TODO: Add task in outstanding tasks for execution in comms_loop
        return self._continuation_find_resc(target_key)
    
    def get_min_key(self) -> str:
        return self._obj_key_table.minKey()
    
    def get_max_key(self) -> str:
        return self._obj_key_table.maxKey()
    
    def _accept_connection(self):
        raise NotImplementedError
    
    def _add_to_my_table(self, key, resource):
        raise NotImplementedError
    
    def _continuation_find_resc(self, target_key: str):
        completed = False
        raise NotImplementedError
        """
        while not completed:
            with self._task_manager_mutex:
                if target_key in self._outstanding_tasks:
                    task_to_exec = self.outstanding_tasks.pop(target_key)
                    return self._process_task(task_to_exec)
            self.
        """
    def _find_next_key_to_use(self) -> int:
        # Start by finding three reference points for
        highest_known = self.get_max_key()
        for peer in list(self._peer_table.keys()):
        compare_list[0] = self.get_max_key()
        
        mid_peer = 
        
        compare_list[1] = 
    
    def _handshake_peer(self, target_host, target_port) -> bool:
        raise NotImplementedError
    
    def _pass_request_on(self, target) -> str:
        raise NotImplementedError
    
    def _give_my_info(self) -> str:
        """return JSON string containing target information."""
        ret_dict = {"ranking": self._my_ranking,
                    "min_key": self.get_min_key(),
                    "max_key": self.get_max_key(),
                    "hostname": self._my_host,
                    "port": self._my_port
        
        return json.dumps(ret_dict)
        
        
    def _comms_loop(self):
        raise NotImplementedError
