import streamlit as st

st.title("PhysicsAI Test Deployment")
st.write("If you can see this, the deployment is working correctly!")

# Add a simple interactive element
if st.button("Click me"):
    st.success("Success! Your Streamlit Cloud deployment is working.")
