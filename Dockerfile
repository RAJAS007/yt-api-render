# Use the latest Python 3.13
FROM python:3.13-slim

# Install FFmpeg and Git (Required for yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg git

# Set up the app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run the server on port 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
