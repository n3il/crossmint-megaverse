from typing import Dict, Any, TYPE_CHECKING
from .types import Position, Color

if TYPE_CHECKING:
    from .base import MegaverseAPI, validate_position
else:
    from .base import validate_position


class SoloonMixin:
    """Mixin class for Soloon-related API endpoints."""

    @validate_position
    def create_soloon(self: 'MegaverseAPI', position: Position, color: Color) -> Dict[str, Any]:
        """Create a new Soloon at the specified position with the given color.

        Args:
            position: The position where to create the Soloon
            color: The color of the Soloon to create

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column,
            "color": color
        }
        result = self._make_request("POST", "/soloons", data=data)
        self._invalidate_current_map_cache()
        return result

    @validate_position
    def delete_soloon(self: 'MegaverseAPI', position: Position) -> Dict[str, Any]:
        """Delete a Soloon at the specified position.

        Args:
            position: The position where to delete the Soloon

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column
        }
        result = self._make_request("DELETE", "/soloons", data=data)
        self._invalidate_current_map_cache()
        return result