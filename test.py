"""
Test script for the Alpamayo demo without requiring video files.

Generates dummy frames and tests the full pipeline.
"""

import numpy as np
from alpamayo_policy import AlpamayoPolicy
from decision_schema import validate_decision
from visualize import create_visualization_window

def generate_dummy_frames(num_frames=10, width=640, height=480):
    """Generate dummy video frames for testing."""
    frames = []
    for i in range(num_frames):
        # Create a simple frame with some variation
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Add some color based on frame number
        color = (i * 25 % 255, 100, 150)
        cv2.rectangle(frame, (50, 50), (width-50, height-50), color, -1)
        # Add frame number text
        cv2.putText(frame, f"Frame {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        frames.append(frame)
    return frames

def test_pipeline():
    """Test the full decision making pipeline."""
    print("Testing Alpamayo R1 Demo Pipeline...")

    # Generate dummy frames
    frames = generate_dummy_frames(5)
    print(f"Generated {len(frames)} dummy frames")

    # Initialize policy
    policy = AlpamayoPolicy(mock=True)

    goal_prompt = "Analyze the scene and decide the next driving action."

    decisions = []
    for i, frame in enumerate(frames):
        print(f"Processing frame {i}...")
        decision_json = policy.decide(frame, goal_prompt)
        print(f"Raw decision: {decision_json}")

        # Validate decision
        try:
            decision = validate_decision(decision_json)
            decision['frame_id'] = i  # Add frame_id after validation
            decisions.append(decision)
            print(f"Validated decision: {decision['decision']} (confidence: {decision['confidence']})")
        except ValueError as e:
            print(f"Validation error: {e}")
            continue

    print(f"Generated {len(decisions)} decisions")

    # Test visualization (commented out to avoid GUI in headless environment)
    # create_visualization_window(frames, decisions, original_fps=1)

    print("Pipeline test completed successfully!")

if __name__ == "__main__":
    import cv2  # Import here to avoid issues if not installed
    test_pipeline()
