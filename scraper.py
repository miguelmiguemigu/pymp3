import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

def download_video(video_url, output_path, format):
    if format == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }
    else:
        print(f"Unsupported format: {format}")
        return

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print(f"Downloaded and converted: {video_url}")
    except DownloadError as e:
        print(f"Error downloading {video_url}: {str(e)}")

def download_playlist(playlist_url, output_path, format):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_dict = ydl.extract_info(playlist_url, download=False)

        print(f'Downloading playlist: {playlist_dict["title"]}')

        for video in playlist_dict['entries']:
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            download_video(video_url, output_path, format)

playlist_url = input("Enter the playlist URL: ")
output_path = input("Enter the output path, in the format 'C:/path/to/folder': ")
format = input("Enter the format (mp3 or mp4): ").lower()

download_playlist(playlist_url, output_path, format)