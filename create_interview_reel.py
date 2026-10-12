"""
Generate Authentic UGC Interview Reel with Handheld Camera Motion
==================================================================
Merges:
1. 4K Master Photographic Portrait (ananya_final_master_portrait.jpg)
2. Studio Voiceover Audio (ananya_day01_audio.mp3)
3. Handheld smartphone camera micro-breathing motion (zoom & subtle pan)
Exports 9:16 (1080x1920) 60fps MP4 ready for Instagram / YouTube Shorts / TikTok
"""

import os
import subprocess

IMAGE_PATH = os.path.abspath("ananya_final_master_portrait.jpg")
AUDIO_PATH = os.path.abspath("ananya_day01_audio.mp3")
OUTPUT_MP4 = os.path.abspath("ananya_day01_interview_reel.mp4")

def build_reel():
    print(f"[*] Building viral interview reel from {IMAGE_PATH}...")
    
    # Zoompan filter: subtle organic 1.0 to 1.05 zoom with breathing motion at 60fps
    # 18.26 seconds duration (approx 1095 frames at 60fps)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", IMAGE_PATH,
        "-i", AUDIO_PATH,
        "-filter_complex",
        "[0:v]scale=1200:2133,zoompan=z='min(zoom+0.00012,1.06)':d=1100:x='iw/2-(iw/zoom/2)+sin(in/25)*3':y='ih/2-(ih/zoom/2)+cos(in/30)*2':s=1080x1920:fps=60,format=yuv420p[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        OUTPUT_MP4
    ]
    
    print("[*] Executing FFmpeg rendering pipeline...")
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Final 9:16 Interview Reel exported to {OUTPUT_MP4}")

if __name__ == "__main__":
    build_reel()
