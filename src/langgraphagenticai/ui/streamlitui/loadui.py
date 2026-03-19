import streamlit as st
import os
from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def initialize_session(self):
        return {
            "current_step": "requirements",
            "requirements": "",
            "user_stories": "",
            "po_feedback": "",
            "generated_code": "",
            "review_feedback": "",
            "decision": None
        }

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        # Only initialize session state keys if not already set
        if "timeframe" not in st.session_state:
            st.session_state.timeframe = ''
        if "IsFetchButtonClicked" not in st.session_state:
            st.session_state.IsFetchButtonClicked = False
        if "IsSDLC" not in st.session_state:
            st.session_state.IsSDLC = False
        if "state" not in st.session_state:
            st.session_state.state = self.initialize_session()

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input(
                    "GROQ API Key", type="password"
                )
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key. Get one at: https://console.groq.com/keys")

            # Use case selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot with Tool", "AI News"]:
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state[
                    "TAVILY_API_KEY"
                ] = st.text_input("TAVILY API Key", type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API key. Get one at: https://app.tavily.com/home")

            # AI News specific controls — separated from key validation
            if self.user_controls["selected_usecase"] == "AI News":
                st.subheader("📰 AI News Explorer")

                time_frame = st.selectbox(
                    "📅 Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )

                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame
                else:
                    st.session_state.IsFetchButtonClicked = False

        return self.user_controls