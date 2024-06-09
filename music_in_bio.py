from spotipy.oauth2 import SpotifyOAuth
from telethon import TelegramClient, sync
from telethon.tl.functions.account import UpdateProfileRequest

import spotipy
import time

# Spotify credentials
SPOTIPY_CLIENT_ID = 'CLIENT ID'
SPOTIPY_CLIENT_SECRET = 'CLIENT SECRET'
SPOTIPY_REDIRECT_URI = 'URI'

#Telegram credentials
API_ID = 'API_ID'
API_HASH = 'API HASH'
PHONE_NUMBER = 'TG NUMBER'

client = TelegramClient('session_name', API_ID, API_HASH)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-read-currently-playing"))

def update_telegram_bio(track_name):
    client(UpdateProfileRequest(about=f'🎧: {track_name}'))

def main():
    client.start(phone=PHONE_NUMBER)
    print("Telegram connected")
    current_track = None
    while True:
        try:
            # Get current track from Spotify
            now_playing = sp.currently_playing()
            if now_playing is not None and now_playing['is_playing']:
                track_name = now_playing['item']['name']
                artist_name = now_playing['item']['artists'][0]['name']
                new_track = f'{track_name} - {artist_name}'

                if new_track != current_track:
                    current_track = new_track
                    print("Update telegram bio, current track:", current_track)
                    update_telegram_bio(current_track)
            else:
                print("Nothing's playing.")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(30)

if __name__ == "__main__":
    with client:
        main()
