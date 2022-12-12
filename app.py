from flask import Flask, request, render_template

# Include the pytube library
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
  # Get the video URL from the form submission
  video_url = request.form['video-url']

  # Get the YouTube video
  yt = YouTube(video_url)

  # Get the audio stream
  audio_stream = yt.streams.filter(only_audio=True).first()

  # Set the HTTP headers for the download
  headers = {
    'Content-Disposition': 'attachment; filename="{}.mp3"'.format(yt.title),
    'Content-Type': 'audio/mpeg'
  }

  # Download the audio to a temporary file
  temp_file = audio_stream.download()

  # Open the temporary file and return its contents
  with open(temp_file, 'rb') as f:
    return f.read(), 200, headers

if __name__ == '__main__':
  app.run()
