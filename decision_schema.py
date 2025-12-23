"""
Decision schema validation for Alpamayo outputs.

Defines the expected JSON structure and validates responses.
"""

import json
from typing import Dict, Any, List

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "frame_id": {"type": "integer"},
        "scene_type": {
            "type": "string",
            "enum": ["intersection", "straight_road", "crosswalk", "parking_lot"]
        },
        "agents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["vehicle", "pedestrian", "cyclist"]},
                    "position": {"type": "string", "enum": ["left", "right", "ahead", "crossing"]}
                },
                "required": ["type", "position"]
            }
        },
        "traffic_light": {
            "type": "string",
            "enum": ["red", "yellow", "green", "unknown"]
        },
        "hazards": {
            "type": "array",
            "items": {"type": "string"}
        },
        "decision": {
            "type": "string",
            "enum": ["accelerate", "maintain_speed", "slow_down", "brake", "stop", "yield"]
        },
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "reason": {"type": "string"}
    },
    "required": ["scene_type", "agents", "traffic_light", "hazards", "decision", "confidence", "reason"]
}

def validate_decision(decision_json: str) -> Dict[str, Any]:
    """
    Validate a decision JSON string against the schema.

    Args:
        decision_json (str): JSON string to validate

    Returns:
        dict: Parsed and validated decision

    Raises:
        ValueError: If validation fails
    """
    try:
        decision = json.loads(decision_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Basic validation (in production, use jsonschema library)
    required_fields = DECISION_SCHEMA["properties"].keys()
    for field in required_fields:
        if field not in decision:
            raise ValueError(f"Missing required field: {field}")

    # Validate enums
    if decision["scene_type"] not in DECISION_SCHEMA["properties"]["scene_type"]["enum"]:
        raise ValueError(f"Invalid scene_type: {decision['scene_type']}")

    if decision["traffic_light"] not in DECISION_SCHEMA["properties"]["traffic_light"]["enum"]:
        raise ValueError(f"Invalid traffic_light: {decision['traffic_light']}")

    if decision["decision"] not in DECISION_SCHEMA["properties"]["decision"]["enum"]:
        raise ValueError(f"Invalid decision: {decision['decision']}")

    # Validate agents
    for agent in decision["agents"]:
        if agent["type"] not in DECISION_SCHEMA["properties"]["agents"]["items"]["properties"]["type"]["enum"]:
            raise ValueError(f"Invalid agent type: {agent['type']}")
        if agent["position"] not in DECISION_SCHEMA["properties"]["agents"]["items"]["properties"]["position"]["enum"]:
            raise ValueError(f"Invalid agent position: {agent['position']}")

    # Validate confidence
    if not (0.0 <= decision["confidence"] <= 1.0):
        raise ValueError(f"Confidence must be between 0.0 and 1.0: {decision['confidence']}")

    return decision
