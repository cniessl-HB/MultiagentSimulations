"""
dist_schemas.py - JSON Schemas for various RPC/peer-tasks.

Copyright 2026 - Christopher T Niessl

See LICENSE.txt for usage.
"""

PACK_TYPE_ACK_PACKET = "ack_packet"
ACK_PACKET = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string", "default": PACK_TYPE_ACK_PACKET},
        "packet_id": {"type": "string", "default": ""},
        "acked_packet_id": {"type": "string", "default": ""},
    },
    "required": ["packet_type", "packet_id", "acked_packet_id"],
    "additionalProperties": False,
}

PACK_GET_RESC_AT_KEY = "get_resource"
GET_RESC_AT_KEY = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string", "default": PACK_GET_RESC_AT_KEY},
        "packet_id": {"type": "string", "default": ""},
        "resource_key": {"type": "string", "default":""},
        "query_origin": {"type": "integer", "default": 0},
    },
    "required": ["packet_type", "packet_id", "resource_key", "query_origin"],
    "additionalProperties": False,
}

PACK_RESC_TO_PEER = "pass_resource"
PASS_RESC_TO_PEER = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string", "default": PACK_PASS_RESC_TO_PEER},
        "packet_id": {"type": "string", "default": ""},
        "resource_key": {"type": "string", "default": ""},
        "fragment_num": {"type": "integer", "default": 0},
        "total_fragments": {"type": "integer", "default": 1},
        "fragment_data": {"type": "string", "default": ""},
    },
    "required": [
        "packet_type",
        "packet_id",
        "resource_key",
        "fragment_num",
        "total_fragments",
        "fragment_data",
    ],
    "additionalProperties": False,
}

PACK_REREQUEST_MISSING_FRAGMENT = "request_missing_frag"
REREQUEST_MISSING_FRAGMENT = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string", "default": PACK_REREQUEST_MISSING_FRAGMENT},
        "packet_id": {"type": "string", "default": ""},
        "resource_key": {"type": "string", "default": ""},
        "fragment_num": {"type": "integer", "default": 0},
    },
    "required": ["packet_type", "packet_id", "resource_key", "fragment_num"],
    "additionalProperties": False,
}

PACK_TYPE_GET_PEER_NETWORK_INFO = "get_peer_info"
GET_PEER_NETWORK_INFO = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string", "default": PACK_TYPE_GET_PEER_NETWORK_INFO},
        "packet_id": {"type": "string", "default": ""},
        "target_peer_id": {"type": "integer", "default": -1},
    },
    "required": ["packet_type", "packet_id", "target_peer_id"],
    "additionalProperties": False,
}

PACK_TYPE_PEER_NETWORK_INFO = "peer_info"
PEER_NETWORK_INFO = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string"},
        "packet_id": {"type": "string"},
        "target_peer_id": {"type": "integer"},
        "network_address": {"type": "string"},
    },
    "required": ["packet_type", "packet_id", "target_peer_id", "network_address"],
    "additionalProperties": False,
}
PACK_FIND_NEXT_AVAILABLE_KEY = "find_next_key"
FIND_NEXT_AVAILABLE_KEY = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string"},
        "packet_id": {"type": "string"},
        "max_key_hint": {"type": "int"},
    },
    "required": ["packet_type", "packet_id", "max_key_hint"],
    "additionalProperties": False,
}

PROVIDED_NEXT_AVAILABLE_KEY = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string"},
        "packet_id": {"type": "string"},
        "new_key_granted": {"type": "int"},
    },
    "required": ["packet_type", "packet_id", "new_key_granted"],
    "additionalProperties": False,
}

PUSH_RESC_REQUEST = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string"},
        "packet_id": {"type": "string"},
        "resource_key": {"type": "string"},
        "total_fragments": {"type": "integer"},
    },
    "required": ["packet_type", "packet_id", "resource_key", "total_fragments"],
    "additionalProperties": False,
}

READY_TO_REC_RESC = {
    "type": "object:",
    "properties": {
        "packet_type": {"type": "string"},
        "packet_id": {"type": "string"},
        "resource_key": {"type": "string"},
        "push_packet_id": {"type": "string"},
    },
    "required": ["packet_type", "packet_id", "resource_key", "push_packet_id"],
    "additionalProperties": False,
}


def get_dist_schema_dict() -> dict:
    decode_dict = {
        PACK_TYPE_ACK_PACKET: ACK_PACKET,
        PACK_GET_RESC_AT_KEY: GET_RESC_AT_KEY,
        PACK_RESC_TO_PEER: PASS_RESC_TO_PEER,
        PACK_REREQUEST_MISSING_FRAGMENT: REREQUEST_MISSING_FRAGMENT,
        PACK_TYPE_GET_PEER_NETWORK_INFO : GET_PEER_NETWORK_INFO,
        PACK_TYPE_PEER_NETWORK_INFO: PEER_NETWORK_INFO,
        PACK_FIND_NEXT_AVAILABLE_KEY: FIND_NEXT_AVAILABLE_KEY,
        "the_next_key": PROVIDED_NEXT_AVAILABLE_KEY,
        "push_resource": PUSH_RESC_REQUEST,
        "ready_to_receive": READY_TO_REC_RESC,
    }
    return decode_dict
