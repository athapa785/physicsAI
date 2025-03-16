#!/usr/bin/env python3
"""
PhysicsAI Application Entry Point

This script serves as the main entry point for the PhysicsAI application.
It launches the Streamlit application using the streamlit CLI.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run the PhysicsAI Streamlit application."""
    # Get the path to the app directory
    project_root = Path(__file__).parent
    app_path = project_root / "app" / "streamlit_app.py"
    
    # Run the Streamlit application
    print(f"Starting PhysicsAI application from {app_path}...")
    subprocess.run(["streamlit", "run", str(app_path)])

if __name__ == "__main__":
    main()
