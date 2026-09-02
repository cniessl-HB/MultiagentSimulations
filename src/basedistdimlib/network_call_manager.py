"""
network_call_manager.py - A manager for tasks running over the network.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

import threading

class network_call_manager():

    def __init__():
        self._task_manager_mutex = threading.Lock()
        self._task_notifiers = {}
        self._outstanding_tasks = {}
        self._completed_tasks = {}
    
    def setup_connection():
        raise NotImplementedError
    
    def setup_task():
        raise NotImplementedError
    
    def _main_listen_loop():
        raise NotImplementedError
