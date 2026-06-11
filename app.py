import streamlit as st
from src.generator import generate_answer

st.title("QuantMind: AI Financial Analyst")
st.caption("Analyzing over SEC filings, latest news, and financial metrics")

# Query
question = st.text_area(
    "Ask anything about a company",
    placeholder="Give me a fundamental analysis of Apple"
)
# Button
if st.button("Analyze"):
    if not question:
        st.error("Please enter a question")
    else:
        st.markdown("## Analysis")
        st.write_stream(generate_answer(question))