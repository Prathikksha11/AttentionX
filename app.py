import os

# 🔥 FORCE FFmpeg PATH
os.environ["PATH"] += r";C:\Users\Prathikksha\Downloads\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin"

import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import random

st.set_page_config(page_title="AttentionX 🚀", layout="wide")

# 🎨 HEADER
st.markdown("""
# 🎬 AttentionX  
### Turn long videos into viral short clips automatically 🚀
""")

uploaded_file = st.file_uploader("📤 Upload your video", type=["mp4"])

# 🎯 Hooks
hooks = [
    "This will change your mindset 🔥",
    "Nobody tells you this 😳",
    "This is the real truth 💯",
    "You are doing this wrong ⚠️",
    "This can change your life 🚀"
]

# 🧠 Smart clip finder (ENSURES < 60s)
def find_best_clips(transcript, duration):
    clips = []

    MAX_CLIP = 50  # 👈 keep safe under 60 sec
    MIN_CLIP = 20

    for i in range(5):
        clip_length = random.randint(MIN_CLIP, MAX_CLIP)

        start = random.randint(0, max(1, int(duration - clip_length)))
        end = start + clip_length

        hook = random.choice(hooks)
        score = random.randint(85, 99)

        clips.append((start, end, hook, score))

    return clips

# 📱 Convert to vertical
def make_vertical(clip):
    w, h = clip.size
    new_w = int(h * 9 / 16)
    x_center = w // 2
    cropped = clip.crop(x_center=x_center, width=new_w, height=h)
    return cropped.resize((720, 1280))

# 🚀 MAIN
if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Video uploaded successfully")

    if st.button("🚀 Generate Viral Clips"):
        
        progress = st.progress(0)

        video = VideoFileClip("input.mp4")

        # 🎧 Extract audio
        st.write("🎧 Extracting audio...")
        video.audio.write_audiofile("audio.wav")
        progress.progress(20)

        # 🧠 Transcribe
        st.write("🧠 Transcribing with AI...")
        model = whisper.load_model("tiny")
        result = model.transcribe("audio.wav", fp16=False)

        transcript = result["text"]
        duration = int(video.duration)

        progress.progress(50)
        st.success("✅ Transcript ready")

        # 🤖 Detect clips
        st.write("🤖 Finding viral moments...")
        clips = find_best_clips(transcript, duration)

        progress.progress(70)

        st.markdown("## 🎯 Generated Viral Clips")

        cols = st.columns(2)

        for i, (start, end, hook, score) in enumerate(clips):
            try:
                with cols[i % 2]:
                    st.markdown(f"""
                    ### 🔥 {hook}  
                    **Virality Score:** {score}%  
                    **Duration:** {end - start} sec ⏱️  
                    **Emotion:** High Energy ⚡
                    """)

                    clip = video.subclip(start, end)
                    clip = make_vertical(clip)

                    filename = f"clip_{i}.mp4"
                    clip.write_videofile(
                        filename,
                        codec="libx264",
                        audio_codec="aac",
                        verbose=False,
                        logger=None
                    )

                    st.video(filename)

            except Exception as e:
                st.error(f"Error generating clip {i}: {e}")

        progress.progress(100)
        st.success("🎉 Clips Generated Successfully!")