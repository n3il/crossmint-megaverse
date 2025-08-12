import requests
from requests_ratelimiter import LimiterSession
from typing import Optional, Dict, Any
import time
import logging
from functools import wraps, lru_cache


class MegaverseAPIError(Exception):
    """Base exception class for Megaverse API errors."""
    pass


class ValidationError(MegaverseAPIError):
    """Raised when input validation fails."""
    pass


class APIError(MegaverseAPIError):
    """Raised when API request fails."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""
    pass


def validate_position(func):
    """Decorator to validate Position objects."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Find position argument
        for arg in args[1:]:  # Skip self
            if hasattr(arg, 'row') and hasattr(arg, 'column'):
                if not isinstance(arg.row, int) or not isinstance(arg.column, int):
                    raise ValidationError("Position row and column must be integers")
                if arg.row < 0 or arg.column < 0:
                    raise ValidationError("Position row and column must be non-negative")
        return func(*args, **kwargs)
    return wrapper

from .polyanets import PolyanetMixin
from .soloons import SoloonMixin
from .comeths import ComethMixin
from .maps import MapMixin


class MegaverseAPI(
    PolyanetMixin, SoloonMixin, ComethMixin, MapMixin
):
    """Crossmint Megaverse API client with comprehensive error handling.

    This class provides a complete interface to the Crossmint Megaverse Challenge API.
    It includes functionality for:
    - Creating, deleting Polyanets, Soloons, and Comeths
    - Retrieving current and goal maps
    - Rate limiting and retry logic
    - Input validation and error handling

    The client automatically handles:
    - Rate limiting (1 request per second)
    - HTTP timeouts (30 seconds)
    - Automatic retries on rate limit exceeded
    - SSL verification (configurable)

    Example:
        >>> client = MegaverseAPI('your-candidate-id')
        >>> current_map = client.get_current_map()
        >>> goal_map = client.get_goal_map()
        >>> client.create_polyanet(Position(5, 5))

    Attributes:
        BASE_URL: The base URL for the Crossmint API
        candidate_id: Your unique candidate identifier
        verify_ssl: Whether to verify SSL certificates
        session: Rate-limited HTTP session
    """

    BASE_URL = "https://challenge.crossmint.io/api"

    def __init__(self, candidate_id: str, verify_ssl: bool = False):
        """Initialize the Megaverse API client.

        Args:
            candidate_id: Your unique candidate ID for the challenge.
                         Must be a non-empty string.
            verify_ssl: Whether to verify SSL certificates. Defaults to False
                       for development environments.

        Raises:
            ValidationError: If candidate_id is not provided, empty, or invalid.

        Example:
            >>> client = MegaverseAPI('abc123def456')
            >>> client = MegaverseAPI('test-id', verify_ssl=True)
        """
        if not candidate_id or not isinstance(candidate_id, str):
            raise ValidationError("candidate_id must be a non-empty string")
        if len(candidate_id.strip()) == 0:
            raise ValidationError("candidate_id cannot be whitespace only")
        self.candidate_id = candidate_id
        self.verify_ssl = verify_ssl

        # Cache for storing maps to avoid repeated API calls
        self._goal_map_cache: Optional[Dict[str, Any]] = None
        self._current_map_cache: Optional[Dict[str, Any]] = None
        self._cache_timeout = 300  # 5 minutes
        self._last_cache_time = 0

        # Create rate-limited session with exponential backoff
        self.session = LimiterSession(per_second=1)

        if not self.verify_ssl:
            requests.packages.urllib3.disable_warnings()

    def _is_cache_valid(self) -> bool:
        """Check if the current cache is still valid."""
        return (time.time() - self._last_cache_time) < self._cache_timeout

    def _clear_cache(self) -> None:
        """Clear all cached data."""
        self._goal_map_cache = None
        self._current_map_cache = None
        self._last_cache_time = 0

    def _update_cache_time(self) -> None:
        """Update the cache timestamp."""
        self._last_cache_time = time.time()

    def _invalidate_current_map_cache(self) -> None:
        """Invalidate current map cache after state changes."""
        self._current_map_cache = None

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Megaverse API with comprehensive error handling.

        This method handles all HTTP communication with the API, including:
        - Input validation
        - Automatic candidate ID injection
        - Rate limiting and retries
        - Comprehensive error handling
        - Response parsing

        Args:
            method: HTTP method. Must be one of: GET, POST, DELETE, PUT, PATCH
            endpoint: API endpoint path starting with '/'. Example: '/polyanets'
            data: Optional request body data. Will be JSON-encoded.
                  candidateId is automatically added.
            params: Optional query parameters for GET requests.

        Returns:
            Parsed JSON response from the API as a dictionary.
            Empty dict if response has no content.

        Raises:
            ValidationError: If method or endpoint parameters are invalid
            APIError: If the HTTP request fails for any reason
            RateLimitError: If rate limit is exceeded (after retries)

        Example:
            >>> response = client._make_request('POST', '/polyanets',
            ...                                 {'row': 5, 'column': 5})
            >>> response = client._make_request('GET', '/map/candidate123/goal')
        """
        # Validate inputs
        if method not in ["GET", "POST", "DELETE", "PUT", "PATCH"]:
            raise ValidationError(f"Invalid HTTP method: {method}")
        if not endpoint or not isinstance(endpoint, str):
            raise ValidationError("Endpoint must be a non-empty string")
        if not endpoint.startswith("/"):
            raise ValidationError("Endpoint must start with '/'")

        url = f"{self.BASE_URL}{endpoint}"

        # Always include candidateId in the request
        if data is None:
            data = {}
        data = data.copy()  # Create a copy to avoid modifying the original
        data["candidateId"] = self.candidate_id

        try:
            response = self.session.request(
                method=method,
                headers={"Content-Type": "application/json"},
                url=url,
                json=data,
                params=params,
                verify=self.verify_ssl,
                timeout=30  # Add timeout
            )

            # Handle specific status codes
            if response.status_code == 429:
                logging.warning("⚡️ Rate limit exceeded. Retrying in 5 seconds...")
                time.sleep(5)
                return self._make_request(method, endpoint, data, params)

            # Raise for other HTTP errors
            response.raise_for_status()

            # Return JSON if response is not empty
            return response.json() if response.content else {}

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {response.status_code}: {e}"
            if hasattr(response, 'text'):
                error_msg += f" - {response.text[:200]}"
            if response.status_code == 429:
                raise RateLimitError(error_msg, response.status_code, response.text)
            else:
                raise APIError(error_msg, response.status_code, response.text)

        except requests.exceptions.Timeout:
            raise APIError("Request timed out after 30 seconds")

        except requests.exceptions.ConnectionError as e:
            raise APIError(f"Connection error: {e}")

        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")

        except ValueError as e:
            # JSON decode error
            raise APIError(f"Invalid JSON response: {e}")

    def delete_entity_by_metadata(self, position, metadata: Dict[str, Any]) -> None:
        """Delete an entity based on its metadata type.

        Args:
            position: Position object with row and column
            metadata: Entity metadata dict containing 'type' and optional attributes
        """
        entity_type = metadata['type']
        if entity_type == 0:
            self.delete_polyanet(position)
        elif entity_type == 1:
            self.delete_soloon(position)
        elif entity_type == 2:
            self.delete_cometh(position)

    def create_entity_by_metadata(self, position, metadata: Dict[str, Any]) -> None:
        """Create an entity based on its metadata type.

        Args:
            position: Position object with row and column
            metadata: Entity metadata dict containing 'type' and optional attributes
        """
        entity_type = metadata['type']
        if entity_type == 0:
            self.create_polyanet(position)
        elif entity_type == 1:
            self.create_soloon(position, metadata['color'])
        elif entity_type == 2:
            self.create_cometh(position, metadata['direction'])
