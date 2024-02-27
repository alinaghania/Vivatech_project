import streamlit as st


def run():
    

    st.set_page_config(
        page_title="GPT-4V Demos",
        page_icon="🤖",
        initial_sidebar_state="expanded",
    )

    st.sidebar.caption(":red[How can i assist you today ?]")

    st.write("# Car Accident ? 🚗")
    st.write("\n")
    st.info(
        "I am here to help you with your vision tasks! 🤖"
    )
    st.info("Open them from the sidebar!", icon="↖️")
    st.caption(
        """ HELLO HELLO MY NAME IS GPT-4V AND I AM YOUR ASSURANCE BOT 🤖 """
    )
    st.write("\n")
   

if __name__ == "__main__":
    run()
