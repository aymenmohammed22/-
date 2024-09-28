from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'C:/path/to/downloaded/video.%(ext)s'  # عدل المسار هنا حيث تريد حفظ الفيديو
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return jsonify({'message': 'Video downloaded successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
