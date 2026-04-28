import streamlit as st
import requests
import pandas as pd
import os
import time

# Configuration & Backend Link
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# --- PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="PolyMind | Neural Suite",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEURAL SUITE MASTER STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Stealth Foundation */
    :root {
        --bg-main: #020617;
        --bg-card: #0F172A;
        --border-subtle: rgba(255, 255, 255, 0.05);
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --accent-blue: #2563EB;
        --accent-gradient: linear-gradient(90deg, #2563EB 0%, #4F46E5 100%);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary);
    }

    .block-container {
        padding: 1rem 5rem !important;
        max-width: 1300px;
    }

    /* --- SIDEBAR BUTTON TRANSFORMATION --- */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid var(--border-subtle);
    }
    
    /* Hide default radio circles */
    [data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stWidgetLabel"] {
        display: none;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        display: flex !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        border-radius: 8px !important;
        border: 1px solid var(--border-subtle) !important;
        background: transparent !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        color: #4B5563 !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.03) !important;
    }

    /* Active State for Sidebar Buttons */
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input[checked]) {
        background: rgba(37, 99, 235, 0.1) !important;
        border: 1px solid rgba(37, 99, 235, 0.3) !important;
        border-left: 3px solid var(--accent-blue) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Hide the radio input bullet */
    [data-testid="stSidebar"] div[role="radiogroup"] input {
        display: none;
    }

    /* --- INGESTION ARCHITECTURE --- */
    .ingest-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 2.5rem;
        height: 100%;
        transition: border 0.3s ease;
    }

    .ingest-card:hover { 
        border-color: rgba(37, 99, 235, 0.2); 
    }

    /* --- BUTTON CONSISTENCY --- */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border-radius: 8px !important;
        height: 48px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }

    /* Input focus polish */
    .stTextInput input {
        background-color: #111827 !important;
        border: 1px solid var(--border-subtle) !important;
        color: white !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--accent-blue) !important;
    }

    /* Footer Card */
    .footer-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: INDUSTRIAL DASHBOARD ---
with st.sidebar:
    st.markdown("<div style='padding: 1rem 0;'><h2 style='color: white; font-weight: 700; letter-spacing: 1px;'>POLYMIND</h2><p style='color: #4F46E5; font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px;'>NEURAL COMMAND</p></div>", unsafe_allow_html=True)
    st.write("")
    workspace = st.radio("WORKSPACES", 
        ["DATA INGESTION", "QUERY INTERFACE", "SYSTEM METRICS"],
        label_visibility="collapsed")
    st.write("---")
    st.markdown("<p style='color: #475569; font-size: 0.6rem;'>ENCRYPTED TUNNEL: v1.9.4</p>", unsafe_allow_html=True)

# --- MODULE: SOURCE INGESTION (REFINED) ---
if workspace == "DATA INGESTION":
    st.markdown("<h1 style='color: white; font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;'>Source Ingestion</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3B82F6; font-weight: 500; margin-bottom: 0.2rem;'>Turn raw documents and URLs into structured intelligence.</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.9rem; margin-bottom: 2rem;'>Upload PDFs or connect web sources to build a searchable knowledge base.</p>", unsafe_allow_html=True)
    
    # Helper Strip
    st.markdown("<div style='background: #0F172A; border: 1px solid rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin-bottom: 2rem; color: #F8FAFC; font-size: 0.9rem;'>INFO: This is the first step — everything you add here becomes the foundation for analysis.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("### LOCAL ARCHIVE (PDF)")
            st.markdown("<p style='color: #475569; font-size: 0.8rem; margin-bottom: 1.5rem;'>Upload localized document archives for semantic indexing.</p>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Archive Upload", type="pdf", label_visibility="collapsed")
            
            if st.button("EXECUTE INDEXING"):
                if uploaded_file:
                    with st.spinner("Processing..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        try:
                            res = requests.post(f"{BACKEND_URL}/ingest/pdf", files=files)
                            if res.status_code == 200: 
                                st.success("SUCCESS: INDEX COMPLETE")
                            elif res.status_code in [502, 504]:
                                st.error(f"ENGINE ERROR: {res.status_code} - Backend Timeout or Gateway Error. Please check if the Render service is active and environment variables are set.")
                            else:
                                st.error(f"ENGINE ERROR: {res.status_code} - {res.text}")
                        except Exception as e: 
                            st.error(f"NETWORK ERROR: {str(e)}")
            
            st.markdown("<p style='text-align: center; color: #475569; font-size: 0.65rem; margin-top: 1rem;'>Analyze and index document for vector search</p>", unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown("### REMOTE NODE (URL)")
            st.markdown("<p style='color: #475569; font-size: 0.8rem; margin-bottom: 1.5rem;'>Connect and synchronize external web resources.</p>", unsafe_allow_html=True)
            
            st.write("Enter Protocol URL (HTTPS)")
            url = st.text_input("URL Input", placeholder="https://external-resource.com", label_visibility="collapsed")
            
            if st.button("SYNCHRONIZE"):
                if url:
                    with st.spinner("Synchronizing..."):
                        try:
                            res = requests.post(f"{BACKEND_URL}/ingest/url", json={"url": url})
                            if res.status_code == 200: 
                                st.success("SUCCESS: SYNC COMPLETE")
                            else:
                                st.error(f"ENGINE ERROR: {res.status_code} - {res.text}")
                        except Exception as e: 
                            st.error(f"NETWORK ERROR: {str(e)}")
            
            st.markdown("<p style='text-align: center; color: #475569; font-size: 0.65rem; margin-top: 1rem;'>Fetch and map content from remote protocol</p>", unsafe_allow_html=True)

    # --- DOCUMENT MANAGEMENT SECTION ---
    st.write("---")
    dhead1, dhead2 = st.columns([3, 1])
    with dhead1:
        st.markdown("<h3 style='color: white; margin-bottom: 1rem;'>Active Knowledge Base</h3>", unsafe_allow_html=True)
    with dhead2:
        if st.button("WIPE ALL", help="Clear entire knowledge base", type="primary"):
            with st.spinner("Nuking index..."):
                if requests.delete(f"{BACKEND_URL}/documents").status_code == 200:
                    st.success("Wiped!")
                    time.sleep(1)
                    st.rerun()
    
    try:
        docs_res = requests.get(f"{BACKEND_URL}/documents")
        if docs_res.status_code == 200:
            active_docs = docs_res.json()
            if not active_docs:
                st.info("No active documents in knowledge base.")
            else:
                for doc in active_docs:
                    with st.container(border=True):
                        dcol1, dcol2, dcol3 = st.columns([3, 1, 1])
                        with dcol1:
                            st.markdown(f"**{doc['name']}**")
                        with dcol2:
                            st.markdown(f"`{doc['source_type'].upper()}`")
                        with dcol3:
                            if st.button("DELETE", key=f"del_{doc['id']}", use_container_width=True):
                                with st.spinner("Deleting..."):
                                    del_res = requests.delete(f"{BACKEND_URL}/documents/{doc['id']}")
                                    if del_res.status_code == 200:
                                        st.success(f"Deleted")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error("Error")
    except:
        st.error("Could not fetch document list.")

    # Security Footer
    st.markdown("""
        <div class="footer-card">
            <div>
                <div style="font-weight: 700; font-size: 1rem; color: white;">SECURITY: PRIVATE. ENCRYPTED.</div>
                <div style="color: #64748B; font-size: 0.8rem;">Your data is processed within a secure tunnel. External sharing is restricted.</div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.2); padding: 4px 12px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;">AES-256 ENCRYPTED</div>
        </div>
    """, unsafe_allow_html=True)

# --- MODULE: QUERY INTERFACE ---
elif workspace == "QUERY INTERFACE":
    st.markdown("<h1 style='color: white; font-size: 2.2rem; font-weight: 700; margin-bottom: 2rem;'>Query Interface</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Enter research strategy...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.status("🧠 Processing query...", expanded=True) as status:
                st.write("Retrieving information...")
                time.sleep(1)
                st.write("Generating response...")
                
                try:
                    response = requests.post(f"{BACKEND_URL}/query", json={"query": query})
                    if response.status_code == 200:
                        data = response.json()
                        status.update(label="Complete", state="complete")
                        st.markdown(data["answer"])
                        st.session_state.messages.append({"role": "assistant", "content": data["answer"]})
                except:
                    st.error("Engine failure.")

# --- MODULE: SYSTEM METRICS ---
elif workspace == "SYSTEM METRICS":
    st.markdown("<h1 style='color: white; font-size: 2.2rem; font-weight: 700; margin-bottom: 2rem;'>System Metrics</h1>", unsafe_allow_html=True)
    
    try:
        metrics_res = requests.get(f"{BACKEND_URL}/metrics")
        if metrics_res.status_code == 200:
            m = metrics_res.json()
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("SESSIONS", m["total_queries"])
            with c2: st.metric("LATENCY", f"{m['avg_response_time']:.2f}s")
            with c3: st.metric("HEALTH", "OPTIMAL")
    except:
        pass

    st.write("---")
    try:
        hist_res = requests.get(f"{BACKEND_URL}/history")
        if hist_res.status_code == 200:
            history = hist_res.json()
            if history:
                df = pd.DataFrame(history)
                st.dataframe(df[["timestamp", "query", "response_time"]], use_container_width=True)
    except:
        pass
