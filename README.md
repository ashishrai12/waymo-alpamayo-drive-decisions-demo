# Alpamayo R1 Autonomous Driving Demo

A minimal demo showcasing Alpamayo R1's video-language-action reasoning capabilities using Waymo Open Dataset camera data.

<img width="1533" height="839" alt="{30C2EBF6-DAC6-4C21-990D-CF81B2077BEB}" src="https://github.com/user-attachments/assets/acc53850-d442-4441-bc0a-10f788d4c918" />


## Overview

This demo demonstrates high-level autonomous driving decision making through:
- **Perception**: Scene analysis from camera frames
- **Reasoning**: Language-based decision making
- **Action**: Discrete driving actions
- **Explanation**: Human-readable reasoning

## Features

- Modular Python implementation
- Mock Alpamayo R1 interface (easily swappable with real model)
- OpenCV-based visualization with frame-by-frame playback
- JSON-structured decision outputs
- Urban driving scenarios (intersections, pedestrians, traffic)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install opencv-python numpy
   ```

## Usage

### Local Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up PYTHONPATH:
   ```bash
   # Windows
   $env:PYTHONPATH = "src"
   # Linux/macOS
   export PYTHONPATH=$PYTHONPATH:$(pwd)/src
   ```

### Run Demo

```bash
python main.py --video_path data/your_waymo_video.mp4 --fps 1
```

### Docker Support

Build and run using Docker:

```bash
docker build -t alpamayo-demo .
docker run -it alpamayo-demo
```

## Project Structure

```text
├── src/
│   └── alpamayo_demo/      # Core package
│       ├── core/           # Logic and schemas
│       ├── utils/          # Data loading and visualization
│       └── pipeline.py     # Pipeline orchestration
├── tests/                  # Unit and integration tests
├── scripts/                # Utility scripts (CI, setup)
├── data/                   # Dataset folder
├── Dockerfile              # Containerization
└── main.py                 # Entry point
```

## Architecture

The project follows a modular design:

- **`AlpamayoPolicy`**: The core decision-making interface.
- **`DecisionSchema`**: Strict validation for model outputs.
- **`DataLoader`**: Optimized frame sampling from high-frequency Waymo data.
- **`Visualization`**: Real-time decision delivery HUD.

### Decision Format

Each timestep outputs JSON with:
```json
{
  "frame_id": 0,
  "scene_type": "intersection",
  "agents": [{"type": "pedestrian", "position": "crossing"}],
  "traffic_light": "red",
  "hazards": ["pedestrian crossing"],
  "decision": "stop",
  "confidence": 0.89,
  "reason": "Pedestrian detected at crosswalk"
}
```

### Actions

- `accelerate`: Increase speed
- `maintain_speed`: Keep current speed
- `slow_down`: Gradually reduce speed
- `brake`: Hard stop
- `stop`: Come to complete stop
- `yield`: Give way to others

## Extending

### Real Alpamayo Integration

Replace the mock in `alpamayo_policy.py` with actual model calls:

```python
def decide(self, frame, prompt):
    # Process frame with vision model
    # Send to Alpamayo with prompt
    # Return structured JSON
    pass
```

### Additional Data Sources

Modify `data_loader.py` to load from:
- Waymo TFRecords directly
- Other autonomous driving datasets
- Live camera feeds

### Enhanced UI

Replace OpenCV with Streamlit for web-based interface:
- Timeline scrubbing
- Decision history
- Interactive playback

## Dependencies

- opencv-python: Video processing and visualization
- numpy: Array operations

## License

[Add appropriate license]

## Contributing

[Add contribution guidelines]
