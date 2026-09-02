import streamlit as st

st.set_page_config(
    page_title="Judge",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Debate Judge")

if "debate_result" not in st.session_state:

    st.warning("No debate has been conducted.")

    st.stop()

result = st.session_state["debate_result"]

st.subheader("Judgement")

st.write(result["judgement"])

