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

    def __init__(self):
        self.size_bytes = b'\x00\x00\x00\x00'
        self.text_checksum = b'\x00\x00\x00\x00'
    
    def _decode_size(self) -> int:
        return int.from_bytes(self.size_bytes, byteorder='big')
    
    def _decode_checksum(self) -> int:
        return int.from_bytes(self.text_checksum, byteorder='big')
    
    def compare_size(self, read_buffer_size: int) -> bool:
        return (self._decode_size() == read_buffer_size + 12)
    
    def compare_checksums(self, checksum: int) -> bool:
        return (self._decode_checksum() == checksum)

class packet_state(Enum):
    SCANNING_MN = 1
    SCANNING_SIZE = 2
    SCANNING_CHKSUM = 3
    READING_DATA = 4
    READING_COMPLETE = 5

class packet_scanner():

    def _reset_state(self):
        self.state = packet_state.SCANNING_MN
        self.current_header = schema_header()
        self.bytes_in_state = 0
        self.working_buffer = b''
        self.working_chescksum = 0

    def __init__(self):
        self._reset_state()

    def scan_and_process(self, input_bytes: bytes):
        trun_bytes = b''
        ret_val = 0
        if self.state == packet_state.SCANNING_MN:
            ret_val = self._scan_magic_number(input_bytes)
            if ret_val == 0:
                return
            else:
                trun_bytes = input_bytes[ret_val:]
        if self.state == packet_state.SCANNING_SIZE:
            ret_val = self._scan_size(input_bytes)
            if ret_val == 0:
                return
            else:
                trun_bytes = input_bytes[ret_val:]
        if self.state == packet_state.SCANNING_CHKSUM:
            ret_val = self._scan_checksum(self, input_bytes)
            if ret_val == 0:
                return
            else:
                trun_bytes = input_bytes[ret_val:]
        if self.state == packet_state.READING_DATA:
            ret_val = self._scan_packet_content(self, input_bytes)
            if ret_val == 0:
                return
            else:
                raise NotImplementedError
        if self.state == packet_state.READING_COMPLETE:
            raise NotImplementedError
            

    def _scan_magic_number(self, input_bytes: bytes) -> int:
        for ii in range(0, len(input_bytes)):
            if input_bytes[ii] == SCHEMA_HEADER_MAGIC_NUM[self.bytes_in_state]:
                self.bytes_in_state += 1
            else:
                self.bytes_in_state = 0
                continue
            if self.bytes_in_state >= 4:
                self.state = packet_state.SCANNING_SIZE
                self.bytes_in_state = 0
                return ii+1
        return 0
    
    def _scan_size(self, input_bytes: bytes) -> int:
        for ii in range(0, len(input_bytes)):
            size_value = input_bytes[self.bytes_in_state]
            self.current_header.size_bytes[self.bytes_in_state] = size_value
            self.bytes_in_state += 1
            if self.bytes_in_state >= 4:
                self.state = packet_state.SCANNING_CHKSUM
                self.bytes_in_state = 0
                return ii+1
        return 0
    
    def _scan_checksum(self, input_bytes: bytes) -> int:
        for ii in range(0, len(input_bytes)):
            checksum_value = input_bytes[self.bytes_in_state]
            self.current_header.checksum_bytes[self.bytes_in_state] = checksum_value
            self.bytes_in_state += 1
            if self.bytes_in_state >= 4:
                self.state = packet_state.READING_DATA
                self.bytes_in_state = 0
                return ii+1
        return 0

    def _scan_packet_content(self, input_bytes) -> int:
        for ii in range(0, len(input_bytes)):
            self.working_checksum += input_bytes[ii]
            self.working_buffer.append(input_bytes[ii])
            self.bytes_in_state += 1
            if self.current_header.compare_size(self.bytes_in_state):
                self.state = packet_state.READING_COMPLETE
                return ii
        return 0

