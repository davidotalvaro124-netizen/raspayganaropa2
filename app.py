import streamlit as st
import random
from streamlit_scratch_card import streamlit_scratch_card

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS DE MARCA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Raspa y Gana | Tu Marca de Ropa",
    page_icon="🎁",
    layout="centered"
)

# Estilo personalizado elegante (Estilo Moda Premium)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #111111, #1a1a1a);
        color: #ffffff;
    }
    .stButton>button {
        background-color: #D4AF37;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #f1c40f;
        color: #000000;
    }
    .prize-title {
        text-align: center;
        color: #D4AF37;
        font-size: 2.5rem;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE MARKETING (LOTE DE PREMIOS)
# ---------------------------------------------------------
def get_random_discount():
    # Probabilidades de conversión
    rand = random.random() * 100
    if rand < 50:
        return "10%", "FASHION10"   # 50% Probabilidad
    elif rand < 80:
        return "20%", "FASHION20"   # 30% Probabilidad
    elif rand < 95:
        return "40%", "FASHION40"   # 15% Probabilidad
    else:
        return "60%", "VIP60"       # 5% Probabilidad (Ganador Mayor)

# ---------------------------------------------------------
# INTERFAZ Y FLUJO DE USUARIO
# ---------------------------------------------------------
st.title("🎁 FASHION REWARDS")
st.subheader("¡Descubre tu descuento exclusivo!")
st.write("Ingresa tu correo para habilitar tu tarjeta de Raspa y Gana.")

# Manejo de estado para controlar la secuencia del juego
if "step" not in st.session_state:
    st.session_state.step = "email_step"
if "discount" not in st.session_state:
    st.session_state.discount = None
if "code" not in st.session_state:
    st.session_state.code = None

# PASO 1: Captura de Correo Electrónico
if st.session_state.step == "email_step":
    with st.form("lead_form"):
        email = st.text_input("Correo electrónico:", placeholder="ejemplo@correo.com")
        submit_btn = st.form_submit_button("¡QUIERO MI DESCUENTO!")
        
        if submit_btn:
            if email and "@" in email:
                # Determinar premio
                discount, code = get_random_discount()
                st.session_state.discount = discount
                st.session_state.code = code
                st.session_state.user_email = email
                st.session_state.step = "game_step"
                st.rerun()
            else:
                st.error("Por favor ingresa un correo electrónico válido.")

# PASO 2: El Juego de Raspa y Gana
elif st.session_state.step == "game_step":
    st.info("👇 **Instrucción:** Usa el ratón o tu dedo sobre el marco dorado para raspar y ver tu premio.")
    
    # Visual de la tarjeta de raspa y gana
    card_result = streamlit_scratch_card(
        overlay_color="#D4AF37",
        brush_radius=15,
        key="scratch_card_widget"
    )

    # Mostrar la recompensa que está detrás
    st.markdown(f"""
        <div style="text-align: center; margin-top: 15px; background-color: #222; padding: 20px; border-radius: 12px; border: 2px dashed #D4AF37;">
            <p style="margin: 0; color: #888;">TUS RESULTADOS:</p>
            <h1 class="prize-title">{st.session_state.discount} OFF</h1>
            <p style="font-size: 1.2rem; margin: 0;">Código: <strong>{st.session_state.code}</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"¡Felicidades! Hemos asignado este cupón a: **{st.session_state.user_email}**")
