from requests import get, post
import re


def js_runner(js_string):
    data = get('https://onecompiler.com/api/getIdAndToken').json()

    token_title = data['id']
    token = data['token']
    js_content = js_string.replace('"', '"') + ';'
    js_translate_data = {
        'name': 'JavaScript',
        'title': token_title,
        'version': 'ES6',
        'mode': 'javascript',
        'description': None,
        'extension': 'js',
        'languageType': 'programming',
        'active': True,
        'properties': {
            'language': 'javascript',
            'docs': True,
            'tutorials': True,
            'cheatsheets': True,
            'filesEditable': True,
            'filesDeletable': True,
            'files': [{'name': 'index.js', 'content': js_content}],
            'newFileOptions': [
                {
                    'helpText': 'New JS file',
                    'name': 'script${i}.js',
                    'content': "/**\n *  In main file\n *  let script${i} = require('./script${i}');\n *  console.log(script${i}.sum(1, 2));\n */\n\nfunction sum(a, b) {\n    return a + b;\n}\n\nmodule.exports = { sum };",
                },
                {
                    'helpText': 'Add Dependencies',
                    'name': 'package.json',
                    'content': '{\n  "name": "main_app",\n  "version": "1.0.0",\n  "description": "",\n  "main": "HelloWorld.js",\n  "dependencies": {\n    "lodash": "^4.17.21"\n  }\n}',
                },
            ],
        },
        '_id': token_title,
        'user': None,
        'idToken': token,
        'visibility': 'public',
    }

    # post js data to js translator sever
    translated_js_from_js_runner = post(
        'https://onecompiler.com/api/code/exec', json=js_translate_data
    ).text
    return translated_js_from_js_runner


def snap_save(facebook_video_url):
    # snapsave server return encoded javascript code
    raw_result_contain_js = post(
        'https://snapsave.app/action.php',
        data={'url': facebook_video_url},
        headers={
            'origin': 'https://snapsave.app',
            'referer': 'https://snapsave.app/',
        },
    ).text

    try:
        the_js_result = re.search(
            r'javascript\">(.*?)<\/script>', raw_result_contain_js
        ).group(1)
    except Exception:
        the_js_result = raw_result_contain_js

    # translate the encoded javascript code to readable code using https://onecompiler.com/javascript/
    translated_js = js_runner(the_js_result)

    # then get download url (higher quality video)
    url_result = re.search(r'href=\\\\\\\"(http.*?)\\\\\\\"', translated_js).group(1)

    return url_result

