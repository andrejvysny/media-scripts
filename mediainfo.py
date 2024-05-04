import subprocess
import json

def get_media_info(file_path):
    try:
        # Use FFmpeg to extract media information in JSON format
        cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_entries", "stream=index,codec_type,codec_name:stream_tags=language,title", file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Parse the JSON output
        media_info = json.loads(result.stdout)

        # Extract and print audio and subtitle information
        audio_tracks = []
        subtitles = []

        for stream in media_info.get("streams", []):
            codec_type = stream.get("codec_type")
            if codec_type == "audio":
                track_info = {
                    "index": stream.get("index"),
                    "codec_name": stream.get("codec_name"),
                    "language": stream.get("tags", {}).get("language", "unknown"),
                    "title": stream.get("tags", {}).get("title", "N/A")
                }
                audio_tracks.append(track_info)
            elif codec_type == "subtitle":
                subtitle_info = {
                    "index": stream.get("index"),
                    "language": stream.get("tags", {}).get("language", "unknown"),
                    "title": stream.get("tags", {}).get("title", "N/A")
                }
                subtitles.append(subtitle_info)

        return {"audio_tracks": audio_tracks, "subtitles": subtitles}

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}

# Example usage
file_path = '/home/andrejvysny/Downloads/Mission Impossible - Dead Reckoning Part One (2023) [tmdbid-575264] - EN.mp4'
media_info = get_media_info(file_path)
print("Audio Tracks:", media_info["audio_tracks"])
print("Subtitles:", media_info["subtitles"])
