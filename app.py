import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION & SÉCURITÉ ---
st.set_page_config(page_title="Mon AI Hub Privé", layout="wide")

# Vérification du mot de passe
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.session_state["authenticated"]:
        return True
    
    st.title("🔐 Accès Restreint")
    pwd = st.text_input("Entrez le mot de passe pour accéder au Hub :", type="password")
    if st.button("Se connecter"):
        if pwd == st.secrets["PASSWORD"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect")
    return False

if check_password():
    # --- 2. CONFIGURATION DE L'IA ---
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]) 

    # --- 3. DESIGN DU HUB (CSS) ---
    st.markdown("""
        <style>
        .stButton>button { width: 100%; border-radius: 10px; background-color: #2d3748; color: white; }
        .card {
            background-color: #1e2630;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #2d3748;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 Mon Hub d'Applications IA")
    
    # --- 4. NAVIGATION ---
    menu = ["Tableau de Bord", "Profile Scorer", "Générateur à Martine"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Tableau de Bord":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card"><h3>📊 Profile Scorer</h3><p>Analyse de CV et scoring.</p></div>', unsafe_allow_html=True)
            if st.button("Lancer Profile Scorer"):
                st.info("Outil en cours d'intégration...")
        
        with col2:
            st.markdown('<div class="card"><h3>🎨 Générateur à Martine</h3><p>Création d\'images persistantes.</p></div>', unsafe_allow_html=True)
            if st.button("Lancer le Générateur"):
                st.info("Outil en cours d'intégration...")

    elif choice == "Profile Scorer":
        st.subheader("📊 Profile Scorer")
        # Ici on ajoutera ton "System Instruction" plus tard
        user_input = st.text_area("Collez le CV ici :")
        if st.button("Analyser"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_input)
            st.write(response.text)
            
    st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({"authenticated": False}))