import yt_dlp

url = 'https://www.youtube.com/watch?v=kClwJxgmrgk&list=RDkClwJxgmrgk&start_radio=1'

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
