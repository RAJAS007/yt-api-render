import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import yt_dlp
import uvicorn

app = FastAPI()

# Create downloads directory
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def cleanup_file(path: str):
    """Deletes file after download"""
    if os.path.exists(path):
        os.remove(path)

@app.get("/download")
async def download_video(url: str, type: str = "video", background_tasks: BackgroundTasks = None):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best' if type == "video" else 'bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        
        # Audio specific settings
        if type == "audio":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if type == "audio":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        background_tasks.add_task(cleanup_file, filename)
        
        return FileResponse(path=filename, filename=os.path.basename(filename))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
