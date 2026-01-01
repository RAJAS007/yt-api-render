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
        # These options make the request look like a real mobile user
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best' if type == "video" else 'bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            # Use the Android client to bypass age-gates and some bot checks
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['configs', 'js'],
                }
            },
            # Spoof User-Agent to look like a standard browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
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
        # If this fails, the only remaining option is using cookies
        raise HTTPException(status_code=500, detail=f"YouTube Blocked the Request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
