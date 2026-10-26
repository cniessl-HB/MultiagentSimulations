"""
dist_schemas.py - JSON Schemas for various RPC/peer-tasks.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

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
                       "target_peer_id": {"type": "integer"},
                   },
                   "required": ["packet_type", "packet_id", "target_peer_id"],
                   "additionalProperties": False}

PEER_NETWORK_INFO = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "target_peer_id": {"type": "integer"},
                       "network_address": {"type": "string"},
                   },
                   "required": ["packet_type", "packet_id", "target_peer_id","network_address"],
                   "additionalProperties": False}

FIND_NEXT_AVAILABLE_KEY = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "max_key_hint": {"type": "int"},
                   },
                   "required": ["packet_type", "packet_id", "max_key_hint"],
                   "additionalProperties": False}

PROVIDED_NEXT_AVAILABLE_KEY = {"type" : "object:",
                     "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "new_key_granted": {"type": "int"},
                   },
                   "required": ["packet_type", "packet_id", "new_key_granted"],
                   "additionalProperties": False}

PUSH_RESC_REQUEST = {"type" : "object:",
                   "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "resource_key": {"type": "string"},
                       "total_fragments": {"type": "integer"}
                   },
                   "required": ["packet_type","packet_id","resource_key","total_fragments"],
                   "additionalProperties": False
                   }

READY_TO_REC_RESC = {"type" : "object:",
                   "properties":{
                       "packet_type": {"type": "string"},
                       "packet_id": {"type": "string"},
                       "resource_key": {"type": "string"},
                       "push_packet_id": {"type": "string"}
                   },
                   "required": ["packet_type","packet_id","resource_key","push_packet_id"],
                   "additionalProperties": False
                   }

def get_dist_schema_dict() -> dict:
    self.decode_dict = {
        "get_resource": GET_RESC_AT_KEY,
        "pass_resource": PASS_RESC_TO_PEER,
        "get_peer_info": GET_PEER_NETWORK_INFO,
        "find_next_key": FIND_NEXT_AVAILABLE_KEY
    }
