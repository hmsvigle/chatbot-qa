#!/usr/bin/env python3

"""
Main entry point for the Ejari Chatbot application.
This file serves as the launcher for the Streamlit frontend.
"""

import sys
from pathlib import Path

# Add frontend to path
frontend_path = Path(__file__).parent / "frontend"
sys.path.append(str(frontend_path))

from ui import ChatbotUI

if __name__ == "__main__":
    app = ChatbotUI()
    app.run()