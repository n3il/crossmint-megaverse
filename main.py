"""
Main entry point for the Crossmint Megaverse Challenge solution.

This module provides the main functionality to recreate a megaverse according
to a target goal map by comparing the current state with the desired state
and making appropriate API calls to create, modify, or delete celestial objects.
"""

from typing import NoReturn
import sys
import logging

from megaverse_api import MegaverseAPI, ValidationError, APIError
from megaverse_api.types import Position
from megaverse_api.entities import GOAL_VALUE_TO_TYPE, metadata_from_type


# Configure logging with a more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def recreate_expected_goal_map(client: MegaverseAPI) -> None:
    """Recreate the expected goal map by comparing with the current map.

    This function performs a complete analysis and transformation of the
    megaverse by:
    1. Fetching the current state of all cells
    2. Fetching the target goal state
    3. Comparing each cell position
    4. Removing incorrect entities
    5. Creating correct entities

    Args:
        client: Initialized MegaverseAPI client with valid candidate_id

    Raises:
        APIError: If any API call fails
        KeyError: If response data is malformed
        ValidationError: If position data is invalid
    """

    logging.info("📡 Fetching current map...")
    current_map = client.get_current_map()

    logging.info("🎯 Fetching goal map...")
    goal_map = client.get_goal_map()

    logging.info(f"🔭 Calculating the known edges of the megaverse: \
      {len(goal_map)}x{len(goal_map[0])}")

    logging.info("💫 Begin megaverse exploration...")

    for row_idx, row in enumerate(goal_map):
        for col_idx, cell in enumerate(row):
            position = Position(row_idx, col_idx)

            goal_cell_value = goal_map[row_idx][col_idx]
            current_cell_value = metadata_from_type(current_map[row_idx][col_idx])

            if current_cell_value != goal_cell_value:
                logging.info(f"🌀 Anomaly detected at [{row_idx}, {col_idx}]. \
                  Expected {goal_cell_value}, found {current_cell_value}.")

                if current_cell_value != "SPACE":
                    current_metadata = GOAL_VALUE_TO_TYPE[current_cell_value]
                    logging.info(f"💥 Evaporating existing {current_cell_value}...")
                    client.delete_entity_by_metadata(position, current_metadata)

                goal_metadata = GOAL_VALUE_TO_TYPE[goal_cell_value]
                if not goal_metadata:
                    continue

                logging.info(f"✨ Creating {goal_cell_value}...")
                client.create_entity_by_metadata(position, goal_metadata)

    logging.info("🛰️ Megaverse exploration complete!")


def main() -> NoReturn:
    """Main entry point for the application.

    Parses command line arguments, initializes the API client,
    and orchestrates the megaverse recreation process.

    Command line usage:
        python main.py <candidate_id>

    Args:
        None (uses sys.argv)

    Raises:
        SystemExit: If candidate_id is not provided or API calls fail
    """
    # Validate command line arguments
    if len(sys.argv) != 2:
        logging.error("Invalid number of arguments.")
        logging.error("Usage: python main.py <candidate_id>")
        logging.error("Example: python main.py abc123def456")
        sys.exit(1)

    candidate_id = sys.argv[1].strip()

    try:
        logging.info(f"🚀 Initializing Megaverse API client with candidate ID: {candidate_id}")
        client = MegaverseAPI(candidate_id=candidate_id)

        logging.info("🌌 Starting megaverse recreation process...")
        recreate_expected_goal_map(client)

        logging.info("✅ Megaverse recreation completed successfully!")

    except ValidationError as e:
        logging.error(f"❌ Validation error: {e}")
        sys.exit(1)

    except APIError as e:
        logging.error(f"❌ API error: {e}")
        if hasattr(e, 'status_code') and e.status_code:
            logging.error(f"Status code: {e.status_code}")
        sys.exit(1)

    except KeyboardInterrupt:
        logging.warning("🛑 Process interrupted by user")
        sys.exit(1)

    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        logging.error("Please check your candidate ID and network connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()
