"""
dist_schemas.py - JSON Schemas for various RPC/peer-tasks.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

from jsonschema import validate

ACK_PACKET = {"type" : "object:",
                   "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "acked_packet_id": {"type": "string"},
                   },
                   "required": ["packet_type","packet_id","acked_packet_id"],
                   "additionalProperties": False
                   }

GET_RESC_AT_KEY = {"type" : "object:",
                   "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "resource_key": {"type": "string"},
                       "query_origin": {"type": "integer"}
                   },
                   "required": ["packet_type","packet_id","resource_key","query_origin"],
                   "additionalProperties": False
                   }
                   
PASS_RESC_TO_PEER = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "resource_key": {"type": "string"},
                       "fragment_num": {"type": "integer"},
                       "total_fragments": {"type" : "integer"},
                       "fragment_data": {"type" : "string"}
                   },
                   "required": ["packet_type", "packet_id", "resource_key","fragment_num", "total_fragments", "fragment_data"],
                   "additionalProperties": False}

REREQUEST_MISSING_FRAGMENT = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "resource_key": {"type": "string"},
                       "fragment_num": {"type": "integer"},
                   },
                   "required": ["packet_type", "packet_id", "resource_key","fragment_num"],
                   "additionalProperties": False}

GET_PEER_NETWORK_INFO = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "peer_id": {"type": "integer"},
                   },
                   "required": ["packet_type", "packet_id", "peer_id"],
                   "additionalProperties": False}

PEER_NETWORK_INFO = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "peer_id": {"type": "integer"},
                       "network_address": {"type": "string"},
                   },
                   "required": ["packet_type", "packet_id", "peer_id","network_address"],
                   "additionalProperties": False}

FIND_NEXT_AVAILABLE_KEY = {}

PROVIDED_NEXT_AVAILABLE_KEY = {}

SCHEMA_HEADER_MAGIC_NUM = b'\x4d\x53\x69\x6d'
SCHEMA_MAX_PAYLOAD_SIZE = 2048

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

class full_schema_packet():

    def __init__(self, header, content):
        self.header = header
        self.raw_content = content
        self.decoded_content = None
        self.decode_dict = {
            "get_resource": GET_RESC_AT_KEY,
            "pass_resource": PASS_RESC_TO_PEER,
            "get_peer_info": GET_PEER_NETWORK_INFO,
            "find_next_key": FIND_NEXT_AVAILABLE_KEY
        }
        
    def _check_conformity(self) -> bool:
        if len(self.content.encode('utf-8')) > MAX_JSON_SIZE:
            raise ValueError("Exceeds max size")
        try:
            self.decoded_content = json.loads(self.content)
            return True
        except json.JSONDecodeError as err:
            print(f"Malicious or malformed JSON detected: {err}")
            return False

    def get_decoded_content(self) -> dict:
        if not self._check_conformity():
            return {"type":"error - invalid json"}
        # Check for initial schema hint, then validate against it.
        if "packet_type" not in self.decoded_content:
            return {"type":"error - missing type"}
        target_type = self.decoded_content["type"]
        if target_type not in self.decode_dict:
            return {"type":"error - non-supported type"}
        target_schema = self.decode_dict[target_type]
        try:
            # This will pass silently if the data matches the schema
            validate(instance=self.raw_content, schema=target_schema)
        except jsonschema.exceptions.ValidationError as e:
            return {"type":"error - failed validation"}
        except jsonschema.exceptions.SchemaError as e:
            return {"type":"error - schema invalid"}
        return self.decoded_content

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
        self.processed_packet = None

    def get_processed_packet(self) -> full_schema_packet:
        return_packet = self.processed_packet
        self.processed_packet = None
        return return_packet

    def scan_and_process(self, input_bytes: bytes) -> int:
        trun_bytes = bytearray(input_bytes)
        bytes_processed = 0
        if self.state == packet_state.SCANNING_MN:
            bytes_processed = self._scan_magic_number(trun_bytes)
            if bytes_processed == 0:
                return 0
            else:
                trun_bytes = trun_bytes[bytes_processed:]
        if self.state == packet_state.SCANNING_SIZE:
            bytes_processed = self._scan_size(trun_bytes)
            if bytes_processed == 0:
                return 0
            else:
                trun_bytes = trun_bytes[bytes_processed:]
        if self.state == packet_state.SCANNING_CHKSUM:
            bytes_processed = self._scan_checksum(self, trun_bytes)
            if bytes_processed == 0:
                return 0
            else:
                trun_bytes = trun_bytes[bytes_processed:]
        if self.state == packet_state.READING_DATA:
            bytes_processed = self._scan_packet_content(self, trun_bytes)
            if bytes_processed == 0:
                return 0
            else:
                trun_bytes = trun_bytes[bytes_processed:]
        if self.state == packet_state.READING_COMPLETE:
            if self._validate_packet():
                self.processed_packet = full_schema_packet(self.current_header, self.working_buffer)
            self._reset_state()
            return len(input_bytes) - len(trun_bytes)
            

    def _scan_magic_number(self, input_bytes: bytes) -> int:
        for ii in range(0, len(input_bytes)):
            if input_bytes[ii] == SCHEMA_HEADER_MAGIC_NUM[self.bytes_in_state]:
                self.bytes_in_state += 1
            else:
                self.bytes_in_state = 0
                continue
            if self.bytes_in_state == 4:
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
                self.bytes_in_state = 0
                return ii+1
        return 0
    
    def _validate_packet(self) -> bool:
        return self.current_header.compare_checksum(self.working_checksum)

