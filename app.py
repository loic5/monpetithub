import streamlit as st
import google.generativeai as genai

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
            # ICI LE CHANGEMENT NOM : LooPix
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
                    model = genai.GenerativeModel('gemini-1.5-flash', 
                        system_instruction="METS TON PROMPT PROFILE SCORER ICI")
                    response = model.generate_content(user_input)
                    st.markdown("### 📋 Résultat")
                    st.write(response.text)

    # --- 4. MOTEUR : LOOPIX (Anciennement Martine) ---
    elif st.session_state.page == "loopix":
        st.title("⚡ LooPix")
        st.write("Bienvenue dans l'interface LooPix.")
        
        user_input_loopix = st.text_area("Entrez votre demande pour LooPix :", height=200)
        
        if st.button("Générer avec LooPix"):
            if user_input_loopix:
                with st.spinner("LooPix réfléchit..."):
                    model = genai.GenerativeModel('gemini-1.5-flash', 
                        system_instruction="METS TON PROMPT LOOPIX ICI")
                    response = model.generate_content(user_input_loopix)
                    st.write(response.text)
