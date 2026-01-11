"""
Data loader for Waymo Open Dataset video clips.

For this demo, assumes a video file (MP4) extracted from Waymo data.
In a full implementation, this would load from TFRecords.

Functions:
    - load_video_frames: Load and sample frames from video
"""

import cv2
import numpy as np

def load_video_frames(video_path, sample_fps=1):
    """
    Load video frames and sample at specified FPS.

    Args:
        video_path (str): Path to video file
        sample_fps (int): Frames per second to sample

    Returns:
        list: List of sampled frames (numpy arrays)
        float: Original video FPS
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame sampling interval
    sample_interval = max(1, int(original_fps / sample_fps))

    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % sample_interval == 0:
            frames.append(frame)

        frame_count += 1

    cap.release()
    return frames, original_fps
