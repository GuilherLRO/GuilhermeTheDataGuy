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
    page_title="Video Format Converter",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff6b6b;
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
st.markdown('<h1 class="main-header">🎬 Video Format Converter</h1>', unsafe_allow_html=True)

# Sidebar for conversion settings
with st.sidebar:
    st.header("⚙️ Conversion Settings")
    
    # Output format selection
    output_formats = {
        "mp4": "MP4 (H.264)",
        "avi": "AVI",
        "mkv": "MKV",
        "webm": "WebM",
        "mov": "MOV (QuickTime)"
    }
    
    selected_format = st.selectbox(
        "Convert to:",
        options=list(output_formats.keys()),
        index=0,  # Default to MP4
        format_func=lambda x: output_formats[x]
    )
    
    st.markdown("---")
    
    # Quality settings
    st.subheader("🎯 Quality Settings")
    
    quality_presets = {
        "high": "High Quality (slower, larger file)",
        "medium": "Medium Quality (balanced)",
        "low": "Low Quality (faster, smaller file)",
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
        
        video_bitrate = st.slider(
            "Video Bitrate (kbps):",
            min_value=500,
            max_value=10000,
            value=2000,
            step=100
        )
        
        audio_bitrate = st.slider(
            "Audio Bitrate (kbps):",
            min_value=64,
            max_value=320,
            value=128,
            step=32
        )
        
        resolution = st.selectbox(
            "Resolution:",
            options=["original", "1920x1080", "1280x720", "854x480", "640x360"],
            index=0
        )
    
    st.markdown("---")
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        remove_audio = st.checkbox("Remove Audio", value=False)
        compress_video = st.checkbox("Compress Video", value=True)
        preserve_metadata = st.checkbox("Preserve Metadata", value=True)
    
    st.markdown("---")
    
    # Supported formats info
    st.info("""
    **Supported Input Formats:**
    - MOV, MP4, AVI, MKV
    - WebM, FLV, WMV
    - Maximum file size: 1GB (configurable)
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload Video File")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a video file to convert",
        type=['mov', 'mp4', 'avi', 'mkv', 'webm', 'flv', 'wmv'],
        help="Upload a video file to convert to your desired format"
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
            if st.button("🔄 Convert Video", type="primary", use_container_width=True):
                with st.spinner("🔄 Converting video..."):
                    try:
                        # Create temporary files
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as input_tmp:
                            input_tmp.write(uploaded_file.getvalue())
                            input_path = input_tmp.name
                        
                        # Generate output filename
                        original_name = Path(uploaded_file.name).stem
                        output_filename = f"{original_name}_converted.{selected_format}"
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{selected_format}") as output_tmp:
                            output_path = output_tmp.name
                        
                        # Build FFmpeg command
                        cmd = ["ffmpeg", "-i", input_path, "-y"]  # -y to overwrite output file
                        
                        # Add quality settings
                        if quality_preset == "custom":
                            cmd.extend(["-b:v", f"{video_bitrate}k"])
                            cmd.extend(["-b:a", f"{audio_bitrate}k"])
                            
                            if resolution != "original":
                                cmd.extend(["-s", resolution])
                        elif quality_preset == "high":
                            cmd.extend(["-crf", "18", "-preset", "slow"])
                        elif quality_preset == "medium":
                            cmd.extend(["-crf", "23", "-preset", "medium"])
                        elif quality_preset == "low":
                            cmd.extend(["-crf", "28", "-preset", "fast"])
                        
                        # Add format-specific options
                        if selected_format == "mp4":
                            cmd.extend(["-c:v", "libx264", "-c:a", "aac"])
                        elif selected_format == "webm":
                            cmd.extend(["-c:v", "libvpx-vp9", "-c:a", "libopus"])
                        elif selected_format == "avi":
                            cmd.extend(["-c:v", "libx264", "-c:a", "mp3"])
                        
                        # Advanced options
                        if remove_audio:
                            cmd.extend(["-an"])
                        
                        if compress_video and quality_preset != "custom":
                            cmd.extend(["-movflags", "+faststart"])
                        
                        if not preserve_metadata:
                            cmd.extend(["-map_metadata", "-1"])
                        
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
                            st.session_state.converted_file_path = output_path
                            st.session_state.converted_filename = output_filename
                            st.session_state.conversion_time = end_time - start_time
                            st.session_state.output_size_mb = output_size_mb
                            
                            st.success("✅ Video converted successfully!")
                            
                        else:
                            st.error(f"❌ Conversion failed: {result.stderr}")
                            # Clean up output file if it exists
                            if os.path.exists(output_path):
                                os.unlink(output_path)
                    
                    except Exception as e:
                        st.error(f"❌ Error during conversion: {str(e)}")
                        # Clean up files
                        if 'input_path' in locals() and os.path.exists(input_path):
                            os.unlink(input_path)
                        if 'output_path' in locals() and os.path.exists(output_path):
                            os.unlink(output_path)

with col2:
    st.header("📥 Download Converted Video")
    
    if 'converted_file_path' in st.session_state and st.session_state.converted_file_path:
        # Display conversion info
        st.markdown('<div class="conversion-box">', unsafe_allow_html=True)
        
        st.markdown(f"**📁 Original File:** {uploaded_file.name}")
        st.markdown(f"**📁 Converted File:** {st.session_state.converted_filename}")
        st.markdown(f"**⏱️ Conversion Time:** {st.session_state.conversion_time:.2f} seconds")
        st.markdown(f"**📊 Output Size:** {st.session_state.output_size_mb:.2f} MB")
        st.markdown(f"**🎯 Format:** {selected_format.upper()}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        with open(st.session_state.converted_file_path, "rb") as file:
            st.download_button(
                label="📥 Download Converted Video",
                data=file.read(),
                file_name=st.session_state.converted_filename,
                mime=f"video/{selected_format}",
                use_container_width=True,
                type="primary"
            )
        
        # Clean up button
        if st.button("🗑️ Clear Results", use_container_width=True):
            if os.path.exists(st.session_state.converted_file_path):
                os.unlink(st.session_state.converted_file_path)
            # Clear session state
            for key in ['converted_file_path', 'converted_filename', 'conversion_time', 'output_size_mb']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    else:
        st.info("👆 Upload a video file and click 'Convert Video' to see results here.")

# Progress and status section
if 'conversion_time' in st.session_state:
    st.markdown("---")
    st.markdown("### 📊 Conversion Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Conversion Time", f"{st.session_state.conversion_time:.2f}s")
    
    with col2:
        original_size = uploaded_file.size / (1024*1024)
        compression_ratio = (original_size - st.session_state.output_size_mb) / original_size * 100
        st.metric("Size Reduction", f"{compression_ratio:.1f}%")
    
    with col3:
        st.metric("Output Size", f"{st.session_state.output_size_mb:.2f} MB")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎬 Video Converter powered by FFmpeg | Built with Streamlit</p>
    <p><small>Supports MOV, MP4, AVI, MKV, WebM, FLV, WMV formats</small></p>
</div>
""", unsafe_allow_html=True)

