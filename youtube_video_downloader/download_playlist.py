#!/usr/bin/env python3
"""
YouTube Playlist Downloader

Download all videos or audio from a YouTube playlist using yt-dlp.
"""

import yt_dlp
import sys
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.table import Table
from rich import box


# Initialize Rich console
console = Console()

# Global progress tracking
progress = None
task_id = None
current_file = None


def progress_hook(d):
    """Hook function to track download progress with Rich."""
    global progress, task_id, current_file
    
    if d['status'] == 'downloading':
        if progress is None:
            return
        
        # Extract filename from info if available
        info = d.get('info_dict', {})
        title = info.get('title', 'Unknown')
        playlist_index = info.get('playlist_index', '?')
        
        # Update progress bar
        if task_id is not None:
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                # Truncate long titles
                display_title = title[:50] + "..." if len(title) > 50 else title
                progress.update(
                    task_id,
                    completed=downloaded,
                    total=total,
                    description=f"[cyan]#{playlist_index} Downloading:[/cyan] [yellow]{display_title}[/yellow]"
                )
    elif d['status'] == 'finished':
        if progress is not None and task_id is not None:
            info = d.get('info_dict', {})
            title = info.get('title', 'Unknown')
            playlist_index = info.get('playlist_index', '?')
            filename = os.path.basename(d.get('filename', ''))
            
            # Truncate long titles
            display_title = title[:50] + "..." if len(title) > 50 else title
            console.print(f"[green]✓[/green] [bold]#{playlist_index}[/bold] [dim]Completed:[/dim] [cyan]{display_title}[/cyan]")
    elif d['status'] == 'error':
        console.print(f"[red]✗[/red] [bold red]Error downloading:[/bold red] {d.get('filename', 'Unknown file')}")


def download_playlist(
    playlist_url: str,
    audio_only: bool = False,
    output_path: str = "./downloads",
    audio_format: str = "mp3",
    audio_quality: str = "192",
    video_quality: str = "best",
    subtitles: bool = False,
    subtitle_lang: str = "en"
):
    """
    Download all videos from a YouTube playlist.
    
    Args:
        playlist_url: URL of the YouTube playlist
        audio_only: If True, download only audio
        output_path: Directory to save downloads
        audio_format: Audio format (mp3, m4a, opus, etc.)
        audio_quality: Audio quality/bitrate (e.g., "192", "320K")
        video_quality: Video quality (e.g., "best", "worst", "720p")
        subtitles: Whether to download subtitles
        subtitle_lang: Subtitle language code (e.g., "en", "pt")
    """
    global progress, task_id, current_file
    
    # Display header
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]YouTube Playlist Downloader[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    # Create output directory if it doesn't exist
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Display configuration table
    config_table = Table(title="[bold]Download Configuration[/bold]", box=box.ROUNDED, show_header=False)
    config_table.add_row("[bold cyan]Playlist URL:[/bold cyan]", playlist_url)
    config_table.add_row("[bold cyan]Output Directory:[/bold cyan]", f"[green]{os.path.abspath(output_path)}[/green]")
    config_table.add_row("[bold cyan]Mode:[/bold cyan]", 
                        f"[yellow]Audio Only ({audio_format.upper()})[/yellow]" if audio_only 
                        else f"[blue]Video ({video_quality})[/blue]")
    
    if audio_only:
        config_table.add_row("[bold cyan]Audio Quality:[/bold cyan]", f"[yellow]{audio_quality}[/yellow]")
    
    if subtitles:
        config_table.add_row("[bold cyan]Subtitles:[/bold cyan]", f"[magenta]Yes ({subtitle_lang})[/magenta]")
    
    console.print(config_table)
    console.print()
    
    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
        'quiet': True,  # We'll use our own progress display
        'no_warnings': False,
        'progress_hooks': [progress_hook],
    }
    
    if audio_only:
        # Audio-only download configuration
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }],
        })
        console.print(f"[yellow]📻[/yellow] [bold]Mode:[/bold] Downloading audio only as [cyan]{audio_format.upper()}[/cyan] format")
    else:
        # Video download configuration
        if video_quality != "best":
            ydl_opts['format'] = f'best[height<={video_quality}]'
        else:
            ydl_opts['format'] = 'best'
        console.print(f"[blue]🎥[/blue] [bold]Mode:[/bold] Downloading videos (quality: [cyan]{video_quality}[/cyan])")
    
    # Subtitle configuration
    if subtitles:
        ydl_opts.update({
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [subtitle_lang],
        })
        console.print(f"[magenta]📝[/magenta] [bold]Subtitles:[/bold] Will be downloaded in [cyan]{subtitle_lang}[/cyan]")
    
    console.print()
    
    # Download the playlist
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress_bar:
            progress = progress_bar
            task_id = progress_bar.add_task("[cyan]Initializing...", total=100)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get playlist info first
                progress_bar.update(task_id, description="[cyan]🔍 Fetching playlist information...")
                console.print("[dim]🔍 Fetching playlist information...[/dim]")
                try:
                    info = ydl.extract_info(playlist_url, download=False)
                    playlist_title = info.get('title', 'Unknown Playlist')
                    video_count = len(info.get('entries', []))
                    playlist_uploader = info.get('uploader', 'Unknown')
                    
                    # Display playlist info in a nice format
                    info_panel = Panel(
                        f"[bold cyan]{playlist_title}[/bold cyan]\n"
                        f"[dim]Uploader:[/dim] {playlist_uploader}\n"
                        f"[dim]Videos:[/dim] [bold green]{video_count}[/bold green]",
                        border_style="cyan",
                        title="[bold cyan]Playlist Info[/bold cyan]"
                    )
                    console.print(info_panel)
                    console.print()
                    
                    # Update progress bar for each video
                    progress_bar.update(task_id, total=video_count * 100)
                    
                except Exception as e:
                    console.print(f"[yellow]⚠[/yellow] [bold yellow]Warning:[/bold yellow] Could not fetch playlist info: [dim]{e}[/dim]")
                    console.print("[dim]Proceeding with download anyway...[/dim]\n")
                
                # Start downloading
                progress_bar.update(task_id, description="[green]⬇️ Starting downloads...")
                console.print("[bold green]⬇️ Starting download...[/bold green]\n")
                ydl.download([playlist_url])
                
                progress_bar.update(task_id, completed=progress_bar.tasks[task_id].total, description="[green]✓ All downloads completed!")
        
        # Success message with summary
        console.print()
        
        # Count downloaded files
        downloaded_files = list(output_dir.glob("*"))
        file_count = len([f for f in downloaded_files if f.is_file()])
        
        success_content = (
            f"[bold green]✓ Download completed successfully![/bold green]\n\n"
            f"[cyan]📁 Files downloaded:[/cyan] [bold]{file_count}[/bold]\n"
            f"[cyan]📂 Location:[/cyan] [green]{os.path.abspath(output_path)}[/green]"
        )
        
        console.print(Panel(
            success_content,
            border_style="green",
            title="[bold green]✓ Success[/bold green]"
        ))
        
    except yt_dlp.utils.DownloadError as e:
        console.print()
        console.print(Panel(
            f"[bold red]Download Error[/bold red]\n\n[red]{str(e)}[/red]",
            border_style="red",
            title="[bold red]Error[/bold red]"
        ))
        sys.exit(1)
    except KeyboardInterrupt:
        console.print()
        console.print(Panel(
            "[bold yellow]Download interrupted by user[/bold yellow]",
            border_style="yellow",
            title="[bold yellow]Interrupted[/bold yellow]"
        ))
        sys.exit(1)
    except Exception as e:
        console.print()
        console.print(Panel(
            f"[bold red]Unexpected Error[/bold red]\n\n[red]{str(e)}[/red]",
            border_style="red",
            title="[bold red]Error[/bold red]"
        ))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Download all videos or audio from a YouTube playlist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all videos
  python download_playlist.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
  
  # Download only audio as MP3
  python download_playlist.py "PLAYLIST_URL" --audio-only
  
  # Download audio with custom quality
  python download_playlist.py "PLAYLIST_URL" --audio-only --audio-quality 320K
  
  # Download videos with subtitles
  python download_playlist.py "PLAYLIST_URL" --subtitles
  
  # Download to custom directory
  python download_playlist.py "PLAYLIST_URL" --output ./my_downloads
        """
    )
    
    parser.add_argument(
        'playlist_url',
        help='URL of the YouTube playlist to download'
    )
    
    parser.add_argument(
        '--audio-only',
        action='store_true',
        help='Download only audio (requires ffmpeg)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./downloads',
        help='Output directory for downloads (default: ./downloads)'
    )
    
    parser.add_argument(
        '--audio-format',
        default='mp3',
        choices=['mp3', 'm4a', 'opus', 'wav', 'flac'],
        help='Audio format when using --audio-only (default: mp3)'
    )
    
    parser.add_argument(
        '--audio-quality',
        default='192',
        help='Audio quality/bitrate (default: 192, examples: 128, 192, 256, 320K)'
    )
    
    parser.add_argument(
        '--video-quality',
        default='best',
        help='Video quality (default: best, examples: 720p, 1080p, best, worst)'
    )
    
    parser.add_argument(
        '--subtitles',
        action='store_true',
        help='Download subtitles along with videos'
    )
    
    parser.add_argument(
        '--subtitle-lang',
        default='en',
        help='Subtitle language code (default: en)'
    )
    
    args = parser.parse_args()
    
    # Validate playlist URL
    if 'youtube.com' not in args.playlist_url and 'youtu.be' not in args.playlist_url:
        console.print("[yellow]⚠[/yellow] [bold yellow]Warning:[/bold yellow] The URL doesn't appear to be a YouTube URL.")
        response = console.input("[dim]Continue anyway? (y/n): [/dim]")
        if response.lower() != 'y':
            console.print("[red]Aborted.[/red]")
            sys.exit(0)
    
    download_playlist(
        playlist_url=args.playlist_url,
        audio_only=args.audio_only,
        output_path=args.output,
        audio_format=args.audio_format,
        audio_quality=args.audio_quality,
        video_quality=args.video_quality,
        subtitles=args.subtitles,
        subtitle_lang=args.subtitle_lang
    )


if __name__ == "__main__":
    main()

