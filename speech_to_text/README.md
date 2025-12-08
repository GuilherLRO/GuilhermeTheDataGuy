# Audio & Video Processing Apps - Streamlit Collection

A collection of user-friendly Streamlit applications for audio transcription, video format conversion, and video-to-audio extraction.

## 🎤 Audio Transcription App
Transcribe audio files using OpenAI's Whisper model with easy copy-to-clipboard functionality.

## 🎬 Video Converter App  
Convert video formats, especially MOV to MP4, with quality and compression options.

## 🎵 Video to Audio Converter App
Extract audio from video files in various formats (MP3, WAV, M4A, FLAC, OGG, AAC).

## Features

- 🎤 **Audio Upload**: Support for multiple audio/video formats (MP3, MP4, WAV, M4A, FLAC, OGG, WEBM, AVI, MOV)
- 🤖 **Whisper Models**: Choose from different Whisper model sizes (tiny, base, small, medium, large)
- 🌍 **Language Detection**: Automatic language detection or manual language selection
- 📝 **Markdown Output**: Formatted transcription with timestamps and metadata
- 📋 **Copy to Clipboard**: Easy one-click copying of plain text or formatted markdown
- 📊 **Detailed Segments**: View transcription with timestamps for each segment
- 🎨 **Modern UI**: Clean, responsive interface with custom styling

## Installation

1. **Clone or navigate to the speech_to_text directory**
   ```bash
   cd speech_to_text
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Choose how to run the apps:**

   **Option A: Use the App Launcher**
   ```bash
   streamlit run app_launcher.py
   ```

   **Option B: Run individual apps**
   ```bash
   # Audio Transcription App
   streamlit run streamlit_app.py
   
   # Video Converter App
   streamlit run video_converter_app.py
   
   # Video to Audio Converter App
   streamlit run video_to_audio_app.py
   ```

   **Option C: Run all apps simultaneously**
   ```bash
   # Terminal 1 - Audio Transcription (port 8501)
   streamlit run streamlit_app.py --server.port 8501
   
   # Terminal 2 - Video Converter (port 8502)  
   streamlit run video_converter_app.py --server.port 8502
   
   # Terminal 3 - Video to Audio Converter (port 8503)
   streamlit run video_to_audio_app.py --server.port 8503
   ```

4. **Open your browser** and navigate to the appropriate URL

## 🎤 Audio Transcription Usage

1. **Upload Audio**: Use the file uploader to select your audio or video file
2. **Select Model**: Choose the Whisper model size based on your speed/accuracy needs:
   - **Tiny**: Fastest, least accurate
   - **Base**: Fast, less accurate
   - **Small**: Balanced
   - **Medium**: Good balance (recommended)
   - **Large**: Slowest, most accurate
3. **Choose Language**: Select "Auto-detect" or specify the language
4. **Transcribe**: Click "Start Transcription" and wait for processing
5. **Copy Results**: Use the copy buttons to copy plain text or formatted markdown

## 🎬 Video Converter Usage

1. **Upload Video**: Use the file uploader to select your video file (MOV, MP4, AVI, etc.)
2. **Select Output Format**: Choose your desired output format (MP4, AVI, MKV, WebM, MOV)
3. **Choose Quality**: Select quality preset or customize settings:
   - **High**: Best quality, larger file size
   - **Medium**: Balanced quality and size
   - **Low**: Smaller file, faster processing
   - **Custom**: Set your own bitrate and resolution
4. **Advanced Options**: Configure audio removal, compression, metadata preservation
5. **Convert**: Click "Convert Video" and wait for processing
6. **Download**: Download your converted video file

## 🎵 Video to Audio Converter Usage

1. **Upload Video**: Use the file uploader to select your video file (MOV, MP4, AVI, etc.)
2. **Select Audio Format**: Choose your desired audio format (MP3, WAV, M4A, FLAC, OGG, AAC)
3. **Choose Quality**: Select quality preset or customize settings:
   - **High**: 320 kbps (best quality)
   - **Medium**: 192 kbps (balanced)
   - **Low**: 128 kbps (smaller file)
   - **Custom**: Set your own bitrate, sample rate, and channels
4. **Advanced Options**: Configure audio normalization, silence removal, fade effects
5. **Extract**: Click "Extract Audio" and wait for processing
6. **Download**: Download your extracted audio file

## Model Performance

| Model  | Size  | Speed | Accuracy | Use Case |
|--------|-------|-------|----------|----------|
| Tiny   | ~39MB | Fastest | Basic | Quick drafts |
| Base   | ~74MB | Fast | Good | General use |
| Small  | ~244MB | Medium | Better | Balanced |
| Medium | ~769MB | Slower | High | High quality |
| Large  | ~1550MB | Slowest | Best | Professional |

## Supported Formats

- **Audio**: MP3, WAV, M4A, FLAC, OGG, AAC
- **Video**: MP4, WEBM, AVI, MOV, MKV, FLV, WMV, 3GP
- **Maximum file size**: 1GB (configurable via Streamlit settings)

## Example Output

The app generates both plain text and markdown formatted transcriptions:

```markdown
# Audio Transcription

**File:** audio_sample.mp3  
**Date:** 2024-01-15 14:30:25  
**Model:** Medium  
**Language:** EN

## Transcription

This is the transcribed text from your audio file...
```

## File Size Configuration

The default file size limit is 200MB, but you can increase it:

**Option 1: Configuration File**
Create `.streamlit/config.toml` in your project root:
```toml
[server]
maxUploadSize = 1000  # 1GB limit
```

**Option 2: Command Line**
```bash
streamlit run app_name.py --server.maxUploadSize 1000
```

**Option 3: Environment Variable**
```bash
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1000
streamlit run app_name.py
```

## Troubleshooting

- **FFmpeg Error**: Make sure FFmpeg is installed on your system
- **Memory Issues**: Try using a smaller model (tiny/base) for large files
- **Slow Processing**: Large models take more time but provide better accuracy
- **Copy Issues**: Ensure your browser allows clipboard access
- **File Size Error**: Increase the upload limit using the methods above

## Requirements

- Python 3.8+
- FFmpeg (for audio processing)
- Sufficient RAM for model loading (varies by model size)

## Notes

- First run will download the selected Whisper model (this may take a few minutes)
- Models are cached after first download for faster subsequent use
- Transcription quality depends on audio quality and model selection
