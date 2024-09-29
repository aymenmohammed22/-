from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    # الحصول على البيانات من الطلب
    data = request.get_json()
    video_url = data.get('url')

    # التحقق من وجود عنوان URL
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # إعداد خيارات yt-dlp لتحليل الفيديو بدون تحميله
    ydl_opts = {
        'format': 'best',  # استخراج أفضل جودة متاحة
        'noplaylist': True, # منع تحميل قوائم التشغيل
        'skip_download': True # عدم تحميل الفيديو
    }

    try:
        # استخدم yt-dlp لتحليل المعلومات الخاصة بالفيديو
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # إعداد بيانات الفيديو للرد
            video_data = {
                'title': info.get('title'),
                'url': info.get('url'),  # الرابط الأصلي للفيديو
                'ext': info.get('ext'),   # امتداد الملف
                'duration': info.get('duration'),  # مدة الفيديو
                'thumbnail': info.get('thumbnail'),  # رابط الصورة المصغرة
                'formats': []  # قائمة تنسيقات الفيديو
            }

            # استخراج روابط التنزيل المختلفة
            for format in info['formats']:
                video_data['formats'].append({
                    'format_id': format.get('format_id'),  # معرف التنسيق
                    'format': format.get('format'),  # اسم التنسيق
                    'url': format.get('url'),  # رابط التنسيق
                    'resolution': format.get('resolution'),  # دقة الفيديو
                    'filesize': format.get('filesize')  # حجم الملف
                })

        # إرسال المعلومات إلى التطبيق
        return jsonify(video_data), 200

    except yt_dlp.utils.ExtractorError as e:
        return jsonify({'error': f'Extractor Error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
