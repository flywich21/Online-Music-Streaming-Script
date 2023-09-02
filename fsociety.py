import yt_dlp as ydl
import os
import time
from audio_controller import AudioController

bot = 'Dara- '

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_audio_url(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'default_search': 'auto',
    }

    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
        info_dict = ydl_instance.extract_info(query, download=False)
        if 'entries' in info_dict:
            video_url = info_dict['entries'][0]['url']
        else:
            video_url = info_dict['url']

    return video_url

def main():
    clear_terminal()
    user_query = input(f"{bot}Enter your search query: ")

    # Check for a number between 200 and 300 in the query
    volume_level = 0.5  # Default volume

    audio_url = get_audio_url(user_query)
    if audio_url:
        print(f"{bot}Searching for '{user_query}'")

        looping = False
        controller = None
        is_playing = False

        while True:
            print(f"{bot}Playing from '{user_query}' in search")

            if not is_playing and controller is None:
                controller = AudioController(audio_url, volume_level)
                controller.play()
                is_playing = True

            if looping and not is_playing:
                controller.play()  # Restart playback for looping
                is_playing = True

            command = input(f"{bot}Enter 'loop' to toggle loop, 'change' to play a new song, or 'stop' to stop: ")
            if command == 'loop':
                looping = not looping
                if looping:
                    print("Looping enabled")
                else:
                    print("Looping disabled")
            elif command == 'change':
                looping = False
                controller.stop()  # Stop the current playback
                controller = None  # Reset the controller
                is_playing = False  # Reset playback status
                user_query = input(f"{bot}Enter a new search query: ")
                audio_url = get_audio_url(user_query)
                if audio_url:
                    print(f"{bot}Searching for '{user_query}'")
            elif command == 'stop':
                looping = False
                if controller:
                    controller.stop()  # Stop the current playback
                controller = None  # Reset the controller
                is_playing = False  # Reset playback status
                break
            else:
                print(f"{bot}Invalid command. Please enter 'loop', 'change', or 'stop'.")

            time.sleep(1)

if __name__ == "__main__":
    main()
