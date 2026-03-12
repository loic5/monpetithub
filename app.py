import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. CONFIGURATION & SÉCURITÉ ---
st.set_page_config(page_title="Mon AI Hub Privé", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "hub"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.authenticated:
        return True
    st.title("🔐 Accès Restreint")
    pwd = st.text_input("Mot de passe :", type="password")
    if st.button("Se connecter"):
        if pwd == st.secrets["PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")
    return False

if check_password():
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Barre latérale
    if st.session_state.page != "hub":
        if st.sidebar.button("⬅️ Retour au Hub"):
            st.session_state.page = "hub"
            st.rerun()
    
    st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({"authenticated": False, "page": "hub"}))

    # --- 2. LE HUB (INTERFACE GRAPHIQUE) ---
    if st.session_state.page == "hub":
        st.title("🚀 Mon Hub d'Applications IA")
        
        st.markdown("""
            <style>
            .stButton>button { width: 100%; border-radius: 10px; background-color: #2d3748; color: white; height: 3em; }
            .card { background-color: #1e2630; padding: 20px; border-radius: 15px; border: 1px solid #2d3748; min-height: 150px; }
            </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card"><h3>📊 Profile Scorer</h3><p>Analyse de CV et scoring.</p></div>', unsafe_allow_html=True)
            if st.button("Lancer Profile Scorer", key="launch_scorer"):
                st.session_state.page = "scorer"
                st.rerun()
        
        with col2:
            st.markdown('<div class="card"><h3>⚡ LooPix</h3><p>Générateur de contenu intelligent.</p></div>', unsafe_allow_html=True)
            if st.button("Lancer LooPix", key="launch_loopix"):
                st.session_state.page = "loopix"
                st.rerun()

    # --- 3. MOTEUR : PROFILE SCORER ---
    elif st.session_state.page == "scorer":
        st.title("📊 Profile Scorer")
        user_input = st.text_area("Collez le texte ici :", height=300)
        
        if st.button("Lancer l'Analyse"):
            if user_input:
                with st.spinner("Analyse en cours..."):
                    # On utilise une config simple sans system_instruction ici pour tester la stabilité
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Agis en tant que recruteur expert. Analyse ce texte et donne un score : {user_input}")
                    st.markdown("### 📋 Résultat")
                    st.write(response.text)

    # --- 4. MOTEUR : LOOPIX ---
    elif st.session_state.page == "loopix":
        st.title("⚡ LooPix")
        st.write("Décrivez votre mise en scène et ajoutez votre photo.")
        
        uploaded_file = st.file_uploader("Choisir une photo...", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="✅ Photo prête", width=150)
        
        user_input_loopix = st.text_area("Votre souhait (ex: Moi en astronaute) :", height=150)
        
        if st.button("Générer le Prompt"):
            if user_input_loopix and uploaded_file:
                with st.spinner("LooPix analyse votre visage et crée le prompt..."):
                    try:
                        img = PIL.Image.open(uploaded_file)
                        
                        # INITIALISATION SIMPLE
                        model = genai.GenerativeModel('gemini-1.5-flash-latest')
                        
                        # CONSTRUCTION DU MESSAGE (Texte + Image)
                        # On met les instructions directement dans le message envoyé
                        prompt_complet = [
                            f"CONTEXTE: Tu es LooPix, expert en Midjourney. Analyse la personne sur cette photo et crée un prompt en anglais pour la mettre dans cette situation : {user_input_loopix}. RÉPONSE ATTENDUE: Le prompt technique détaillé en anglais, puis une explication courte en français.",
                            img
                        ]
                        
                        response = model.generate_content(prompt_complet)
                        
                        st.markdown("---")
                        st.markdown("### ✨ Résultat LooPix")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Erreur technique : {e}")
            else:
                st.warning("Il manque la photo ou le texte !")
