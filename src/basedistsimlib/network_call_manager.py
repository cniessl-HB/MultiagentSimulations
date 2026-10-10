"""
network_call_manager.py - A manager for tasks running over the network.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import threading

from collections import deque
from enum import Enum
from time import sleep
import uuid

from dist_schemas import packet_scanner

class ncm_task():

    def __init__(self, 
                 task_name_root: str, 
                 task_state: str,):
        self._task_name_root = task_name_root
        self._uuid = uuid.uuid4()
        self._full_task_name = self._task_name_root + "_" + str(self._uuid)
        self._task_state = task_state
        self._completion_notifier = threading.Event()
    
    def get_full_task_name(self):
        return self._full_task_name
    
    def handle_input(self, input_json):
        raise NotImplementedError

class network_call_manager():

    MAX_PACK_SIZE = 4096
    MAX_QUEUE_SIZE = 64

    def __init__(self, io_socket):
        
        # Operation variables
        self._task_manager_mutex = threading.Lock()
        self._shutdown_notifier = threading.Event()
        self._is_running: bool = False
        self._ready: bool = False

        # Task related variables
        self._packet_queue = deque()
        self._outstanding_tasks = {}
        self._completed_tasks = {}
    
        # IO Socket variables
        self._io_socket = io_socket
        self._packet_scanner = packet_scanner()
    
    def get_queue_size(self) -> int:
        with self._task_manager_mutex:
            return len(self._packet_queue)
    
    def is_running(self) -> bool:
        with self._task_manager_mutex:
            return self._is_running
    
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
    
    def _enque_packet(self, data):
        raise NotImplementedError
    
    def _process_queue(self):
        raise NotImplementedError
    
    def _main_listen_loop(self):
        prev_ret_data = b''
        while self.is_running():
            # If Queue is maxed out, process packet first
            if self.queue_size() >= self.MAX_QUEUE_SIZE:
                self._process_queue()
            # Check incoming data. Queue it up if available.
            # Otherwise process more messages on the queue.
            incoming_data = self._io_socket.recv(self.MAX_PACK_SIZE)
            prev_ret_data = prev_ret_data + incoming_data
            if len(prev_ret_data) > 0:
                trun_point = self._packet_scanner.scan_and_process(incoming_data)
                if trun_point == 0:
                    # The whole packet was used, but a new one isn't available
                    continue
                else:
                    # A packet is ready, enqueue the packet and retain the rest for
                    # processing on the next cycle.
                    prev_ret_data = prev_ret_data[trun_point:]
                    self._enque_packet(self._packet_scanner.get_processed_packet())
            elif self.get_queue_size() > 0:
                self._process_queue()
            
            
            

        
