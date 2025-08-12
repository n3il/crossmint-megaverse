from typing import Dict, Any, TYPE_CHECKING
import time
from .types import MegaVerseGrid, GoalResponse, MapResponse

if TYPE_CHECKING:
    from .base import MegaverseAPI


class MapMixin:
    """Mixin class for Map-related API endpoints.

    This mixin provides methods to retrieve both goal and current maps
    from the Crossmint Megaverse API.
    """

    def _get_goal_response(self: 'MegaverseAPI') -> GoalResponse:
        """Get the raw goal response from the API with caching.

        Uses cached data if available and valid, otherwise fetches fresh data.

        Returns:
            Complete goal response including metadata

        Raises:
            requests.HTTPError: If the API request fails
        """
        if self._goal_map_cache and self._is_cache_valid():
            return self._goal_map_cache

        response = self._make_request("GET", f"/map/{self.candidate_id}/goal")
        self._goal_map_cache = response
        self._update_cache_time()
        return response

    def get_goal_map(self: 'MegaverseAPI') -> MegaVerseGrid:
        """Retrieve the goal map for the current challenge phase.

        The goal map represents the target configuration that the megaverse
        should match. It contains string representations of each cell type.

        Returns:
            The goal map as a 2D list of cell values

        Raises:
            requests.HTTPError: If the API request fails
            KeyError: If the response doesn't contain the expected 'goal' key
        """
        return self._get_goal_response()['goal']

    def _get_current_map_response(self: 'MegaverseAPI') -> MapResponse:
        """Get the raw current map response from the API with caching.

        Note: Current map caching is more aggressive since it changes frequently.
        Cache is invalidated after any create/delete operation.

        Returns:
            Complete current map response including metadata

        Raises:
            requests.HTTPError: If the API request fails
        """
        # Current map changes frequently, so we use a shorter cache time
        if self._current_map_cache and (time.time() - self._last_cache_time) < 30:
            return self._current_map_cache

        response = self._make_request("GET", f"/map/{self.candidate_id}")
        self._current_map_cache = response
        self._update_cache_time()
        return response

    def get_current_map(self: 'MegaverseAPI') -> MegaVerseGrid:
        """Retrieve the current map for the current challenge phase.

        The current map represents the actual state of the megaverse.
        Each cell contains metadata about the entity at that position.

        Returns:
            The current map as a 2D list of cell metadata dictionaries

        Raises:
            requests.HTTPError: If the API request fails
            KeyError: If the response doesn't contain expected nested keys
        """
        return self._get_current_map_response()['map']['content']
