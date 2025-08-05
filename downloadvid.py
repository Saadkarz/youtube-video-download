# Install required packages:
# pip install pytube yt-dlp

from pytube import YouTube
import yt_dlp
import os

def download_video_pytube(url, output_path='.'):
    """Try downloading with pytube first"""
    try:
        print("Trying with pytube...")
        yt = YouTube(url)
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Views: {yt.views:,}")

        # Select the highest resolution progressive stream (includes audio)
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        
        if not stream:
            # If no progressive stream, try adaptive (video only)
            stream = yt.streams.filter(adaptive=True, file_extension='mp4').get_highest_resolution()
            print("Note: Downloaded video-only stream (no audio)")

        print("Downloading...")
        stream.download(output_path=output_path)
        print(f"Download complete! Saved to: {output_path}")
        return True

    except Exception as e:
        print(f"Pytube failed: {e}")
        return False

def download_video_ytdlp(url, output_path='.'):
    """Fallback to yt-dlp which is more reliable"""
    try:
        print("Trying with yt-dlp...")
        
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best available
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Uploader: {info.get('uploader', 'Unknown')}")
            print(f"Duration: {info.get('duration', 'Unknown')} seconds")
            
            # Download the video
            print("Downloading...")
            ydl.download([url])
            print(f"Download complete! Saved to: {output_path}")
            return True
            
    except Exception as e:
        print(f"yt-dlp failed: {e}")
        return False

def download_video(url, output_path='.'):
    """Main function that tries pytube first, then yt-dlp as fallback"""
    print(f"Attempting to download from: {url}")
    
    # Try pytube first
    if download_video_pytube(url, output_path):
        return
    
    print("\n" + "="*50)
    print("Pytube failed, trying yt-dlp as fallback...")
    print("="*50)
    
    # Fallback to yt-dlp
    if download_video_ytdlp(url, output_path):
        return
    
    print("\n❌ Both methods failed. Possible solutions:")
    print("1. Check if the URL is correct and video is public")
    print("2. Update packages: pip install --upgrade pytube yt-dlp")
    print("3. Try a different video URL")
    print("4. Check your internet connection")

if __name__ == '__main__':
    video_url = "https://youtu.be/hpszGl2cl_k?si=02HNQDc81V7273Ng"
    download_video(video_url)
