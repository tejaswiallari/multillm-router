import sys
sys.path.insert(0, ".")
import streamlit as st
from src.utils.router import Router
from src.models.groq_client import GroqClient

st.set_page_config(page_title="Multi-LLM Router", page_icon="🤖", layout="wide")
st.title("🤖 Multi-LLM Intelligent Routing System")
st.markdown("*Automatically routes your query to the best AI model with full explainability*")
st.divider()

router = Router()
client = GroqClient()

query = st.text_area("Enter your query:", height=100)

if st.button("Route and Generate", type="primary"):
    if query.strip() == "":
        st.warning("Please enter a query!")
    else:
        result = router.route(query)
        features = result["features"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📊 Query Analysis")
            st.metric("Query Type", features.query_type.upper())
            st.metric("Complexity", features.complexity.upper())
            st.metric("Domain", features.domain.upper())
            st.metric("Word Count", features.word_count)

        with col2:
            st.subheader("📈 Model Scores")
            for model, score in sorted(result["scores"].items(), key=lambda x: x[1], reverse=True):
                st.progress(score/10, text=f"{model}: {score}")

        with col3:
            st.subheader("🎯 Routing Decision")
            st.metric("Selected Model", result["selected_model"].upper())
            st.success(f"Best model for {features.query_type} queries in {features.domain} domain")

        st.divider()

        st.subheader("💡 Why this model was selected?")
        selected = result["selected_model"]
        score = result["scores"][selected]
        other_models = {k: v for k, v in result["scores"].items() if k != selected}
        best_other = max(other_models, key=other_models.get)
        advantage = round(score - other_models[best_other], 2)

        st.info(f"""
**Selected Model:** {selected}

**Query Type:** {features.query_type} — this model has the highest capability score for this type

**Complexity Level:** {features.complexity} — routing weight adjusted accordingly

**Domain:** {features.domain}

**Score Advantage:** {selected} scored {advantage} points higher than {best_other} ({other_models[best_other]})

**Final Score:** {score} / 10
        """)

        st.divider()
        st.subheader("💬 Generated Response")
        with st.spinner("Generating response..."):
            response = client.generate(result["selected_model"], query)

        if response["success"]:
            st.markdown(response["response"])
        else:
            st.error(f"Error: {response['response']}")
