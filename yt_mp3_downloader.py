import yt_dlp

url = 'https://www.youtube.com/watch?v=-bVZQNEIAVs&t=4599s'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',  # kbps, use '320' for highest quality
    }],
}

url = input("enter youtube link...")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
