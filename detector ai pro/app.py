import os
import stripe
import librosa
import numpy as np
import tensorflow as tf
from flask import Flask, render_template_string, request, redirect

# --- CHEILE TALE STRIPE ---
stripe.api_key = "sk_test_51P6WshRu8vW8f7fTM85H1pBeH7O20Z248p1mE7m4w7Y8u2u6Z5y3O1p9X8e7r6t5"

app = Flask(__name__)

# --- FUNCTII AI ---
def genereaza_spectrograma(cale_fisier):
    try:
        y, sr = librosa.load(cale_fisier, duration=10)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)
        if S_dB.shape[1] > 430: S_dB = S_dB[:, :430]
        else: S_dB = np.pad(S_dB, ((0,0), (0, 430 - S_dB.shape[1])))
        return S_dB.reshape(1, 128, 430, 1)
    except: return None

def creeaza_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 430, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

# Incarcam sau cream un model gol de test
if os.path.exists("detector_finalizat.h5"):
    model = tf.keras.models.load_model("detector_finalizat.h5")
else:
    model = creeaza_model()

# --- PAGINA WEB ---
@app.route('/')
def index():
    return '''
    <h1>Detector Muzica AI - 1€</h1>
    <form action="/pay" method="POST"><button type="submit">Plateste 1€ si Verifica</button></form>
    '''

@app.route('/pay', methods=['POST'])
def pay():
    session = stripe.checkout.Session.create(
        line_items=[{'price_data': {'currency': 'eur', 'product_data': {'name': 'Verificare AI'}, 'unit_amount': 100}, 'quantity': 1}],
        mode='payment',
        success_url=request.host_url + 'upload?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.host_url
    )
    return redirect(session.url, code=303)

@app.route('/upload')
def upload():
    return '<h1>Plata reusita!</h1><form action="/result" method="POST" enctype="multipart/form-data"><input type="file" name="file"><button type="submit">Analizeaza</button></form>'

@app.route('/result', methods=['POST'])
def result():
    f = request.files['file']
    f.save("temp.mp3")
    data = genereaza_spectrograma("temp.mp3")
    res = model.predict(data)[0][0]
    verdict = "AI" if res > 0.5 else "UMAN"
    return f"<h1>Rezultat: {verdict}</h1><p>Scor: {res}</p><a href='/'>Inapoi</a>"

if __name__ == "__main__":
    app.run(port=5000)
