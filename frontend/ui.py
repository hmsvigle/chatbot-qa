import streamlit as st
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

from services.chatbot_service import ChatbotService

class ChatbotUI:
    def __init__(self):
        self.page_config()
        self.initialize_session_state()
    
    def page_config(self):
        st.set_page_config(
            page_title="Ejari Chatbot",
            page_icon="🏠",
            layout="centered"
        )
    
    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "chatbot_service" not in st.session_state:
            st.session_state.chatbot_service = None
            st.session_state.initialized = False
    
    @st.cache_resource
    def initialize_chatbot_service(_self):
        service = ChatbotService()
        if service.initialize():
            return service
        return None
    
    def render_header(self):
        st.title("🏠 Ejari Chatbot")
        st.markdown("Welcome! I'm here to help you with Ejari-related queries.")
    
    def render_sidebar(self):
        with st.sidebar:
            st.header("ℹ️ Information")
            if st.session_state.chatbot_service:
                st.info(st.session_state.chatbot_service.get_stats())
            
            st.markdown("---")
            st.subheader("🔧 Settings")
            
            # Threshold adjustment
            threshold = st.slider(
                "Similarity Threshold",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Lower values return more results but may be less accurate"
            )
            
            if st.session_state.chatbot_service:
                st.session_state.chatbot_service.update_threshold(threshold)
            
            st.markdown("---")
            st.markdown("**Sample Questions:**")
            st.markdown("- What is Ejari?")
            st.markdown("- How do I register my tenancy contract?")
            st.markdown("- What documents are required?")
    
    def render_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def handle_user_input(self):
        if prompt := st.chat_input("Ask me anything about Ejari..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate assistant response
            if st.session_state.chatbot_service:
                with st.chat_message("assistant"):
                    with st.spinner("Searching for answer..."):
                        response = st.session_state.chatbot_service.process_query(prompt)
                    st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                with st.chat_message("assistant"):
                    error_msg = "Sorry, the chatbot is not properly initialized. Please refresh the page."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    def render_footer(self):
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: gray; font-size: 0.8em;'>
                Ejari Chatbot | Powered by Sentence Transformers & Streamlit
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    def run(self):
        self.render_header()
        
        # Initialize chatbot service
        if not st.session_state.initialized:
            with st.spinner("Initializing chatbot... This may take a moment on first run."):
                st.session_state.chatbot_service = self.initialize_chatbot_service()
                if st.session_state.chatbot_service:
                    st.session_state.initialized = True
                    st.success("Chatbot initialized successfully!")
                else:
                    st.error("Failed to initialize chatbot. Please check your setup.")
                    st.stop()
        
        self.render_sidebar()
        self.render_chat_history()
        self.handle_user_input()
        self.render_footer()

if __name__ == "__main__":
    app = ChatbotUI()
    app.run()