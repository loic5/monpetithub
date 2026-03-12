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

    # --- 4. MOTEUR : LOOPIX (L'Architecte d'Image) ---
    elif st.session_state.page == "loopix":
        st.title("⚡ LooPix")
        st.write("Décrivez votre mise en scène et ajoutez votre photo de référence.")
        
        # AJOUT : Bouton pour télécharger la photo
        uploaded_file = st.file_uploader("Choisissez votre photo de référence...", type=['png', 'jpg', 'jpeg'])
        
        user_input_loopix = st.text_area("Votre souhait (ex: Moi en tenue de samouraï dans le futur) :", height=150)
        
        if st.button("Générer le Prompt Expert"):
            if user_input_loopix and uploaded_file:
                with st.spinner("LooPix analyse votre photo et crée le prompt..."):
                    # On charge l'image pour l'envoyer à Gemini
                    import PIL.Image
                    img = PIL.Image.open(uploaded_file)
                    
                    model = genai.GenerativeModel('gemini-1.5-flash', 
                        system_instruction="""Tu es LooPix. Ta mission est d'analyser la photo fournie (traits du visage, cheveux, style) et la demande de l'utilisateur pour créer un PROMPT TECHNIQUE en ANGLAIS pour Midjourney.
                        
                        Structure ta réponse ainsi :
                        1. **Prompt technique (Anglais)** : Un paragraphe détaillé commençant par 'A high-quality photo of [description de la personne basée sur l'image]...' en incluant le décor, les habits et l'éclairage. Ajoute les paramètres '--ar 16:9 --v 6.0'.
                        2. **Note de LooPix (Français)** : Explique tes choix artistiques.""")
                    
                    # On envoie le texte + l'image
                    response = model.generate_content([user_input_loopix, img])
                    
                    st.markdown("---")
                    st.markdown("### ✨ Résultat de la conception")
                    st.write(response.text)
            elif not uploaded_file:
                st.warning("Pense à ajouter une photo pour que je sache à quoi tu ressembles !")
            else:
                st.warning("Dis-moi ce que tu veux faire (le contexte, l'endroit...)")
