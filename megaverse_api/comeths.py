from typing import Dict, Any, TYPE_CHECKING
from .types import Position, Direction

if TYPE_CHECKING:
    from .base import MegaverseAPI, validate_position
else:
    from .base import validate_position


class ComethMixin:
    """Mixin class for Cometh-related API endpoints."""

    @validate_position
    def create_cometh(self: 'MegaverseAPI', position: Position, direction: Direction) -> Dict[str, Any]:
        """Create a new Cometh at the specified position with the given direction.

        Args:
            position: The position where to create the Cometh
            direction: The direction of the Cometh to create

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column,
            "direction": direction
        }
        result = self._make_request("POST", "/comeths", data=data)
        self._invalidate_current_map_cache()
        return result

    @validate_position
    def delete_cometh(self: 'MegaverseAPI', position: Position) -> Dict[str, Any]:
        """Delete a Cometh at the specified position.

        Args:
            position: The position where to delete the Cometh

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column
        }
        result = self._make_request("DELETE", "/comeths", data=data)
        self._invalidate_current_map_cache()
        return result
