import pytest
from megaverse_api.types import Position


class TestPosition:
    def test_position_creation(self):
        pos = Position(5, 10)
        assert pos.row == 5
        assert pos.column == 10

    def test_position_equality(self):
        pos1 = Position(1, 2)
        pos2 = Position(1, 2)
        pos3 = Position(2, 1)
        assert pos1 == pos2
        assert pos1 != pos3

    def test_position_with_zero_values(self):
        pos = Position(0, 0)
        assert pos.row == 0
        assert pos.column == 0