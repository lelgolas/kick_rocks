import cv2
import os
import argparse

def extract_frames(video_path, output_dir, extraction_rate):
    # Create output directory if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file.
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # Get the video's frames per second (fps)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps == 0:
        print("Error retrieving video FPS")
        return

    # Calculate the interval (in frames) between extractions.
    # For example, if the video is 30 fps and extraction_rate is 5,
    # we extract one frame every 6 frames.
    frame_interval = int(round(video_fps / extraction_rate))
    if frame_interval == 0:
        frame_interval = 1

    frame_count = 0  # Count all frames read.
    saved_count = 0  # Count of frames saved.
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save frame if it meets the interval criteria.
        if frame_count % frame_interval == 0:
            output_path = os.path.join(output_dir, f"frame_{saved_count:06d}.png")
            cv2.imwrite(output_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted and saved {saved_count} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract frames from a video at a specified frame rate and save them as images."
    )
    parser.add_argument("video_path", help="Path to the input MP4 video file.")
    parser.add_argument("output_dir", help="Directory where the extracted images will be saved.")
    parser.add_argument(
        "--rate",
        type=float,
        default=1.0,
        help="Number of frames to extract per second (default: 1 frame per second)."
    )
    
    args = parser.parse_args()
    extract_frames(args.video_path, args.output_dir, args.rate)
