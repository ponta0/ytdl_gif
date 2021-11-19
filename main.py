from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import youtube_dl
import secrets
import ffmpeg
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/ytdl_gif/")
def ytdl_gif(video_id: str, ss: int, t: int):
    if (ss is None or t is None):
        return "Invalid Query"
    filename = secrets.token_hex(16) + ".mp4"
    ytdl_options = {
        "format": "bestvideo[ext=mp4][height<=240]",
        "outtmpl": f"static/{filename}"
    }
    youtube_dl.YoutubeDL(ytdl_options).download([video_id])
    stream = ffmpeg.input(f"static/{filename}", ss = ss, t = t)
    stream = ffmpeg.output(stream, f"static/{filename}.gif")
    ffmpeg.run(stream)
    os.remove(f"static/{filename}")
    return RedirectResponse(f"/static/{filename}.gif")