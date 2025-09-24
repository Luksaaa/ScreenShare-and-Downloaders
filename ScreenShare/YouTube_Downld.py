import os
from yt_dlp import YoutubeDL

def get_youtube_playlist_items(url):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'dump_single_json': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                return [entry['url'] for entry in info['entries']], [entry['title'] for entry in info['entries']]
            else:
                return [url], [info.get('title', 'Nepoznata pjesma')]
    except Exception as e:
        print(f"❌ Greška pri dohvaćanju informacija: {e}")
        return [url], ['Nepoznata pjesma']

def main():
    print("=== YouTube WAV Downloader ===")
    print("1. Pjesma")
    print("2. Playlista")
    choice = input("Choose (1 or 2) --> ").strip()

    url = input("YouTube URL  --> ").strip()
    save_path = input("Folder to save (npr. C:/User/Desktop) --> ").strip()

    if not save_path.endswith(("\\", "/")):
        save_path += "/"

    ffmpeg_path = "C:/ffmpeg"

    output_template = os.path.join(save_path, "%(title)s.%(ext)s")

    is_single = choice == '1'
    urls, titles = get_youtube_playlist_items(url) if not is_single else ([url], [''])

    if not is_single:
        print(f"\n📃 Playlista sadrži {len(urls)} pjesama.\n")

    print(f"✅ Pripremljeno {len(urls)} pjesama za skidanje.\n")

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '1411',
        }],
        'noplaylist': is_single,
        'quiet': False,
        'ignoreerrors': True
    }

    print("🎵 Downloading, please wait...\n")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            for idx, link in enumerate(urls, start=1):
                try:
                    title_display = titles[idx - 1] if idx - 1 < len(titles) else link
                    print(f"🔸 ({idx}/{len(urls)}) Preuzimam: {title_display}")
                    ydl.download([link])
                except Exception as e:
                    print(f"⚠️ Preskačem: {link} zbog greške: {e}")
        print("\n✅ Download complete! (Unavailable videos were skipped.)")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    main()
