import whisper
import os
from pathlib import Path
from datetime import timedelta

def format_timestamp(seconds):
    """Format seconds to [HH:MM:SS.mmm] format"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - total_seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def get_numeric_part(filename):
    """Extract numeric part from filename for sorting"""
    # Remove .ogg extension and convert to int
    return int(filename.replace('.ogg', ''))

def main():
    # Load Whisper model (medium complexity)
    print("Loading Whisper model 'medium'...")
    model = whisper.load_model("medium")
    print("Model loaded successfully.\n")
    
    # Get all .ogg files from audi_tg directory
    audi_tg_dir = Path("audi_tg")
    if not audi_tg_dir.exists():
        print(f"Error: Directory '{audi_tg_dir}' not found!")
        return
    
    ogg_files = list(audi_tg_dir.glob("*.ogg"))
    if not ogg_files:
        print(f"No .ogg files found in '{audi_tg_dir}'!")
        return
    
    # Sort files numerically by filename
    ogg_files.sort(key=lambda x: get_numeric_part(x.name))
    
    print(f"Found {len(ogg_files)} audio files to transcribe:")
    for f in ogg_files:
        print(f"  - {f.name}")
    print()
    
    # Store all transcriptions
    all_transcriptions = []
    
    # Transcribe each file
    for idx, audio_file in enumerate(ogg_files, 1):
        print(f"[{idx}/{len(ogg_files)}] Transcribing {audio_file.name}...")
        
        try:
            # Transcribe with verbose output
            result = model.transcribe(str(audio_file), verbose=True)
            
            # Extract segments with timestamps
            segments = result.get("segments", [])
            
            # Add file header
            all_transcriptions.append(f"\n{'='*80}\n")
            all_transcriptions.append(f"File: {audio_file.name}\n")
            all_transcriptions.append(f"{'='*80}\n\n")
            
            # Add each segment with timestamps
            for segment in segments:
                start_time = segment.get("start", 0)
                end_time = segment.get("end", 0)
                text = segment.get("text", "").strip()
                
                # Format timestamps
                start_formatted = format_timestamp(start_time)
                end_formatted = format_timestamp(end_time)
                
                # Add to transcription
                all_transcriptions.append(f"[{start_formatted} --> {end_formatted}] {text}\n")
            
            print(f"✓ Completed {audio_file.name}\n")
            
        except Exception as e:
            print(f"✗ Error transcribing {audio_file.name}: {str(e)}\n")
            all_transcriptions.append(f"\n{'='*80}\n")
            all_transcriptions.append(f"File: {audio_file.name} - ERROR: {str(e)}\n")
            all_transcriptions.append(f"{'='*80}\n\n")
    
    # Combine all transcriptions
    output_text = "".join(all_transcriptions)
    
    # Save to file
    output_file = "audi_tg_transcription.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)
    
    print(f"\n{'='*80}")
    print(f"Transcription complete!")
    print(f"Output saved to: {output_file}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

