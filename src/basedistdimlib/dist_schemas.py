"""
dist_schemas.py - JSON Schemas for various RPC/peer-tasks.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

get_resource_at_key_schema = {}

pass_resource_to_peer_schema = {}

get_peer_network_info = {}

find_next_available_key = {}

SCHEMA_HEADER_MAGIC_NUM = 0x4d53696d

class schema_header():

    def __init__(self, total_size, text_checksum):
        self.total_size = total_size
        self.text_checksum = text_checksum

def scan_for_start(self, input_bytes: bytes) -> int:
    for ii in range(0, len(input_bytes) - 4):
        if input_bytes[ii:(ii+4)] == SCHEMA_HEADER_MAGIC_NUM:
            return ii
    return -1
    # TODO: Change this to be more robust to partial packets

def decode_header(input_bytes: bytes) -> schema_header:
    magic_number = int.from_bytes(input_bytes[0:4], byteorder='big')
    if magic_number != SCHEMA_HEADER_MAGIC_NUM:
        return None
    
    total_size = int.from_bytes(input_bytes[4:8], byteorder='big')
    text_checksum = input_bytes[8:]
    return schema_header(total_size, text_checksum)
