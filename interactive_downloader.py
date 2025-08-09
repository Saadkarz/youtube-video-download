# Interactive YouTube Video Downloader
# Install required packages: pip install pytube yt-dlp

from pytube import YouTube
import yt_dlp
import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print a nice header for the application"""
    print("=" * 60)
    print("🎥 YOUTUBE VIDEO DOWNLOADER 🎥")
    print("=" * 60)
    print("Dual-method downloader with automatic fallback")
    print("Supports all YouTube video formats and qualities")
    print("=" * 60)

def get_user_input():
    """Get YouTube URL and output path from user"""
    print("\n📎 Enter YouTube URL:")
    url = input("URL: ").strip()
    
    print("\n📁 Enter download folder (press Enter for current folder):")
    output_path = input("Path: ").strip()
    
    if not output_path:
        output_path = "."
    
    # Create directory if it doesn't exist
    if output_path != "." and not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
            print(f"✅ Created directory: {output_path}")
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            output_path = "."
    
    return url, output_path

def validate_url(url):
    """Basic YouTube URL validation"""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)

def download_video_pytube(url, output_path='.'):
    """Try downloading with pytube first"""
    try:
        print("\n🔄 Trying with pytube...")
        yt = YouTube(url)
        print(f"📺 Title: {yt.title}")
        print(f"👤 Author: {yt.author}")
        print(f"👁️ Views: {yt.views:,}")

        # Select the highest resolution progressive stream (includes audio)
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        
        if not stream:
            # If no progressive stream, try adaptive (video only)
            stream = yt.streams.filter(adaptive=True, file_extension='mp4').get_highest_resolution()
            print("⚠️ Note: Downloaded video-only stream (no audio)")

        print("⬇️ Downloading...")
        filename = stream.download(output_path=output_path)
        print(f"✅ Download complete! Saved as: {os.path.basename(filename)}")
        return True, filename

    except Exception as e:
        print(f"❌ Pytube failed: {e}")
        return False, None

def download_video_ytdlp(url, output_path='.'):
    """Fallback to yt-dlp which is more reliable"""
    try:
        print("\n🔄 Trying with yt-dlp...")
        
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best available
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"📺 Title: {info.get('title', 'Unknown')}")
            print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
            duration = info.get('duration', 'Unknown')
            if duration != 'Unknown':
                minutes, seconds = divmod(int(duration), 60)
                print(f"⏱️ Duration: {minutes}:{seconds:02d}")
            
            # Download the video
            print("⬇️ Downloading...")
            ydl.download([url])
            
            # Try to get the filename
            filename = ydl.prepare_filename(info)
            print(f"✅ Download complete! Saved as: {os.path.basename(filename)}")
            return True, filename
            
    except Exception as e:
        print(f"❌ yt-dlp failed: {e}")
        return False, None

def download_video(url, output_path='.'):
    """Main function that tries pytube first, then yt-dlp as fallback"""
    print(f"\n🎯 Attempting to download from: {url}")
    
    # Try pytube first
    success, filename = download_video_pytube(url, output_path)
    if success:
        return True, filename
    
    print("\n" + "="*50)
    print("🔄 Pytube failed, trying yt-dlp as fallback...")
    print("="*50)
    
    # Fallback to yt-dlp
    success, filename = download_video_ytdlp(url, output_path)
    if success:
        return True, filename
    
    print("\n❌ Both methods failed. Possible solutions:")
    print("1. Check if the URL is correct and video is public")
    print("2. Update packages: pip install --upgrade pytube yt-dlp")
    print("3. Try a different video URL")
    print("4. Check your internet connection")
    return False, None

def show_menu():
    """Show the main menu options"""
    print("\n" + "="*40)
    print("MENU OPTIONS:")
    print("1. Download a video")
    print("2. Batch download (multiple URLs)")
    print("3. Exit")
    print("="*40)

def batch_download():
    """Allow user to download multiple videos"""
    print("\n📋 BATCH DOWNLOAD MODE")
    print("Enter YouTube URLs one by one (empty line to finish):")
    
    urls = []
    while True:
        url = input(f"URL #{len(urls)+1}: ").strip()
        if not url:
            break
        if validate_url(url):
            urls.append(url)
            print(f"✅ Added: {url}")
        else:
            print("❌ Invalid YouTube URL, skipped")
    
    if not urls:
        print("❌ No valid URLs provided")
        return
    
    print(f"\n📁 Enter download folder for all videos (press Enter for current folder):")
    output_path = input("Path: ").strip() or "."
    
    # Create directory if needed
    if output_path != "." and not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
            print(f"✅ Created directory: {output_path}")
        except Exception as e:
            print(f"❌ Error creating directory: {e}")
            output_path = "."
    
    print(f"\n🚀 Starting batch download of {len(urls)} videos...")
    
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n{'='*20} VIDEO {i}/{len(urls)} {'='*20}")
        success, filename = download_video(url, output_path)
        if success:
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 BATCH DOWNLOAD SUMMARY:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Saved to: {os.path.abspath(output_path)}")

def main():
    """Main application loop"""
    while True:
        clear_screen()
        print_header()
        show_menu()
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Single video download
            print("\n🎬 SINGLE VIDEO DOWNLOAD")
            
            url, output_path = get_user_input()
            
            if not url:
                print("❌ No URL provided!")
                input("Press Enter to continue...")
                continue
            
            if not validate_url(url):
                print("❌ Invalid YouTube URL!")
                input("Press Enter to continue...")
                continue
            
            success, filename = download_video(url, output_path)
            
            if success:
                print(f"\n🎉 SUCCESS! Video saved to: {os.path.abspath(output_path)}")
            
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            # Batch download
            batch_download()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            # Exit
            print("\n👋 Thank you for using YouTube Video Downloader!")
            print("🌟 Star the project on GitHub: https://github.com/Saadkarz/youtube-video-download")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice! Please select 1, 2, or 3.")
            input("Press Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using YouTube Video Downloader!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
