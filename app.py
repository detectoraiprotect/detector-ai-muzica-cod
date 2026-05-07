import streamlit as st
import librosa
import numpy as np
import stripe
import datetime

# --- CONFIGURARE PLĂȚI ---
stripe.api_key = "sk_test_51Pxu86B6fCFFJHDsy82RBMe92L1MzdMuS7n6v68R8R8z3HFnOBUmjud4Vf5nsmE1eFSykuzWr5vPht8al6lYwBb7U00S0vR9C41"
STRIPE_PUBLISHABLE_KEY = "pk_test_51Pxu86B6fCFFJHDsyR06p4IFRUd8C7VQyuXntPBPBnt81Fo6FK8wJLrtUVXvOTnpqaS3i1yEUNXvhu8wkIImTyUP00BT0SaeMS"

st.set_page_config(page_title="AI Detector Pro", page_icon="🛡️")

if 'platit' not in st.session_state:
    st.session_state.platit = False

st.title("🛡️ AI Detector Pro")
st.write("Încarcă un fișier. Analiza completă costă 1€.")

audio_file = st.file_uploader("Încarcă audio", type=["mp3", "wav"])

if audio_file:
    if not st.session_state.platit:
        st.warning("Plătește 1€ pentru a debloca rezultatul.")
        if st.button("💳 Plătește acum"):
            st.session_state.platit = True
            st.rerun()
    else:
        st.success("Analiză deblocată!")
        y, sr = librosa.load(audio_file, duration=30)
        rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        st.metric("Probabilitate AI", f"{85 if rolloff < 6500 else 15}%")
