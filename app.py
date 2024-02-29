import streamlit as st


def run():
    

    st.set_page_config(
        page_title="Your mechano 🚗",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    st.sidebar.caption(":red[How can i assist you today ?]")

    st.write("# AUTO INSIGHT 🚗")
    st.write("\n")
    st.info(
        "I am here to help you 🤖"
    )
    st.info("Open them from the sidebar!", icon="↖️")
    st.caption(
        """ by Yoan & Alina """
    )
    st.write("\n")
   

if __name__ == "__main__":
    run()
