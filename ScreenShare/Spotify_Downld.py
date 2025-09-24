import os
from yt_dlp import YoutubeDL
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = '8deb872e9f184353ab3a68517d455c4b'
SPOTIFY_CLIENT_SECRET = '6406a3ee9b9649f19dc2fb84b8a39abe'

def get_spotify_tracks(url, is_single):
    try:
        sp = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

        if is_single:
            track = sp.track(url)
            return [f"{track['name']} {track['artists'][0]['name']}"]
        else:
            tracks = []
            offset = 0
            limit = 100

            while True:
                results = sp.playlist_items(url, offset=offset, limit=limit)
                items = results['items']
                if not items:
                    break
                for item in items:
                    track = item['track']
                    if track:
                        tracks.append(f"{track['name']} {track['artists'][0]['name']}")
                offset += limit

            return tracks
    except Exception as e:
        print(f"\n❌ Greška pri dohvaćanju podataka sa Spotify-a: {e}")
        return []

def main():
    print("=== Spotify WAV Downloader ===")
    print("1. Pjesma")
    print("2. Playlista")
    choice = input("Odaberi (1 ili 2) --> ").strip()

    spotify_url = input("Spotify URL  --> ").strip()
    save_path = input("Folder za spremanje (npr. C:/User/Desktop) --> ").strip()

    if not save_path.endswith(("\\", "/")):
        save_path += "/"

    ffmpeg_path = "C:/ffmpeg"

    output_template = os.path.join(save_path, "%(title)s.%(ext)s")

    is_single = (choice == '1')
    
    print("\n🔍 Dohvaćam podatke sa Spotify-a...\n")
    track_list = get_spotify_tracks(spotify_url, is_single)

    if not track_list:
        print("⚠️ Nema pjesama za preuzimanje.")
        return

    print(f"✅ Pripremljeno {len(track_list)} pjesama za skidanje.\n")

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

    print("🎵 Skidanje u tijeku, pričekaj...\n")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            for idx, track in enumerate(track_list, start=1):
                try:
                    print(f"🔸 ({idx}/{len(track_list)}) Preuzimam: {track}")
                    ydl.download([f"ytsearch:{track}"])
                except Exception as e:
                    print(f"⚠️ Preskačem: {track} zbog greške: {e}")
        print("\n✅ Preuzimanje završeno! (Nedostupni videi su preskočeni.)")
    except Exception as e:
        print(f"\n❌ Došlo je do pogreške: {e}")

if __name__ == "__main__":
    main()
