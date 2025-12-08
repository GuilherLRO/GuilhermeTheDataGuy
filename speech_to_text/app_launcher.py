import streamlit as st
import subprocess
import sys
import os

# Page configuration
st.set_page_config(
    page_title="App Launcher",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 3rem;
    }
    .app-card {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: transform 0.2s;
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .app-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #495057;
        margin-bottom: 1rem;
    }
    .app-description {
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .launch-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        cursor: pointer;
        width: 100%;
    }
    .launch-button:hover {
        background-color: #218838;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 App Launcher</h1>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <p style='font-size: 1.2rem; color: #6c757d;'>
        Choose an application to launch
    </p>
</div>
""", unsafe_allow_html=True)

# App cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="app-card">
        <div class="app-title">🎤 Audio Transcription</div>
        <div class="app-description">
            Convert audio files to text using OpenAI Whisper with easy copy-to-clipboard functionality
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Audio Transcription", key="audio_app", use_container_width=True):
        st.info("🚀 Launching Audio Transcription App...")
        # Note: In a real deployment, you would redirect to the app
        st.markdown("**To launch the Audio Transcription app, run:**")
        st.code("streamlit run streamlit_app.py")

with col2:
    st.markdown("""
    <div class="app-card">
        <div class="app-title">🎬 Video Converter</div>
        <div class="app-description">
            Convert video formats, especially MOV to MP4, with quality and compression options
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Video Converter", key="video_app", use_container_width=True):
        st.info("🚀 Launching Video Converter App...")
        # Note: In a real deployment, you would redirect to the app
        st.markdown("**To launch the Video Converter app, run:**")
        st.code("streamlit run video_converter_app.py")

with col3:
    st.markdown("""
    <div class="app-card">
        <div class="app-title">🎵 Video to Audio</div>
        <div class="app-description">
            Extract audio from video files in various formats (MP3, WAV, M4A, FLAC, OGG)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Video to Audio", key="video_to_audio_app", use_container_width=True):
        st.info("🚀 Launching Video to Audio Converter App...")
        # Note: In a real deployment, you would redirect to the app
        st.markdown("**To launch the Video to Audio Converter app, run:**")
        st.code("streamlit run video_to_audio_app.py")

# Instructions section
st.markdown("---")
st.markdown("### 📋 How to Use")

st.markdown("""
**Option 1: Use this launcher**
1. Click the launch button for your desired app
2. Follow the terminal instructions shown

**Option 2: Direct terminal commands**
```bash
# For Audio Transcription
streamlit run streamlit_app.py

# For Video Converter  
streamlit run video_converter_app.py

# For Video to Audio Converter
streamlit run video_to_audio_app.py
```

**Option 3: Run all apps simultaneously**
```bash
# Terminal 1
streamlit run streamlit_app.py --server.port 8501

# Terminal 2  
streamlit run video_converter_app.py --server.port 8502

# Terminal 3
streamlit run video_to_audio_app.py --server.port 8503
```
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 App Launcher | Built with Streamlit</p>
    <p><small>Audio Transcription, Video Conversion & Video-to-Audio Tools</small></p>
</div>
""", unsafe_allow_html=True)

