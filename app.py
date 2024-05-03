import streamlit as st

def run():
    st.set_page_config(
        page_title="Your Mechano 🚗",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    # API key input via sidebar
    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if not api_key:
        st.sidebar.error("An OpenAI API key is required to use this application.")

    st.sidebar.caption(":red[How can I assist you today?]")

    st.write("# AUTO INSIGHT 🚗")
    st.write("\n")
    st.info("I am here to help you 🤖")
    st.info("Open them from the sidebar!", icon="↖️")
    st.caption("by Yoan & Alina")
    st.write("\n")

if __name__ == "__main__":
    run()
