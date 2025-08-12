# 🌌 Crossmint Megaverse Challenge

An elegant Python solution for the Crossmint Megaverse Challenge that recreates celestial patterns by managing Polyanets, Soloons, and Comeths through API interactions.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository>
cd crossmint
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the megaverse recreation
python main.py <your-candidate-id>
```

## 🪐 What it Does

The solution analyzes the target megaverse pattern and intelligently:
- 🔍 **Compares** current state vs desired goal
- 💥 **Removes** incorrect celestial objects
- ✨ **Creates** required objects in correct positions
- 🛡️ **Handles** rate limits and API errors gracefully

### Supported Celestial Objects
- **🌟 Polyanets** - Basic stellar objects
- **🌙 Soloons** - Colored moons (blue, red, purple, white)
- **☄️ Comeths** - Directional comets (up, down, left, right)

## 🧪 Testing

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## 🏗️ Architecture

```
megaverse_api/
├── base.py        # Core API client with rate limiting
├── entities.py    # Object type mappings and metadata
├── types.py       # Data structures and type definitions
├── polyanets.py   # Polyanet operations
├── soloons.py     # Soloon operations
├── comeths.py     # Cometh operations
└── maps.py        # Map retrieval operations
```

## 📋 Example Output

```
2024-01-01 12:00:00 - INFO - 🚀 Initializing Megaverse API client
2024-01-01 12:00:01 - INFO - 📡 Fetching current map...
2024-01-01 12:00:02 - INFO - 🎯 Fetching goal map...
2024-01-01 12:00:03 - INFO - 🔭 Calculating extents of the megaverse: 11x11
2024-01-01 12:00:04 - INFO - 🌀 Anomaly detected at [2, 3]. Expected POLYANET, found SPACE.
2024-01-01 12:00:05 - INFO - ✨ Creating POLYANET...
2024-01-01 12:00:06 - INFO - ✅ Megaverse recreation completed successfully!
```