import streamlit as st
import random
import streamlit.components.v1 as components

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Raspa y Gana | Tu Marca de Ropa",
    page_icon="🎁",
    layout="centered"
)

# Estilo visual moderno para Streamlit
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    .stButton>button {
        background-color: #D4AF37;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        border: none;
        width: 100%;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #f1c40f;
        color: #000000;
    }
    .stTextInput input {
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE MARKETING (DESCUENTOS)
# ---------------------------------------------------------
def get_random_discount():
    rand = random.random() * 100
    if rand < 50:
        return "10%", "FASHION10"   # 50% probabilidad
    elif rand < 80:
        return "20%", "FASHION20"   # 30% probabilidad
    elif rand < 95:
        return "40%", "FASHION40"   # 15% probabilidad
    else:
        return "60%", "VIP60"       # 5% probabilidad (Gran Ganador)

# ---------------------------------------------------------
# ESTADOS DEL JUEGO
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = "email_step"

# ---------------------------------------------------------
# INTERFAZ DE USUARIO
# ---------------------------------------------------------
st.title("🎁 FASHION REWARDS")

# PASO 1: CAPTURA DE CORREO
if st.session_state.step == "email_step":
    st.write("¡Ingresa tu correo electrónico para desbloquear tu tarjeta de Raspa y Gana!")
    
    with st.form("lead_form"):
        email = st.text_input("Tu Correo Electrónico:", placeholder="ejemplo@correo.com")
        submit_btn = st.form_submit_button("¡QUIERO MI DESCUENTO!")
        
        if submit_btn:
            if email and "@" in email:
                discount, code = get_random_discount()
                st.session_state.discount = discount
                st.session_state.code = code
                st.session_state.user_email = email
                st.session_state.step = "game_step"
                st.rerun()
            else:
                st.error("Por favor, ingresa un correo válido.")

# PASO 2: TARJETA INTERACTIVA DE RASPA Y GANA
elif st.session_state.step == "game_step":
    st.write(f"¡Hola **{st.session_state.user_email}**! Usa tu dedo o ratón sobre la tarjeta dorada para descubrir tu descuento.")

    # Componente HTML Canvas Interactivo incrustado
    scratch_card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background: transparent;
                font-family: 'Arial', sans-serif;
            }}
            .scratch-container {{
                position: relative;
                width: 320px;
                height: 180px;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            }}
            .prize-box {{
                position: absolute;
                width: 100%;
                height: 100%;
                background: #111;
                color: #fff;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                border: 3px dashed #D4AF37;
                box-sizing: border-box;
                border-radius: 15px;
            }}
            .prize-box h1 {{
                font-size: 3rem;
                color: #D4AF37;
                margin: 0;
            }}
            .prize-box p {{
                margin: 5px 0 0 0;
                font-size: 0.9rem;
                color: #ccc;
            }}
            .coupon {{
                background: #222;
                padding: 4px 12px;
                border-radius: 6px;
                font-weight: bold;
                color: #fff;
                margin-top: 8px;
            }}
            canvas {{
                position: absolute;
                top: 0;
                left: 0;
                cursor: pointer;
                touch-action: none;
            }}
        </style>
    </head>
    <body>
        <div class="scratch-container">
            <div class="prize-box">
                <p>¡GANASTE UN!</p>
                <h1>{st.session_state.discount} OFF</h1>
                <div class="coupon">CÓDIGO: {st.session_state.code}</div>
            </div>
            <canvas id="scratch" width="320" height="180"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('scratch');
            const ctx = canvas.getContext('2d');
            let isScratching = false;

            // Capa dorada
            const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#D4AF37');
            gradient.addColorStop(0.5, '#FFF8DC');
            gradient.addColorStop(1, '#AA7C11');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Texto sobre la capa
            ctx.fillStyle = "#222";
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "center";
            ctx.fillText("✨ RASPA AQUÍ ✨", canvas.width / 2, canvas.height / 2 + 5);

            function scratch(e) {{
                if (!isScratching) return;
                const rect = canvas.getBoundingClientRect();
                const x = (e.clientX || e.touches[0].clientX) - rect.left;
                const y = (e.clientY || e.touches[0].clientY) - rect.top;

                ctx.globalCompositeOperation = 'destination-out';
                ctx.beginPath();
                ctx.arc(x, y, 20, 0, Math.PI * 2);
                ctx.fill();
            }}

            canvas.addEventListener('mousedown', () => isScratching = true);
            canvas.addEventListener('mouseup', () => isScratching = false);
            canvas.addEventListener('mousemove', scratch);

            canvas.addEventListener('touchstart', () => isScratching = true);
            canvas.addEventListener('touchend', () => isScratching = false);
            canvas.addEventListener('touchmove', scratch);
        </script>
    </body>
    </html>
    """

    # Desplegar el juego HTML
    components.html(scratch_card_html, height=220)

    st.success(f"🎉 Usa el código **{st.session_state.code}** al finalizar tu compra para aplicar tu {st.session_state.discount} de descuento.")
    
    if st.button("Intentar con otro correo"):
        st.session_state.step = "email_step"
        st.rerun()
    
