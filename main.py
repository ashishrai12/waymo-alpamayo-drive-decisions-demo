"""
Main entry point for the Alpamayo R1 Autonomous Driving Demo.

This demo showcases video-language-action reasoning using Waymo Open Dataset camera data.
It demonstrates perception → reasoning → action → explanation pipeline.

Usage:
    python main.py --video_path path/to/waymo_video.mp4 --fps 1

Dependencies:
    - opencv-python
    - numpy
    - json
"""

import argparse
import cv2
import json
from data_loader import load_video_frames
from alpamayo_policy import AlpamayoPolicy
from visualize import create_visualization_window

def main():
    parser = argparse.ArgumentParser(description="Alpamayo R1 Autonomous Driving Demo")
    parser.add_argument("--video_path", type=str, default="data/sample_video.mp4", help="Path to Waymo video file (default: data/sample_video.mp4)")
    parser.add_argument("--fps", type=int, default=1, help="Frames per second to sample")
    parser.add_argument("--mock", action="store_true", help="Use mock Alpamayo policy")
    args = parser.parse_args()

    # Load video frames
    frames, fps = load_video_frames(args.video_path, sample_fps=args.fps)

    # Initialize Alpamayo policy (mock or real)
    policy = AlpamayoPolicy(mock=args.mock)

    # Goal prompt for the agent
    goal_prompt = """
    You are an autonomous vehicle driving in an urban environment.
    Analyze the current scene from the front camera and decide the next action.
    Consider safety, traffic rules, and smooth driving.
    Output your decision in the specified JSON format.
    """

    decisions = []
    for i, frame in enumerate(frames):
        # Get decision from Alpamayo
        decision_json = policy.decide(frame, goal_prompt)
        decision = json.loads(decision_json)
        decision['frame_id'] = i  # Ensure correct frame_id
        decisions.append(decision)

    # Visualize
    # Use the sampling FPS for visualization so it plays back at real-time speed relative to the sampling
    create_visualization_window(frames, decisions, original_fps=args.fps)

if __name__ == "__main__":
    main()
