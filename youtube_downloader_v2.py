import yt_dlp
import os

def show_info(url):
    """Fetch metadata and show title, uploader, duration, and size estimates."""
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"\n📹 Title: {info.get('title', 'Unknown')}")
        print(f"👤 Uploader: {info.get('uploader', 'Unknown')}")
        print(f"⏱️ Duration: {int(info.get('duration', 0) / 60)} mins {int(info.get('duration', 0) % 60)} secs")
        return info

def download_youtube(youtube_url):
    # Show video details
    info = show_info(youtube_url)
    choice = input("\nDo you want to download as (a)udio or (v)ideo? ").strip().lower()

    # === AUDIO ===
    if choice.startswith("a"):
        print("\n🎧 Choose Audio Quality:")
        print("1. 128 kbps (smaller size)")
        print("2. 192 kbps (standard HQ)")
        print("3. 256 kbps (very HQ)")
        print("4. 320 kbps (max HQ)\n")

        audio_choice = input("Enter your choice (1-4): ").strip()
        audio_quality = {"1": "128", "2": "192", "3": "256", "4": "320"}.get(audio_choice, "192")

        est_size_mb = int(info.get('filesize_approx', 5_000_000) / 1024 / 1024 / 192 * int(audio_quality))
        print(f"📦 Estimated File Size: ~{est_size_mb:.1f} MB\n")

        folder = "audio"
        os.makedirs(folder, exist_ok=True)
        output_template = os.path.join(folder, "%(title)s.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
            }],
            'quiet': False,
        }

        print(f"\n🎧 Downloading audio at {audio_quality} kbps ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print("\n✅ Audio download complete!")

    # === VIDEO ===
    elif choice.startswith("v"):
        print("\n🎥 Choose Video Quality:")
        print("1. 360p (small)")
        print("2. 480p (medium)")
        print("3. 720p (HD)")
        print("4. 1080p (Full HD)")
        print("5. best (highest available)\n")

        video_choice = input("Enter your choice (1-5): ").strip()
        quality_map = {
            "1": "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "2": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "3": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "4": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "5": "bestvideo+bestaudio/best"
        }
        video_quality = quality_map.get(video_choice, "bestvideo+bestaudio/best")

        est_size = info.get('filesize_approx', 0)
        if est_size:
            print(f"📦 Estimated File Size: ~{est_size / (1024 * 1024):.1f} MB\n")
        else:
            print("📦 Estimated File Size: unknown (depends on chosen resolution)\n")

        folder = "videos"
        os.makedirs(folder, exist_ok=True)
        output_template = os.path.join(folder, "%(title)s.%(ext)s")

        ydl_opts = {
            'format': video_quality,
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'quiet': False,
        }

        print(f"\n🎥 Downloading video at selected quality ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print("\n✅ Video download complete!")

    else:
        print("❌ Invalid choice. Please enter 'a' for audio or 'v' for video.")


if __name__ == "__main__":
    youtube_url = input("Enter YouTube link: ").strip()
    download_youtube(youtube_url)

