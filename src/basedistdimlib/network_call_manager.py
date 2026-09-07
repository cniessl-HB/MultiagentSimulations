"""
network_call_manager.py - A manager for tasks running over the network.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import threading

from time import sleep
import uuid

class ncm_task():

    def __init__(self, 
                 task_name_root: str, 
                 task_state: str,):
        self._task_name_root = task_name_root
        self._uuid = uuid.uuid4()
        self._full_task_name = self._task_name_root + "_" + str(self._uuid)
        self._task_state = task_state
    
    def get_full_task_name(self):
        return self._full_task_name
    
    def handle_input(self, input_json):
        raise NotImplementedError

class ncm_peer():

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

class network_call_manager():

    def __init__(self, ):
        
        # Operation variables
        self._task_manager_mutex = threading.Lock()
        self._shutdown_notifier = threading.Event()
        self._is_running = False
        self._ready = False

        # Task related variables
        self._outstanding_tasks = {}
        self._completed_tasks = {}
    
    def is_running(self):
        with self._task_manager_mutex:
            return self._is_running
    
    def setup_connection(self):
        raise NotImplementedError
    
    def setup_task(self):
        raise NotImplementedError
    
    def start(self):
        if not self._ready:
            raise RuntimeException
        self._is_running = True
        self._msg_handler = threading.Thread(target=self._main_listen_loop(), daemon=True)
        self._msg_handler.start()
        
    def stop(self):
        with self._task_manager_mutex:
            self._is_running = False
        if self._msg_handler:
            self._msg_handler.join() 
       
    def _main_listen_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
                sock.bind(("127.0.0.1", 8443))
    sock.listen(5)
            while self.is_running():
            

    
    print("Server listening on port 8443...")
    
    while True:
        # Accept raw TCP connections
        client_sock, addr = sock.accept()
        
