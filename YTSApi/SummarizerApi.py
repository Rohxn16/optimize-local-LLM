from flask import Flask, request, jsonify
from Summarizer import OptimizeServices
from Summarizer import *

app = Flask(__name__)
service_context = OptimizeServices()


@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No video_id provided'})
    try:
        summary = service_context.get_transcript_summary(url)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)})    

if __name__ == '__main__':
    app.run(debug=True)
