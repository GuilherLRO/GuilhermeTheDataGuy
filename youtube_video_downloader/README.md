# YouTube Playlist Downloader

A Python script to download all videos or audio from YouTube playlists using `yt-dlp`.

## Features

- ✅ Download all videos from a YouTube playlist
- ✅ Download only audio (MP3, M4A, Opus, WAV, FLAC)
- ✅ Customizable audio quality/bitrate
- ✅ Customizable video quality
- ✅ Optional subtitle downloads
- ✅ Custom output directory
- ✅ **Beautiful colored terminal output with Rich**
- ✅ **Real-time progress bars with download speed**
- ✅ **Detailed logging with multiple colors**
- ✅ Progress tracking and error handling

## Requirements

- Python 3.7+
- `yt-dlp` (installed via requirements.txt)
- `ffmpeg` (required for audio extraction)

### Installing ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
```bash
choco install ffmpeg
```

## Installation

### Using uv (Recommended)

1. Create a virtual environment and install dependencies:
```bash
uv venv
uv pip install -r requirements.txt
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### Using pip

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

**Download all videos from a playlist:**
```bash
python download_playlist.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

**Download only audio (MP3):**
```bash
python download_playlist.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --audio-only
```

### Advanced Options

**Download audio with custom quality:**
```bash
python download_playlist.py "PLAYLIST_URL" --audio-only --audio-quality 320K
```

**Download audio in different format:**
```bash
python download_playlist.py "PLAYLIST_URL" --audio-only --audio-format m4a
```

**Download videos with subtitles:**
```bash
python download_playlist.py "PLAYLIST_URL" --subtitles --subtitle-lang en
```

**Download to custom directory:**
```bash
python download_playlist.py "PLAYLIST_URL" --output ./my_downloads
```

**Download videos with specific quality:**
```bash
python download_playlist.py "PLAYLIST_URL" --video-quality 720p
```

**Combine options:**
```bash
python download_playlist.py "PLAYLIST_URL" --audio-only --audio-format mp3 --audio-quality 256 --output ./music
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `playlist_url` | YouTube playlist URL (required) | - |
| `--audio-only` | Download only audio | False |
| `--output`, `-o` | Output directory | `./downloads` |
| `--audio-format` | Audio format (mp3, m4a, opus, wav, flac) | `mp3` |
| `--audio-quality` | Audio quality/bitrate | `192` |
| `--video-quality` | Video quality | `best` |
| `--subtitles` | Download subtitles | False |
| `--subtitle-lang` | Subtitle language code | `en` |

## Examples

### Example 1: Download Music Playlist as MP3
```bash
python download_playlist.py "https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMH7P1WnP5Y4KQO1Qx" \
    --audio-only \
    --audio-quality 320K \
    --output ./music
```

### Example 2: Download Educational Videos with Subtitles
```bash
python download_playlist.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    --subtitles \
    --subtitle-lang en \
    --video-quality 720p \
    --output ./lectures
```

### Example 3: Download Podcast Audio
```bash
python download_playlist.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" \
    --audio-only \
    --audio-format m4a \
    --audio-quality 256 \
    --output ./podcasts
```

## Output Format

Files are saved with the format: `{playlist_index} - {title}.{ext}`

For example:
- `1 - Introduction to Python.mp4`
- `2 - Variables and Data Types.mp3`
- `3 - Functions and Classes.mp4`

## Troubleshooting

### Error: "ffmpeg not found"
Install ffmpeg using the instructions above. The script requires ffmpeg for audio extraction.

### Error: "Unable to download video"
- Check your internet connection
- Verify the playlist URL is correct
- Some videos may be region-restricted or private
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### Error: "No suitable format found"
- The requested quality may not be available
- Try using `--video-quality best` or `--audio-quality best`

## Notes

- The script respects YouTube's terms of service. Only download content you have permission to download.
- Download speeds depend on your internet connection and YouTube's servers.
- Large playlists may take significant time to download.
- Some videos may be unavailable due to regional restrictions or privacy settings.

## License

This script is provided as-is for educational and personal use.

