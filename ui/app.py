import sys
sys.path.insert(0, '.')
import streamlit as st
from src.utils.router import Router
from src.models.ollama_client import OllamaClient

st.set_page_config(page_title="Multi-LLM Router", page_icon="🤖", layout="wide")
st.title("Multi-LLM Intelligent Routing System")
st.divider()

router = Router()
client = OllamaClient()

query = st.text_area("Enter your query:", height=100)

if st.button("Route and Generate", type="primary"):
    if query.strip() == "":
        st.warning("Please enter a query!")
    else:
        result = router.route(query)
        features = result["features"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Query Analysis")
            st.metric("Query Type", features.query_type.upper())
            st.metric("Complexity", features.complexity.upper())
            st.metric("Domain", features.domain.upper())
            st.metric("Word Count", features.word_count)

        with col2:
            st.subheader("Routing Decision")
            st.metric("Selected Model", result["selected_model"].upper())
            for model, score in sorted(result["scores"].items(), key=lambda x: x[1], reverse=True):
                st.progress(score/10, text=f"{model}: {score}")

        st.divider()
        st.subheader("Generated Response")
        with st.spinner("Generating response..."):
            response = client.generate(result["selected_model"], query)

        if response["success"]:
            st.markdown(response["response"])
        else:
            st.error(f"Error: {response['response']}")
