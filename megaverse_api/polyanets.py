from typing import Dict, Any, TYPE_CHECKING
from .types import Position

if TYPE_CHECKING:
    from .base import MegaverseAPI, validate_position
else:
    from .base import validate_position


class PolyanetMixin:
    """Mixin class for Polyanet-related API endpoints."""

    @validate_position
    def create_polyanet(self: 'MegaverseAPI', position: Position) -> Dict[str, Any]:
        """Create a new Polyanet at the specified position.

        Args:
            position: The position where to create the Polyanet

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column
        }
        result = self._make_request("POST", "/polyanets", data=data)
        self._invalidate_current_map_cache()
        return result

    @validate_position
    def delete_polyanet(self: 'MegaverseAPI', position: Position) -> Dict[str, Any]:
        """Delete a Polyanet at the specified position.

        Args:
            position: The position where to delete the Polyanet

        Returns:
            API response dictionary

        Raises:
            requests.HTTPError: If the API request fails
        """
        data = {
            "row": position.row,
            "column": position.column
        }
        result = self._make_request("DELETE", "/polyanets", data=data)
        self._invalidate_current_map_cache()
        return result