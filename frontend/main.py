import streamlit as st
import requests
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="PolyMind - AI Research Assistant", layout="wide")

st.sidebar.title("🧠 PolyMind")
page = st.sidebar.radio("Navigation", ["Ingest", "Chat", "Metrics"])

if page == "Ingest":
    st.header("📂 Data Ingestion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if st.button("Process PDF"):
                with st.spinner("Chunking and Indexing..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/ingest/pdf", files=files)
                    if response.status_code == 200:
                        st.success("PDF processed successfully!")
                    else:
                        st.error(f"Error: {response.text}")

    with col2:
        st.subheader("Paste URL")
        url = st.text_input("Enter URL (e.g., blog post, research paper)")
        if st.button("Process URL"):
            if url:
                with st.spinner("Scraping and Indexing..."):
                    response = requests.post(f"{BACKEND_URL}/ingest/url", json={"url": url})
                    if response.status_code == 200:
                        st.success("URL processed successfully!")
                    else:
                        st.error(f"Error: {response.text}")

elif page == "Chat":
    st.header("💬 Research Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask a question about your documents...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Agents are collaborating..."):
                response = requests.post(f"{BACKEND_URL}/query", json={"query": query})
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    duration = response.json()["response_time"]
                    st.markdown(answer)
                    st.caption(f"Response time: {duration:.2f}s")
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Failed to get response from agents.")

elif page == "Metrics":
    st.header("📊 Performance Metrics")
    
    metrics_res = requests.get(f"{BACKEND_URL}/metrics")
    if metrics_res.status_code == 200:
        m = metrics_res.json()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Queries", m["total_queries"])
        c2.metric("Avg Response Time", f"{m['avg_response_time']:.2f}s")
        c3.metric("Document Status", "Active")

    st.subheader("Recent Query History")
    history_res = requests.get(f"{BACKEND_URL}/history")
    if history_res.status_code == 200:
        history = history_res.json()
        if history:
            df = pd.DataFrame(history)
            st.table(df[["timestamp", "query", "response_time"]])
        else:
            st.info("No queries yet.")
