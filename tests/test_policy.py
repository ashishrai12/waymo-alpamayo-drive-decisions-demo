"""
Test script for the Alpamayo demo without requiring video files.

Generates dummy frames and tests the full pipeline.
"""

import numpy as np
import cv2
from alpamayo_demo.core.policy import AlpamayoPolicy
from alpamayo_demo.core.schema import validate_decision
from alpamayo_demo.utils.visualization import create_visualization_window

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

def test_policy_decision_format():
    """Test that the policy returns correctly structured JSON."""
    policy = AlpamayoPolicy(mock=True)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    goal_prompt = "Test prompt"
    
    decision_json = policy.decide(frame, goal_prompt)
    decision = validate_decision(decision_json)
    
    assert "decision" in decision
    assert "confidence" in decision
    assert "reason" in decision
    assert 0.0 <= decision["confidence"] <= 1.0

def test_full_pipeline_mock():
    """Test the full decision making pipeline with mock data."""
    frames = generate_dummy_frames(3)
    policy = AlpamayoPolicy(mock=True)
    goal_prompt = "Analyze the scene."

    for i, frame in enumerate(frames):
        decision_json = policy.decide(frame, goal_prompt)
        decision = validate_decision(decision_json)
        assert decision is not None
        assert "scene_type" in decision
