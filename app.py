import streamlit as st
import google.generativeai as genai
from PIL import Image

# API Key സുരക്ഷിതമായി നൽകാൻ 
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = "YOUR_API_KEY_HERE"

genai.configure(api_key=api_key)

system_instruction = """
You are an expert Level-3 IT Support Engineer representing 'Rhythm Computer Solutions'. 
Your expertise includes Laptops, Desktops, Printers (Installation, spooler issues, paper jams), Networking (Routers, Switches, LAN/WAN setup, IP conflicts), and general IT hardware troubleshooting.
Provide step-by-step, practical, and highly accurate problem-solving help. 
CRITICAL RULE: If the user asks the question in Malayalam, you MUST reply in fluent Malayalam. If the user asks in English, reply in English.
"""
model = genai.GenerativeModel('gemini-3.8-flash', system_instruction=system_instruction)

# 1. Page Configuration
st.set_page_config(page_title="Rhythm IT Helpdesk", page_icon="logo.jpg", layout="centered")

# 2. Modern Colorful CSS & Hiding Deploy Buttons 
st.markdown("""
<style>
    /* 기존 CSS (ബട്ടൺ, ടെക്സ്റ്റ് ബോക്സ്) */
    .stButton>button {
        background-color: #0033cc;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #002299;
        color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1.5px solid #0033cc;
    }
    
    /* Fork, GitHub തുടങ്ങിയവ ഒളിപ്പിക്കാനുള്ള പുതിയ കോഡ് */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# 3. Chat History Initializing
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---------------------------------------------------------
# 4. SIDEBAR (എപ്പോഴും സ്ക്രീനിൽ കാണാനുള്ള ഭാഗം)
# ---------------------------------------------------------
with st.sidebar:
    # ലോഗോയും പേരും
    st.image("logo.jpg", width=120)
    st.markdown("### Rhythm IT Helpdesk")
    
    # New Chat Button 
    if st.button("🔄 New Chat / പുതിയ ചോദ്യം", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
        
    st.markdown("---")
    
    # സ്ക്രീൻഷോട്ട് അപ്‌ലോഡർ 
    uploaded_file = st.file_uploader("Upload Screenshot (Optional) / സ്ക്രീൻഷോട്ട് നൽകാൻ", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    
    # പുതിയതായി ചേർത്ത കോൺടാക്ട് വിവരങ്ങൾ (Contact Info)
    st.markdown("### 📞 Contact for Services")
    st.markdown("""
    **Rhythm Computer Solutions**  
    📱 +91 9895123809  
    📱 +91 7559923809  
    📧 rythmcomputerpkd@gmail.com
    """)
    
    st.markdown("---")
    
    # മുന്നറിയിപ്പുകൾ
    st.info("⏱️ **Usage Limit:** Maximum 15 queries per minute.")
    st.warning("⚠️ **Disclaimer:** Strictly for IT-related support. Searching for illegal content is prohibited.")
    
    # ഡെവലപ്പർ ക്രെഡിറ്റ്
    st.markdown("<p style='text-align: center; color: gray; font-size: 13px;'>Designed & Developed by <b>Hashim M A</b></p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. MAIN SCREEN (പ്രധാന ചാറ്റ് സ്ക്രീൻ)
# ---------------------------------------------------------
st.title("Rhythm IT Helpdesk 💻")
st.write("Ask any questions related to Laptops, Desktops, Printers, Networking, or other IT equipment in English or Malayalam. / ലാപ്ടോപ്പ്, ഡെസ്ക്ടോപ്പ്, പ്രിൻ്റർ, നെറ്റ്‌വർക്കിംഗ് സംശയങ്ങൾ മലയാളത്തിലോ ഇംഗ്ലീഷിലോ ചോദിക്കാം.")
st.markdown("---")

# പഴയ ചാറ്റുകൾ കാണിക്കാൻ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# പുതിയ ചോദ്യം ചോദിക്കാനുള്ള ചാറ്റ് ബോക്സ്
if prompt := st.chat_input("Type your problem here / നിങ്ങളുടെ പ്രശ്നം ഇവിടെ ടൈപ്പ് ചെയ്യുക..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Finding the best solution... / ഉത്തരം കണ്ടെത്തുന്നു..."):
            try:
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    response = st.session_state.chat_session.send_message([prompt, image])
                else:
                    response = st.session_state.chat_session.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"API Error: ദയവായി നിങ്ങളുടെ യഥാർത്ഥ API Key നൽകിയിട്ടുണ്ടോ എന്ന് പരിശോധിക്കുക. ({e})")
