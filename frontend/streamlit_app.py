from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api")

st.set_page_config(page_title="Multi-Agent AI Research Assistant", layout="wide")

st.title("Multi-Agent AI Research Assistant")
st.write(
    "Upload documents, chat with uploaded content, and generate research reports."
)

tab_upload, tab_chat, tab_reports = st.tabs(["Upload", "Chat", "Reports"])

with tab_upload:
    st.header("Document Upload")
    uploaded_files = st.file_uploader(
        "Select PDF, DOCX, TXT, or CSV files",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "csv"],
    )

    if st.button("Upload and extract text"):
        if not uploaded_files:
            st.warning("Please upload one or more supported documents.")
        else:
            files_payload = [
                ("files", (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type))
                for uploaded_file in uploaded_files
            ]
            try:
                response = requests.post(f"{BACKEND_URL}/documents/upload", files=files_payload, timeout=120)
                response.raise_for_status()
                data = response.json()
                for document in data.get("documents", []):
                    st.subheader(document["filename"])
                    st.caption(f"Saved to: {document['file_path']}")
                    text = document.get("extracted_text", "")
                    if text:
                        st.text_area("Extracted text", text, height=280)
                    else:
                        st.info("No text was extracted from this document.")
                st.success("Upload completed successfully.")
            except requests.RequestException as exc:
                st.error(f"Upload failed: {exc}")

with tab_chat:
    st.header("Chat with Documents")
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = "default"

    question = st.text_input("Ask a question about your uploaded documents")
    if st.button("Send question"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            payload = {
                "question": question,
                "conversation_id": st.session_state.conversation_id,
            }
            try:
                response = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=120)
                response.raise_for_status()
                data = response.json()
                st.markdown("### Answer")
                st.write(data.get("answer", "No response received."))
                citations = data.get("citations", [])
                if citations:
                    st.markdown("### Citations")
                    for citation in citations:
                        st.markdown(f"- {citation}")
                st.success("Chat response generated.")
            except requests.RequestException as exc:
                st.error(f"Chat failed: {exc}")

with tab_reports:
    st.header("Generate Research Report")
    report_title = st.text_input("Report title")
    report_question = st.text_input("Research question")
    if st.button("Generate report"):
        if not report_title.strip() or not report_question.strip():
            st.warning("Please provide both a report title and research question.")
        else:
            payload = {
                "title": report_title,
                "question": report_question,
                "conversation_id": st.session_state.conversation_id,
            }
            try:
                response = requests.post(f"{BACKEND_URL}/reports/generate", json=payload, timeout=180)
                response.raise_for_status()
                data = response.json()
                st.success("Report generated successfully.")
                st.markdown(f"**PDF:** {data.get('pdf_path', '')}")
                st.markdown(f"**DOCX:** {data.get('docx_path', '')}")
                st.text_area("Report content preview", data.get("content", ""), height=300)
            except requests.RequestException as exc:
                st.error(f"Report generation failed: {exc}")