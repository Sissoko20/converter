import streamlit as st
from moviepy import *
import tempfile
import os

st.title("🎥➡️🎵 Convertisseur Vidéo en MP3")

uploaded_file = st.file_uploader("Importez une vidéo (mp4, mov, avi, mkv)", type=["mp4","mov","avi","mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_file.read())
        tmp_video_path = tmp_video.name

    st.info("Conversion en cours...")

    try:
        clip = VideoFileClip(tmp_video_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio_path = tmp_audio.name

        clip.audio.write_audiofile(tmp_audio_path, logger=None)
        clip.close()

        with open(tmp_audio_path, "rb") as f:
            st.download_button(
                label="⬇️ Télécharger le MP3",
                data=f,
                file_name="audio_converti.mp3",
                mime="audio/mpeg"
            )
    except Exception as e:
        st.error(f"Erreur lors de la conversion : {e}")
    finally:
        if os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)
        if 'tmp_audio_path' in locals() and os.path.exists(tmp_audio_path):
            os.remove(tmp_audio_path)
