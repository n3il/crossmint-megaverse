import pytest
from megaverse_api.entities import metadata_from_type, GOAL_VALUE_TO_TYPE


class TestMetadataFromType:
    def test_space_cell(self):
        assert metadata_from_type(None) == "SPACE"

    def test_polyanet_cell(self):
        assert metadata_from_type({"type": 0}) == "POLYANET"

    def test_soloon_cells(self):
        assert metadata_from_type({"type": 1, "color": "blue"}) == "BLUE_SOLOON"
        assert metadata_from_type({"type": 1, "color": "red"}) == "RED_SOLOON"
        assert metadata_from_type({"type": 1, "color": "purple"}) == "PURPLE_SOLOON"
        assert metadata_from_type({"type": 1, "color": "white"}) == "WHITE_SOLOON"

    def test_cometh_cells(self):
        assert metadata_from_type({"type": 2, "direction": "up"}) == "UP_COMETH"
        assert metadata_from_type({"type": 2, "direction": "down"}) == "DOWN_COMETH"
        assert metadata_from_type({"type": 2, "direction": "left"}) == "LEFT_COMETH"
        assert metadata_from_type({"type": 2, "direction": "right"}) == "RIGHT_COMETH"

    def test_missing_type_raises_error(self):
        with pytest.raises(KeyError, match="Missing 'type' key"):
            metadata_from_type({"color": "blue"})

    def test_missing_color_for_soloon_raises_error(self):
        with pytest.raises(KeyError, match="Missing 'color' key"):
            metadata_from_type({"type": 1})

    def test_invalid_color_raises_error(self):
        with pytest.raises(ValueError, match="Invalid color 'invalid'"):
            metadata_from_type({"type": 1, "color": "invalid"})

    def test_missing_direction_for_cometh_raises_error(self):
        with pytest.raises(KeyError, match="Missing 'direction' key"):
            metadata_from_type({"type": 2})

    def test_invalid_direction_raises_error(self):
        with pytest.raises(ValueError, match="Invalid direction 'invalid'"):
            metadata_from_type({"type": 2, "direction": "invalid"})

    def test_invalid_type_raises_error(self):
        with pytest.raises(ValueError, match="Invalid cell type: 999"):
            metadata_from_type({"type": 999})


class TestGoalValueToType:
    def test_goal_value_mappings(self):
        assert GOAL_VALUE_TO_TYPE["SPACE"] is None
        assert GOAL_VALUE_TO_TYPE["POLYANET"] == {"type": 0}
        assert GOAL_VALUE_TO_TYPE["BLUE_SOLOON"] == {"type": 1, "color": "blue"}
        assert GOAL_VALUE_TO_TYPE["UP_COMETH"] == {"type": 2, "direction": "up"}