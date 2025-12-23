# Data Folder

Place your Waymo Open Dataset video clips here.

## Getting Waymo Data

1. Visit the [Waymo Open Dataset website](https://waymo.com/open/)
2. Download scene data (TFRecords)
3. Extract front camera images/videos to MP4 format
4. Place the MP4 files in this folder

## Example Usage

Once you have a video file (e.g., `urban_scene.mp4`), run:

```bash
python ../main.py --video_path urban_scene.mp4 --fps 1
```
