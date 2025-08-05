# YouTube Video Downloader

A robust Python script to download YouTube videos with automatic fallback mechanisms for maximum reliability.

## Features

- **Dual Download Methods**: Uses both `pytube` and `yt-dlp` for maximum compatibility
- **Automatic Fallback**: If pytube fails, automatically tries yt-dlp
- **High Quality Downloads**: Prefers highest resolution with audio
- **Progress Tracking**: Real-time download progress display
- **Error Handling**: Comprehensive error handling with helpful troubleshooting tips
- **Format Selection**: Intelligent format selection (prefers MP4)
- **Video Information**: Displays title, uploader, duration, and views before downloading

## Requirements

### Software Dependencies

- **Python 3.6+**
- **pip** (Python package installer)

### Python Packages

The script requires two packages that will be installed automatically:

- `pytube` - Primary YouTube downloader
- `yt-dlp` - Backup downloader (more reliable, actively maintained)

## Installation

### 1. Clone or Download the Script

Save the `downloadvid.py` file to your desired directory.

### 2. Install Required Packages

```bash
pip install pytube yt-dlp
```

Or install with upgrade to get the latest versions:

```bash
pip install --upgrade pytube yt-dlp
```

## Usage

### Basic Usage

1. **Edit the script** to add your YouTube URL:
   ```python
   video_url = "https://www.youtube.com/watch?v=your_video_id"
   ```

2. **Run the script**:
   ```bash
   python downloadvid.py
   ```

### Programmatic Usage

You can also use the functions in your own code:

```python
from downloadvid import download_video

# Download to current directory
download_video("https://www.youtube.com/watch?v=example")

# Download to specific folder
download_video("https://www.youtube.com/watch?v=example", output_path="./downloads")
```

### Example Output

```
Attempting to download from: https://www.youtube.com/watch?v=example
Trying with pytube...
Pytube failed: HTTP Error 400: Bad Request

==================================================
Pytube failed, trying yt-dlp as fallback...
==================================================
Trying with yt-dlp...
Title: Example Video Title
Uploader: Channel Name
Duration: 1938 seconds
Downloading...
[download] 100% of 75.38MiB in 00:00:07 at 10.56MiB/s
Download complete! Saved to: .
```

## How It Works

### Download Strategy

1. **Primary Method (pytube)**:
   - Fast and lightweight
   - Good for most standard videos
   - May fail due to YouTube API changes

2. **Fallback Method (yt-dlp)**:
   - More robust and actively maintained
   - Handles YouTube updates better
   - Slightly slower but more reliable

### Quality Selection

- **Progressive streams**: Video + audio in single file (preferred)
- **Adaptive streams**: Video-only if progressive not available
- **Format preference**: MP4 → Best available format

## Configuration Options

### Custom Output Path

```python
download_video(url, output_path="./my_videos/")
```

### yt-dlp Options

You can modify the `ydl_opts` in the `download_video_ytdlp()` function:

```python
ydl_opts = {
    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    'format': 'best[ext=mp4]/best',
    'writesubtitles': True,        # Download subtitles
    'writeautomaticsub': True,     # Download auto-generated subtitles
    'subtitleslangs': ['en'],      # Subtitle languages
}
```

## Supported Formats

The script downloads videos in the following priority:

1. **MP4** (preferred - best compatibility)
2. **WebM** (fallback)
3. **Other formats** (as available)

## Troubleshooting

### Common Issues

#### "HTTP Error 400: Bad Request"
- This is normal for pytube - the script will automatically use yt-dlp
- Update packages: `pip install --upgrade pytube yt-dlp`

#### "No module named 'pytube'" or "No module named 'yt_dlp'"
```bash
pip install pytube yt-dlp
```

#### "Video not available"
- Check if the video is public and not region-blocked
- Verify the URL is correct
- Try a different video to test

#### Slow Download Speeds
- This is normal for some videos/regions
- yt-dlp may be slower but more reliable than pytube

#### Permission Errors
- Make sure you have write permissions in the output directory
- Try running as administrator (Windows) or with sudo (Linux/Mac)

### Update Packages

If downloads start failing frequently:

```bash
pip install --upgrade pytube yt-dlp
```

## Legal Considerations

- ⚠️ **Respect Copyright**: Only download videos you have permission to download
- ⚠️ **Personal Use**: Downloaded content should be for personal use only
- ⚠️ **Terms of Service**: Downloading may violate YouTube's Terms of Service
- ⚠️ **Creator Rights**: Consider supporting content creators through official channels

## Advanced Usage

### Batch Downloads

```python
urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://www.youtube.com/watch?v=video3"
]

for url in urls:
    download_video(url, output_path="./batch_downloads/")
```

### Integration with Video Splitter

This script works perfectly with the video splitter (`vid.py`):

1. Download video with this script
2. Copy the downloaded file to the splitter directory
3. Update `input_file` in `vid.py`
4. Run the splitter to create chunks

## Technical Details

### Dependencies

- **pytube**: YouTube downloader library
- **yt-dlp**: Fork of youtube-dl with additional features
- **os**: File path operations (built-in)

### Error Handling

The script includes comprehensive error handling:
- Network connection issues
- Invalid URLs
- Video availability problems
- Permission errors
- Package installation issues

## Changelog

### v2.0.0
- Added yt-dlp fallback mechanism
- Improved error handling
- Better format selection
- Progress tracking
- Comprehensive README

### v1.0.0
- Initial release with pytube
- Basic download functionality

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

## License

This project is open source and available under the MIT License.

---

**Note**: This tool is for educational and personal use only. Please respect copyright laws and YouTube's Terms of Service.
