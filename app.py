import streamlit as st
import stripe

# 1. Configurare Stripe
stripe.api_key = "sk_test_PUNE_AICI_CHEIA_TA_DIN_STRIPE"

# Titlul aplicației
st.title("AI Detector Pro")

# 2. Preluăm parametrii din URL pentru a verifica plata
query_params = st.query_params

if query_params.get("payment") == "success":
    st.balloons()
    st.success("✅ Plată confirmată! Analiza completă a fost deblocată.")
    
    # --- LOC PENTRU REZULTATELE TALE COMPLETE ---
    st.header("Raport Tehnic Complet")
    st.write("- Analiza frecvențelor: Detectat tipar algoritmic în spectrul 14kHz.")
    st.write("- Semnătură vocală: 92% probabilitate de sinteză neuronală.")
    # --------------------------------------------
    
    if st.button("Înapoi la scaner"):
        st.query_params.clear()
        st.rerun()
else:
    # 3. Interfața principală înainte de plată
    st.write("### Probabilitate AI: 85%")
    st.info("Pentru a vedea raportul complet și dovezile tehnice, te rugăm să deblochezi analiza.")

    if st.button("Analiză deblocată! (1€)"):
        try:
            # Crearea sesiunii de checkout
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Analiză completă audio AI',
                        },
                        'unit_amount': 100,  # 1 Euro
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8501/?payment=success',
                cancel_url='http://localhost:8501/?payment=cancel',
            )
            
            # Redirecționare către Stripe
            st.markdown(f'<meta http-equiv="refresh" content="0; url={checkout_session.url}">', unsafe_allow_html=True)
            st.write(f"Dacă nu ești redirecționat, [click aici]({checkout_session.url}).")
            
        except Exception as e:
            st.error(f"Eroare la activarea plății: {e}")

if query_params.get("payment") == "cancel":
    st.warning("Plata a fost anulată. Te rugăm să încerci din nou.")
