# app/streamlit_app.py
import streamlit as st
import requests

st.set_page_config(page_title="Smart News Curator", layout="wide")

st.title("AI-Powered News Curator")
query = st.text_input("Enter your news topic:", placeholder="e.g. Bitcoin price prediction")
max_iter = st.slider("Max refinement iterations", 1, 5, value=3)

if st.button("🔍 Summarize"):
    with st.spinner("Contacting backend agents..."):
        res = requests.post("http://localhost:8000/news", json={
            "query": query,
            "max_iterations": max_iter
        })

        if res.status_code == 200:
            output = res.json()
            st.subheader("🧠 Final Summary")
            st.markdown(f"```markdown\n{output['final_summary']}```")

            st.subheader("📝 Evaluation")
            st.markdown(output["evaluation"])

            st.subheader("Urls")
            for i,url in enumerate(output["url"]):
                st.markdown(f"{i+1}-{url}")

            st.subheader("📝 Iterations")
            st.markdown(output["iteration"])
        else:
            st.error("Failed to get summary. Check FastAPI server.")
