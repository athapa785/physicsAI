import streamlit as st

st.set_page_config(
    page_title="PhysicsAI",
    page_icon="🔭",
    layout="wide"
)

st.title("PhysicsAI - Physics Education Platform")
st.markdown("### Welcome to PhysicsAI!")

st.info("""
This is a simplified deployment test version of PhysicsAI.
The full application includes:
- RAG-enhanced physics lessons based on University Physics textbook
- FAISS vector store for efficient similarity search
- OpenAI embeddings for text vectorization
- Interactive chapter and topic navigation
- Context-aware question answering
""")

# Add a simple interactive element
if st.button("Test Deployment"):
    st.success("✅ Success! Your Streamlit Cloud deployment is working correctly.")
    st.balloons()

# Display deployment information
st.markdown("---")
st.subheader("Deployment Information")
st.code("""
Repository: github.com/athapa785/physicsAI
Branch: streamlit-deploy
Main file: streamlit_cloud.py
""")
