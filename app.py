import streamlit as st
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from io import BytesIO

# Configurare pagină
st.set_page_config(page_title="AI Detector Pro", page_icon="🛡️")

# Inițializare Istoric
if 'istoric' not in st.session_state:
    st.session_state['istoric'] = []

tab1, tab2 = st.tabs(["🎵 Analiză Muzică", "💻 Analiză Cod"])

# --- TAB 1: MUZICĂ ---
with tab1:
    st.header("Detector Muzică AI")
    audio_file = st.file_uploader("Încarcă audio (MP3/WAV)", type=["mp3", "wav"])
    if audio_file:
        y, sr = librosa.load(audio_file, duration=30)
        rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        score = 85 if rolloff < 6500 else 15
   