import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("ffmpeg is available.")
    except FileNotFoundError:
        raise RuntimeError("ffmpeg was not found but is required.")

# Add this at the top of your script
check_ffmpeg()