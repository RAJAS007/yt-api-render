# Use Python 3.9
FROM python:3.9-slim

# Install FFmpeg AND Git (Git is required to install the latest yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg git

# Set up the app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run the server on port 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
