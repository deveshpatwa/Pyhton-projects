import ffmpeg 
import cv2
import subprocess
import moviepy
from moviepy import VideoFileClip
# importing video

# extract audio from a video file

# video = VideoFileClip("video_file.mkv")
# video.audio.write_audiofile("raw_audio_file.mp3")   # lower quality wav is good
# video.close()

# loading audio file in wav format
video = VideoFileClip("video_file.mkv")

video.audio.write_audiofile(
    "temp.wav",
    codec="pcm_s16le",
    fps=44100
)

video.close()


# This is to reduce the background noise 
import soundfile as sf
import noisereduce as nr

audio, sr = sf.read("temp.wav")

clean = nr.reduce_noise(
    y=audio,
    sr=sr,
    stationary=False
)

sf.write("noise_removed.wav", clean, sr)

import subprocess

subprocess.run([
    "deep-filter",
    "input.wav",
    "output.wav"
])

# new code

import subprocess
import os

# -----------------------------
# Input and Output Paths
# -----------------------------
input_audio = "input.wav"
clean_wav = "cleaned.wav"
output_mp3 = "audiobook.mp3"

# -----------------------------
# Run DeepFilterNet
# -----------------------------
print("Cleaning audio with DeepFilterNet...")

subprocess.run(
    [
        "deep-filter",
        input_audio,
        "-o",
        "."
    ],
    check=True
)

# DeepFilterNet saves the cleaned file automatically.
# Find the generated WAV file.
generated_file = None

for file in os.listdir("."):
    if file.endswith(".wav") and file != input_audio:
        generated_file = file
        break

if generated_file is None:
    raise FileNotFoundError("DeepFilterNet output not found.")

# Rename for convenience
os.replace(generated_file, clean_wav)

print("Noise reduction completed.")

# -----------------------------
# Convert WAV to MP3
# -----------------------------
print("Exporting MP3...")

subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-i",
        clean_wav,
        "-codec:a",
        "libmp3lame",
        "-b:a",
        "192k",
        output_mp3,
    ],
    check=True
)

print("Done!")
print("Output:", output_mp3)

import deep_filter 
from d.enhance import enhance, init_df

# Load the model
model, df_state, _ = init_df()

print("Model loaded")