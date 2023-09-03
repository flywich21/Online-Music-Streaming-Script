import vlc
import subprocess
import sys
import os
import yt_dlp as ydl
import time
import threading
from colorama import init, Fore

global audio_playing
def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')
def format_time(seconds):
    # convert seconds to minutes and seconds
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

# specify the path to the directory containing libvlc.dll
try:
    VLC_DIRECTORY = "C:\\Program Files\\VideoLAN\\VLC"
    # add the VLC directory to the system's PATH environment variable
    os.environ["PATH"] += os.pathsep + VLC_DIRECTORY
except:
    print("Vlc's libvlc.dll not found error")
    exit(0)

def playback_thread(player, youtube_url):
    player.play()
    is_paused = False
    last_print_time = 0  # initialize the last time printed

    while True:
        # query the current playback time and duration
        current_time = player.get_time() / 1000  # convert milliseconds to seconds
        total_time = player.get_length() / 1000  # convert milliseconds to seconds

        # check if a second has passed since the last print
        current_print_time = int(current_time)
        if current_print_time != last_print_time:
            # format and print the current playback time and total duration in "mm:ss" format
            current_time_str = format_time(current_time)
            total_time_str = format_time(total_time)
            print(Fore.GREEN + f"Playing {current_time_str}/{total_time_str}", end="\r")
            last_print_time = current_print_time

        time.sleep(1)

def command_thread(player):
    global audio_playing
    while True:
        print(f"\nPress & enter {Fore.BLUE +'Pause'} | {Fore.GREEN +'Resume'} | {Fore.RED +'Stop'} | {Fore.GREEN +'Restart'} | {Fore.RED +'Quit'}")
        command = input(': ').strip().lower()
        if command in ['pause', '1']:
            if audio_playing:
                player.set_pause(1)
                print(Fore.GREEN + "Audio Paused")
                audio_playing = False  # Corrected assignment
            else:
                print(Fore.RED + "Audio is already Paused...")
        elif command in ['resume', '2']:
            if not audio_playing:
                player.set_pause(0)
                print(Fore.GREEN + "Audio Resumed")  # Resume playback
                audio_playing = True  # Corrected assignment
            else:
                print(Fore.RED + "Audio is already playing...")
        elif command in ['stop', 'q', 'quit', '3']:
            player.stop()
            print(Fore.RED + "Stopping...")
            time.sleep(2)  # stop playback
            sys.exit(0)
        elif command in ['restart', '4']:
            player.stop()
            print(Fore.GREEN + "Restarting...")
            time.sleep(2)
            clear()
            main()  # restart the main function
        elif command == "":
            print(Fore.RED +"Input Seems Empty")
        else:
            print(Fore.RED +"Command not recognized by the logic...")

def main():
    global audio_playing
    song_name = input(Fore.BLUE + "Music Name: ")
    print(Fore.GREEN + "\nSearching...")
    # create a VLC media player instance with high-quality audio output
    instance = vlc.Instance("--aout=waveout")

    # create a VLC media player
    player = instance.media_player_new()

    # Use subprocess to call yt-dlp with the --verbose flag and specify high-quality audio
    youtube_url = None
    try:
        process = subprocess.Popen(
            [
                'yt-dlp',
                '--verbose',
                '--skip-download',
                '--format', 'bestaudio/best',
                '--get-url',
                f'ytsearch:{song_name}'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            youtube_url = stdout.strip()
        else:
            print(Fore.RED + "Error:", stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install yt-dlp.")
        sys.exit(1)

    if youtube_url:
        # create a VLC Media object and set it to the audio URL
        media = instance.media_new(youtube_url)
        player.set_media(media)

        print(Fore.BLUE + f"\nPlaying from '{song_name}' in search")
        audio_playing = True
        # create separate threads for playback and command input
        playback_thread_instance = threading.Thread(target=playback_thread, args=(player, youtube_url))
        command_thread_instance = threading.Thread(target=command_thread, args=(player,))

        # sart both threads
        playback_thread_instance.start()
        command_thread_instance.start()

        # wait for both threads to finish
        playback_thread_instance.join()
        command_thread_instance.join()

if __name__ == "__main__":
    main()
