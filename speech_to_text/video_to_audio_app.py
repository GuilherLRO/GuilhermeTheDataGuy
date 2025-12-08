import streamlit as st
import subprocess
import tempfile
import os
import shutil
from pathlib import Path
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Video to Audio Converter",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #9b59b6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .conversion-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-info {
        color: #17a2b8;
        font-weight: bold;
    }
    .download-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .download-button:hover {
        background-color: #0056b3;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎵 Video to Audio Converter</h1>', unsafe_allow_html=True)

# Sidebar for conversion settings
with st.sidebar:
    st.header("⚙️ Audio Settings")
    
    # Output format selection
    audio_formats = {
        "mp3": "MP3 (most compatible)",
        "wav": "WAV (uncompressed)",
        "m4a": "M4A (AAC)",
        "flac": "FLAC (lossless)",
        "ogg": "OGG (Vorbis)",
        "aac": "AAC"
    }
    
    selected_format = st.selectbox(
        "Convert to:",
        options=list(audio_formats.keys()),
        index=0,  # Default to MP3
        format_func=lambda x: audio_formats[x]
    )
    
    st.markdown("---")
    
    # Audio quality settings
    st.subheader("🎯 Audio Quality")
    
    quality_presets = {
        "high": "High Quality (320 kbps)",
        "medium": "Medium Quality (192 kbps)",
        "low": "Low Quality (128 kbps)",
        "custom": "Custom Settings"
    }
    
    quality_preset = st.selectbox(
        "Quality Preset:",
        options=list(quality_presets.keys()),
        index=1,  # Default to medium
        format_func=lambda x: quality_presets[x]
    )
    
    # Custom quality settings
    if quality_preset == "custom":
        st.markdown("**Custom Settings:**")
        
        audio_bitrate = st.slider(
            "Audio Bitrate (kbps):",
            min_value=64,
            max_value=320,
            value=192,
            step=32
        )
        
        sample_rate = st.selectbox(
            "Sample Rate:",
            options=["original", "44100", "48000", "22050", "16000"],
            index=0
        )
        
        channels = st.selectbox(
            "Channels:",
            options=["original", "mono", "stereo"],
            index=0
        )
    
    st.markdown("---")
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        normalize_audio = st.checkbox("Normalize Audio", value=True, help="Adjust volume levels")
        remove_silence = st.checkbox("Remove Silence", value=False, help="Remove silent parts")
        fade_in_out = st.checkbox("Add Fade In/Out", value=False, help="Add 1-second fade effects")
    
    st.markdown("---")
    
    # Supported formats info
    st.info("""
    **Supported Input Formats:**
    - MOV, MP4, AVI, MKV
    - WebM, FLV, WMV, 3GP
    - Maximum file size: 1GB (configurable)
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload Video File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a video file to extract audio from",
        type=['mov', 'mp4', 'avi', 'mkv', 'webm', 'flv', 'wmv', '3gp'],
        help="Upload a video file to extract audio"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_size_mb = uploaded_file.size / (1024*1024)
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"📊 File size: {file_size_mb:.2f} MB")
        
        # Check file size limit
        if file_size_mb > 1000:  # 1GB limit
            st.error("❌ File size exceeds 1GB limit. Please choose a smaller file.")
        else:
            # Convert button
            if st.button("🎵 Extract Audio", type="primary", use_container_width=True):
                with st.spinner("🔄 Extracting audio from video..."):
                    try:
                        # Create temporary files
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as input_tmp:
                            input_tmp.write(uploaded_file.getvalue())
                            input_path = input_tmp.name
                        
                        # Generate output filename
                        original_name = Path(uploaded_file.name).stem
                        output_filename = f"{original_name}_audio.{selected_format}"
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{selected_format}") as output_tmp:
                            output_path = output_tmp.name
                        
                        # Build FFmpeg command
                        cmd = ["ffmpeg", "-i", input_path, "-y"]  # -y to overwrite output file
                        
                        # Add audio quality settings
                        if quality_preset == "custom":
                            cmd.extend(["-b:a", f"{audio_bitrate}k"])
                            
                            if sample_rate != "original":
                                cmd.extend(["-ar", sample_rate])
                            
                            if channels != "original":
                                if channels == "mono":
                                    cmd.extend(["-ac", "1"])
                                elif channels == "stereo":
                                    cmd.extend(["-ac", "2"])
                        elif quality_preset == "high":
                            cmd.extend(["-b:a", "320k"])
                        elif quality_preset == "medium":
                            cmd.extend(["-b:a", "192k"])
                        elif quality_preset == "low":
                            cmd.extend(["-b:a", "128k"])
                        
                        # Add format-specific codec options
                        if selected_format == "mp3":
                            cmd.extend(["-c:a", "libmp3lame"])
                        elif selected_format == "wav":
                            cmd.extend(["-c:a", "pcm_s16le"])
                        elif selected_format == "m4a":
                            cmd.extend(["-c:a", "aac"])
                        elif selected_format == "flac":
                            cmd.extend(["-c:a", "flac"])
                        elif selected_format == "ogg":
                            cmd.extend(["-c:a", "libvorbis"])
                        elif selected_format == "aac":
                            cmd.extend(["-c:a", "aac"])
                        
                        # Advanced audio processing
                        if normalize_audio:
                            cmd.extend(["-af", "loudnorm"])
                        
                        if remove_silence:
                            cmd.extend(["-af", "silenceremove=start_periods=1:start_duration=1:start_threshold=-50dB"])
                        
                        if fade_in_out:
                            cmd.extend(["-af", "afade=t=in:ss=0:d=1,afade=t=out:st=-1:d=1"])
                        
                        # Add output path
                        cmd.append(output_path)
                        
                        # Run FFmpeg command
                        start_time = time.time()
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        end_time = time.time()
                        
                        # Clean up input file
                        os.unlink(input_path)
                        
                        if result.returncode == 0:
                            # Get output file size
                            output_size = os.path.getsize(output_path)
                            output_size_mb = output_size / (1024*1024)
                            
                            # Store in session state
                            st.session_state.extracted_audio_path = output_path
                            st.session_state.extracted_filename = output_filename
                            st.session_state.extraction_time = end_time - start_time
                            st.session_state.output_size_mb = output_size_mb
                            
                            st.success("✅ Audio extracted successfully!")
                            
                        else:
                            st.error(f"❌ Audio extraction failed: {result.stderr}")
                            # Clean up output file if it exists
                            if os.path.exists(output_path):
                                os.unlink(output_path)
                    
                    except Exception as e:
                        st.error(f"❌ Error during audio extraction: {str(e)}")
                        # Clean up files
                        if 'input_path' in locals() and os.path.exists(input_path):
                            os.unlink(input_path)
                        if 'output_path' in locals() and os.path.exists(output_path):
                            os.unlink(output_path)

with col2:
    st.header("📥 Download Extracted Audio")
    
    if 'extracted_audio_path' in st.session_state and st.session_state.extracted_audio_path:
        # Display extraction info
        st.markdown('<div class="conversion-box">', unsafe_allow_html=True)
        
        st.markdown(f"**📁 Original Video:** {uploaded_file.name}")
        st.markdown(f"**🎵 Audio File:** {st.session_state.extracted_filename}")
        st.markdown(f"**⏱️ Extraction Time:** {st.session_state.extraction_time:.2f} seconds")
        st.markdown(f"**📊 Audio Size:** {st.session_state.output_size_mb:.2f} MB")
        st.markdown(f"**🎯 Format:** {selected_format.upper()}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        with open(st.session_state.extracted_audio_path, "rb") as file:
            st.download_button(
                label="📥 Download Audio File",
                data=file.read(),
                file_name=st.session_state.extracted_filename,
                mime=f"audio/{selected_format}",
                use_container_width=True,
                type="primary"
            )
        
        # Clean up button
        if st.button("🗑️ Clear Results", use_container_width=True):
            if os.path.exists(st.session_state.extracted_audio_path):
                os.unlink(st.session_state.extracted_audio_path)
            # Clear session state
            for key in ['extracted_audio_path', 'extracted_filename', 'extraction_time', 'output_size_mb']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    else:
        st.info("👆 Upload a video file and click 'Extract Audio' to see results here.")

# Progress and status section
if 'extraction_time' in st.session_state:
    st.markdown("---")
    st.markdown("### 📊 Extraction Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Extraction Time", f"{st.session_state.extraction_time:.2f}s")
    
    with col2:
        original_size = uploaded_file.size / (1024*1024)
        compression_ratio = (original_size - st.session_state.output_size_mb) / original_size * 100
        st.metric("Size Reduction", f"{compression_ratio:.1f}%")
    
    with col3:
        st.metric("Audio Size", f"{st.session_state.output_size_mb:.2f} MB")

# Usage tips
st.markdown("---")
st.markdown("### 💡 Usage Tips")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🎯 Quality Recommendations:**
    - **High Quality (320 kbps)**: Music, podcasts
    - **Medium Quality (192 kbps)**: General use, voice recordings
    - **Low Quality (128 kbps)**: Quick previews, storage optimization
    """)

with col2:
    st.markdown("""
    **📁 Format Recommendations:**
    - **MP3**: Most compatible, good compression
    - **WAV**: Uncompressed, highest quality
    - **M4A**: Apple devices, good compression
    - **FLAC**: Lossless compression
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎵 Video to Audio Converter powered by FFmpeg | Built with Streamlit</p>
    <p><small>Extract audio from MOV, MP4, AVI, MKV, WebM, FLV, WMV, 3GP formats</small></p>
</div>
""", unsafe_allow_html=True)
