# Use the latest Python 3.13
FROM python:3.13-slim

# Install system tools: FFmpeg (media) and Git (to download yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg git

# Set up the app
WORKDIR /app
COPY requirements.txt .

# Upgrade pip to the latest version first
RUN pip install --no-cache-dir --upgrade pip

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
