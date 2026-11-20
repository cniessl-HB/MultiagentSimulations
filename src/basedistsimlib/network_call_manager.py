"""
network_call_manager.py - A manager for tasks running over the network.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import threading
import uuid
from collections import deque
from enum import Enum

from dist_schemas import packet_scanner
from schema_dict import PEER_NETWORK_INFO, GET_PEER_NETWORK_INFO, PACK_TYPE_PEER_NETWORK_INFO

class ncm_state(Enum):
    
    NEED_CONNECTION_INFO = 0
    IDLE = 1
    EXPECTING_RESPONSE = 2
    
    FAILED = 99
    SUCCESS = 100


class ncm_task:
    def __init__(
        self,
        task_name_root: str,
        task_state: ncm_state,
    ):
        self._task_name_root = task_name_root
        self._uuid = uuid.uuid4()
        self._full_task_name = self._task_name_root + "_" + str(self._uuid)
        self._task_state = task_state
        self._completion_notifier = threading.Event()
        self._outbound_packet = None

    def get_full_task_name(self):
        return self._full_task_name

    def get_outbound_packet(self):
        return self._outbound_packet

    def handle_input(self, input_json) -> bool:
        raise NotImplementedError

class init_task(ncm_task):
    
    def __init__(self):
        self._super(self, "initialize", ncm_state.NEED_CONNECTION_INFO)
    
    def handle_input(self, input_json) -> bool:
        packet_type = input_json["packet_type"]
        if packet_type != PACK_TYPE_PEER_NETWORK_INFO:
            # Set outbound packet to request PEER_NETWORK_INFO
            self._outbound_packet = GET_PEER_NETWORK_INFO
            # TODO: Setup outbound packet
            return False
        else:
            # TODO: provide means to pass up peer info to ncm to distributed table
            self._task_state = ncm_state.SUCCESS
            return True

class network_call_manager:
    MAX_PACK_SIZE = 4096
    MAX_QUEUE_SIZE = 64

    def __init__(self, io_socket, addr):

        # Operation variables
        self._task_manager_mutex = threading.Lock()
        self._shutdown_notifier = threading.Event()
        self._is_running: bool = False
        self._ready: bool = False

        # Packet queues
        self._inbound_packet_queue = deque()
        self._outbound_packet_queue = deque()
        self._parent_packet_queue = deque()

        # Task/state-machine related variables  
        self._outstanding_tasks = {}
        self._flagged_tasks = {}

        # IO Socket variables
        self._io_socket = io_socket
        self._packet_scanner = packet_scanner()
        
        # Additional variables
        self.addr = addr

    def get_queue_size(self) -> int:
        with self._task_manager_mutex:
            return len(self._packet_queue)

    def is_running(self) -> bool:
        with self._task_manager_mutex:
            return self._is_running

    def setup_task(self):
        raise NotImplementedError

    def start(self):
        # Add communication initialization as outstanding
        # task upon start-up.
        with self._task_manager_mutex:
            new_init_task = init_task()
            self.outstanding_tasks["peer_connect"] = new_init_task
        
        self._is_running = True
        self._msg_handler = threading.Thread(
            target=self._main_listen_loop(), daemon=True
        )
        self._msg_handler.start()

    def stop(self):
        with self._task_manager_mutex:
            self._is_running = False
        if self._msg_handler:
            self._msg_handler.join()

    def _enque_packet(self, data):
        with self._task_manager_mutex:
            self._inbound_packet_queue.append(data)

    def _process_queue(self):
        procced_packet = None
        task_to_add_data = None
        move_to_flagged = False
        with self._task_manager_mutex:
            procced_packet = self._inbound_packet_queue.popleft()
        target_task_id = procced_packet["packet_id"]
        if target_task_id in self._outstanding_tasks:
            task_to_add_data = task_to_add_data[target_task]
            move_to_flagged = task_to_add_data.handle_input(procced_packet)
        if move_to_flagged:
            with self._task_manager_mutex:
                self._flagged_tasks[target_task_id] = task_to_add_data
                self._outstanding_tasks[target_task_id] = None

    def _main_listen_loop(self):
        prev_ret_data = b""
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
            if self.get_queue_size() > 0:
                self._process_queue()
