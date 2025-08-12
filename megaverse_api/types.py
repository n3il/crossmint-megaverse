from typing import List, Literal, TypedDict
from dataclasses import dataclass


@dataclass
class Position:
    row: int
    column: int


# Current Map Grid

Color = Literal["blue", "red", "purple", "white"]
Direction = Literal["up", "down", "left", "right"]


class CellMetadataRequired(TypedDict):
    type: int


class CellMetadataOptional(TypedDict, total=False):
    color: Color
    direction: Direction


class CellMetadata(CellMetadataRequired, CellMetadataOptional):
    pass


class MapContent(TypedDict):
    _id: str
    content: List[List[CellMetadata]]
    candidateId: str
    phase: int
    __v: int


class MapResponse(TypedDict):
    map: MapContent


# Goal Grid

CellValue = Literal[
    "SPACE",
    "POLYANET",
    "BLUE_SOLOON",
    "RED_SOLOON",
    "PURPLE_SOLOON",
    "WHITE_SOLOON",
    "UP_COMETH",
    "DOWN_COMETH",
    "LEFT_COMETH",
    "RIGHT_COMETH"
]

MegaVerseGrid = List[List[CellValue]]


class GoalResponse(TypedDict):
    goal: MegaVerseGrid
