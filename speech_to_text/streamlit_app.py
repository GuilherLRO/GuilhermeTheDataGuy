import streamlit as st
import whisper
import tempfile
import os
import pyperclip
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Audio Transcription with Whisper",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .transcription-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .copy-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .copy-button:hover {
        background-color: #218838;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎤 Audio Transcription with Whisper</h1>', unsafe_allow_html=True)

# Sidebar for model selection and settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    model_options = {
        "tiny": "Tiny (fastest, least accurate)",
        "base": "Base (fast, less accurate)", 
        "small": "Small (balanced)",
        "medium": "Medium (good balance)",
        "large": "Large (slowest, most accurate)"
    }
    
    selected_model = st.selectbox(
        "Select Whisper Model:",
        options=list(model_options.keys()),
        index=3,  # Default to medium
        format_func=lambda x: f"{x.title()} - {model_options[x]}"
    )
    
    st.markdown("---")
    
    # Language selection (optional)
    language_options = {
        "auto": "Auto-detect",
        "en": "English",
        "pt": "Portuguese", 
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese"
    }
    
    selected_language = st.selectbox(
        "Select Language (optional):",
        options=list(language_options.keys()),
        index=0,
        format_func=lambda x: language_options[x]
    )
    
    st.markdown("---")
    
    # Supported formats info
    st.info("""
    **Supported Formats:**
    - MP3, MP4, WAV, M4A, FLAC
    - OGG, WEBM, AVI, MOV
    - Maximum file size: 1GB (configurable)
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload Audio File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'mp4', 'wav', 'm4a', 'flac', 'ogg', 'webm', 'avi', 'mov'],
        help="Upload an audio or video file to transcribe"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"📊 File size: {uploaded_file.size / (1024*1024):.2f} MB")
        
        # Transcribe button
        if st.button("🎯 Start Transcription", type="primary", use_container_width=True):
            with st.spinner("🔄 Loading Whisper model and transcribing..."):
                try:
                    # Load the selected model
                    @st.cache_resource
                    def load_whisper_model(model_name):
                        return whisper.load_model(model_name)
                    
                    model = load_whisper_model(selected_model)
                    
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Transcribe
                    language = None if selected_language == "auto" else selected_language
                    result = model.transcribe(tmp_file_path, language=language, verbose=False)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    # Store results in session state
                    st.session_state.transcription_result = result
                    st.session_state.transcription_text = result["text"]
                    st.session_state.transcription_segments = result.get("segments", [])
                    st.session_state.transcription_language = result.get("language", "unknown")
                    
                    st.success("✅ Transcription completed successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Error during transcription: {str(e)}")
                    st.session_state.transcription_result = None

with col2:
    st.header("📝 Transcription Results")
    
    if 'transcription_result' in st.session_state and st.session_state.transcription_result:
        result = st.session_state.transcription_result
        
        # Language detection result
        if 'transcription_language' in st.session_state:
            detected_lang = st.session_state.transcription_language
            st.info(f"🌍 Detected language: {detected_lang.upper()}")
        
        # Transcription text
        transcription_text = st.session_state.transcription_text
        
        # Copy to clipboard button
        col_copy1, col_copy2 = st.columns([1, 1])
        
        with col_copy1:
            if st.button("📋 Copy Text", use_container_width=True):
                try:
                    pyperclip.copy(transcription_text)
                    st.success("✅ Text copied to clipboard!")
                except Exception as e:
                    st.error(f"❌ Failed to copy to clipboard: {str(e)}")
        
        with col_copy2:
            if st.button("📋 Copy Markdown", use_container_width=True):
                try:
                    # Format as markdown with timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    markdown_text = f"""# Audio Transcription

**File:** {uploaded_file.name}  
**Date:** {timestamp}  
**Model:** {selected_model.title()}  
**Language:** {st.session_state.transcription_language.upper()}

## Transcription

{transcription_text}
"""
                    pyperclip.copy(markdown_text)
                    st.success("✅ Markdown copied to clipboard!")
                except Exception as e:
                    st.error(f"❌ Failed to copy to clipboard: {str(e)}")
        
        # Display transcription in a nice box
        st.markdown('<div class="transcription-box">', unsafe_allow_html=True)
        st.text_area(
            "Transcription:",
            value=transcription_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed segments (expandable)
        if st.session_state.transcription_segments:
            with st.expander("📊 View Detailed Segments"):
                for i, segment in enumerate(st.session_state.transcription_segments):
                    start_time = segment.get('start', 0)
                    end_time = segment.get('end', 0)
                    text = segment.get('text', '').strip()
                    
                    st.write(f"**{i+1}.** `{start_time:.1f}s - {end_time:.1f}s`")
                    st.write(text)
                    st.write("---")
    
    else:
        st.info("👆 Upload an audio file and click 'Start Transcription' to see results here.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎤 Audio Transcription powered by OpenAI Whisper | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

