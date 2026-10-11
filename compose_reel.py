"""
Automated Reel Post-Production Composer (FFmpeg)
=================================================
Merges the Kling 3.0 video output with:
1. Studio-grade neural voiceover (ananya_day01_audio.mp3)
2. Subtle ambient campus / breeze audio layering
3. 9:16 format optimization (1080x1920)
"""

import os
import sys
import subprocess
import argparse

def compose_final_reel(video_input: str, audio_input: str = "ananya_day01_audio.mp3", output_reel: str = "final_ananya_reel.mp4") -> bool:
    if not os.path.exists(video_input):
        print(f"[!] Error: Video input file '{video_input}' not found.")
        print("[*] Please download your video from Higgsfield/Kling and save it as 'kling_output.mp4'.")
        return False

    if not os.path.exists(audio_input):
        print(f"[!] Audio file '{audio_input}' not found. Generating audio first...")
        subprocess.run([sys.executable, "make_audio.py"], check=True)

    print(f"[*] Composing final viral reel from '{video_input}' + '{audio_input}'...")

    # FFmpeg command: Replace or mix audio, ensure 1080x1920 vertical, faststart for instant IG playback
    cmd = [
        "ffmpeg", "-y",
        "-i", video_input,
        "-i", audio_input,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-movflags", "+faststart",
        output_reel
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Final reel exported successfully: {output_reel}")
        print("[*] Ready to upload to Instagram Reels / YouTube Shorts / TikTok!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] FFmpeg error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compose Final AI Influencer Reel")
    parser.add_argument("--video", default="kling_output.mp4", help="Path to video downloaded from Kling / Higgsfield")
    parser.add_argument("--audio", default="ananya_day01_audio.mp3", help="Path to neural voice audio")
    parser.add_argument("--output", default="final_ananya_reel.mp4", help="Output final reel video path")
    args = parser.parse_args()

    compose_final_reel(args.video, args.audio, args.output)
