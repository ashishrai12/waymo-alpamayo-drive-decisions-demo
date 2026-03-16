"""
Visualization module for the autonomous driving demo.

Provides OpenCV-based UI with video playback and decision overlays.
Shows video on left, decisions and explanations on right.
"""

import cv2
import numpy as np
import json

def create_visualization_window(frames, decisions, original_fps=30):
    """
    Create an interactive visualization window.

    Args:
        frames: List of video frames
        decisions: List of decision dictionaries
        original_fps: Original video FPS for playback timing
    """
    if not frames or not decisions:
        print("No frames or decisions to display")
        return

    # Window setup
    window_name = "Alpamayo R1 Autonomous Driving Demo"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1200, 600)

    frame_idx = 0
    paused = False
    delay = int(1000 / original_fps)  # Delay between frames in ms

    while True:
        if not paused and frame_idx < len(frames):
            frame = frames[frame_idx].copy()
            decision = decisions[frame_idx]

            # Create display frame with video and info panel
            display_frame = create_display_frame(frame, decision)

            cv2.imshow(window_name, display_frame)

            frame_idx += 1
            if frame_idx >= len(frames):
                frame_idx = 0  # Loop back to start

        # Check if window was closed by user (clicking X)
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

        key = cv2.waitKey(delay if not paused else 0) & 0xFF

        if key == ord('q'):  # Quit
            break
        elif key == ord(' '):  # Pause/Play
            paused = not paused
        elif key == ord('n'):  # Next frame
            if paused and frame_idx < len(frames) - 1:
                frame_idx += 1
        elif key == ord('p'):  # Previous frame
            if paused and frame_idx > 0:
                frame_idx -= 1
        elif key == 27:  # ESC
            break

    cv2.destroyAllWindows()

def create_display_frame(frame, decision):
    """
    Create a display frame with video and decision information.

    Args:
        frame: Video frame (numpy array)
        decision: Decision dictionary

    Returns:
        numpy array: Combined display frame
    """
    # Resize frame to fit left side
    height, width = frame.shape[:2]
    max_video_height = 600
    scale = min(max_video_height / height, 1.0)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Create info panel on the right
    info_width = 400
    info_height = new_height
    info_panel = np.ones((info_height, info_width, 3), dtype=np.uint8) * 240  # Light gray

    # Add decision information to info panel
    y_offset = 30
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (0, 0, 0)  # Black
    thickness = 1

    # Title
    cv2.putText(info_panel, "Alpamayo R1 Decision", (10, y_offset),
                font, 0.8, color, 2)
    y_offset += 40

    # Frame ID
    cv2.putText(info_panel, f"Frame: {decision.get('frame_id', 'N/A')}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25

    # Scene Type
    cv2.putText(info_panel, f"Scene: {decision.get('scene_type', 'N/A')}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25

    # Traffic Light
    cv2.putText(info_panel, f"Traffic Light: {decision.get('traffic_light', 'N/A')}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25

    # Agents
    agents = decision.get('agents', [])
    cv2.putText(info_panel, f"Agents: {len(agents)}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25
    for agent in agents[:3]:  # Show up to 3 agents
        cv2.putText(info_panel, f"  {agent['type']} ({agent['position']})", (10, y_offset),
                    font, font_scale * 0.8, color, thickness)
        y_offset += 20

    # Hazards
    hazards = decision.get('hazards', [])
    cv2.putText(info_panel, f"Hazards: {', '.join(hazards) if hazards else 'None'}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25

    # Decision
    decision_text = decision.get('decision', 'N/A').upper()
    cv2.putText(info_panel, f"Decision: {decision_text}", (10, y_offset),
                font, font_scale, (0, 100, 0), thickness)  # Green
    y_offset += 25

    # Confidence
    confidence = decision.get('confidence', 0.0)
    cv2.putText(info_panel, f"Confidence: {confidence:.2f}", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25

    # Reason
    reason = decision.get('reason', 'N/A')
    # Wrap text if too long
    wrapped_reason = wrap_text(reason, 35)
    cv2.putText(info_panel, "Reason:", (10, y_offset),
                font, font_scale, color, thickness)
    y_offset += 25
    for line in wrapped_reason:
        cv2.putText(info_panel, line, (10, y_offset),
                    font, font_scale * 0.8, color, thickness)
        y_offset += 20

    # Combine video and info panel
    combined = np.hstack([resized_frame, info_panel])

    return combined

def wrap_text(text, max_chars):
    """
    Wrap text to fit within max_chars per line.

    Args:
        text (str): Text to wrap
        max_chars (int): Maximum characters per line

    Returns:
        list: List of wrapped lines
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines
