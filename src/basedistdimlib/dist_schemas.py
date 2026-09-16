"""
dist_schemas.py - JSON Schemas for various RPC/peer-tasks.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

get_resource_at_key_schema = {}

pass_resource_to_peer_schema = {}

get_peer_network_info = {}

find_next_available_key = {}

SCHEMA_HEADER_MAGIC_NUM = b'\x4d\x53\x69\x6d'

class schema_header():

    def __init__(self, total_size, text_checksum):
        self.total_size = total_size
        self.text_checksum = text_checksum

class packet_state(Enum):
    SCANNING_MN = 1
    SCANNING_SIZE = 2
    SCANNING_CHKSUM = 3
    READING_DATA = 4

class packet_scanner():

    def __init__(self):
        self.state = packet_state.SCANNING_MN
        self.current_header = schema_header(0, b'\x00\x00\x00\x00')
        self.bytes_in_state = 0
        self.buffer = b''

    def scan_and_process(self, input_bytes: bytes):
        trun_bytes = b''
        if self.state == packet_state.SCANNING_MN:
            ret_val = self._scan_magic_number(input_bytes)
            if ret_val > 0:
            trun_bytes = input_bytes[ret_val:]

    def _scan_magic_number(self, input_bytes: bytes) -> int:
        for ii in range(0, len(input_bytes)):
            if input_bytes[ii] == SCHEMA_HEADER_MAGIC_NUM[self.bytes_in_state]:
                self.bytes_in_state += 1
            if self.bytes_in_state == 4:
                return ii+1
        return -1
            
    return -1
    # TODO: Change this to be more robust to partial packets

def decode_header(input_bytes: bytes) -> schema_header:
    magic_number = int.from_bytes(input_bytes[0:4], byteorder='big')
    if magic_number != SCHEMA_HEADER_MAGIC_NUM:
        return None
    
    total_size = int.from_bytes(input_bytes[4:8], byteorder='big')
    text_checksum = input_bytes[8:]
    return schema_header(total_size, text_checksum)
