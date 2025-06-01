from flask import Flask, request as req
from snapsave_downloader import snap_save
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    try:
        data = req.args
        facebook_video_url = data['url']
        result = snap_save(facebook_video_url)
        return f"""
        <video width="320" height="240" controls>
          <source src="{result}" type="video/mp4">
          <source src="{result}" type="video/ogg">
        Your browser does not support the video tag.
        </video>
        """

        return result
        if result:
            ret_data = {
                'success': True,
                'result': result,
                'message': 'Unofficial SnapSave API by Karjok Pangesty',
            }
        else:
            ret_data = {
                'success': False,
                'result': None,
                'message': 'Invalid URL or video is private',
            }
    except Exception:
        ret_data = {'success': False, 'result': None, 'message': 'URL params required'}
    return ret_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True)

