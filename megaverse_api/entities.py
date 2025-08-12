from typing import Optional, Dict, Any, Union

"""
Entity definitions and metadata for Megaverse objects.
Contains cell metadata, type mappings, and utility functions.
"""

# Cell metadata with visual representations and properties
GOAL_VALUE_TO_TYPE = {
    "SPACE": None,
    "POLYANET": {"type": 0},
    "BLUE_SOLOON": {"type": 1, "color": "blue"},
    "RED_SOLOON": {"type": 1, "color": "red"},
    "PURPLE_SOLOON": {"type": 1, "color": "purple"},
    "WHITE_SOLOON": {"type": 1, "color": "white"},
    "UP_COMETH": {"type": 2, "direction": "up"},
    "DOWN_COMETH": {"type": 2, "direction": "down"},
    "LEFT_COMETH": {"type": 2, "direction": "left"},
    "RIGHT_COMETH": {"type": 2, "direction": "right"}
}

# Type mapping for API responses (numeric types to string names)
TYPE_TO_GOAL_REF = {
    0: "POLYANET",
    1: {
        "blue": "BLUE_SOLOON",
        "red": "RED_SOLOON",
        "purple": "PURPLE_SOLOON",
        "white": "WHITE_SOLOON",
    },
    2: {
        "up": "UP_COMETH",
        "down": "DOWN_COMETH",
        "left": "LEFT_COMETH",
        "right": "RIGHT_COMETH",
    }
}


def metadata_from_type(cell_dict: Optional[Dict[str, Any]]) -> str:
    """
    Convert API response cell data to metadata string.

    Args:
        cell_dict: Dictionary with 'type' and optional 'color'/'direction' keys,
                  or None for empty space

    Returns:
        String representation of the cell type (e.g., "POLYANET", "BLUE_SOLOON")

    Raises:
        KeyError: If required keys are missing from cell_dict
        ValueError: If cell_dict contains invalid type or attribute values
    """
    if cell_dict is None:
        return "SPACE"

    cell_type = cell_dict.get('type')
    if cell_type is None:
        raise KeyError("Missing 'type' key in cell_dict")

    if cell_type == 0:
        return TYPE_TO_GOAL_REF[0]
    elif cell_type == 1:
        color = cell_dict.get('color')
        if color is None:
            raise KeyError("Missing 'color' key for Soloon type")
        if color not in TYPE_TO_GOAL_REF[1]:
            raise ValueError(f"Invalid color '{color}' for Soloon")
        return TYPE_TO_GOAL_REF[1][color]
    elif cell_type == 2:
        direction = cell_dict.get('direction')
        if direction is None:
            raise KeyError("Missing 'direction' key for Cometh type")
        if direction not in TYPE_TO_GOAL_REF[2]:
            raise ValueError(f"Invalid direction '{direction}' for Cometh")
        return TYPE_TO_GOAL_REF[2][direction]
    else:
        raise ValueError(f"Invalid cell type: {cell_type}")
