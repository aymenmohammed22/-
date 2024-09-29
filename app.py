from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # إعداد خيارات yt-dlp لتحليل الفيديو بدون تحميله
    ydl_opts = {
        'format': 'best',  # استخراج أفضل جودة متاحة
        'noplaylist': True, # منع تحميل قوائم التشغيل
        'skip_download': True # عدم تحميل الفيديو
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج المعلومات الخاصة بالفيديو
            info = ydl.extract_info(video_url, download=False)

            # استخراج رابط التحميل
            video_data = {
                'title': info.get('title'),
                'url': info.get('url'),
                'ext': info.get('ext'),
                'duration': info.get('duration'),
                'thumbnail': info.get('thumbnail'),
                'formats': []
            }

            # استخراج روابط التنزيل المختلفة
            for format in info['formats']:
                video_data['formats'].append({
                    'format_id': format.get('format_id'),
                    'format': format.get('format'),
                    'url': format.get('url'),
                    'resolution': format.get('resolution'),
                    'filesize': format.get('filesize')
                })

        # إرسال المعلومات إلى التطبيق
        return jsonify(video_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
