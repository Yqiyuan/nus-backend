from __future__ import print_function
from flask import Response, Flask, request, send_file
from werkzeug.utils import secure_filename
from spoonacular.rest import ApiException
from pprint import pprint
from operate import db
import os
import json
import spoonacular
import requests
import pymysql
import base64
from PIL import Image
import io
import matplotlib.pyplot as plt
import uuid
from pathlib import Path


app = Flask(__name__)

save_path = Path('D:/upload/images/')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    path = save_path / filename
    return send_file(path, as_attachment=True)

@app.route('/upload', methods=['POST'])
def register():
    # f = request.files['file']
    f_base64 = request.form['file']
    imgdata = base64.b64decode(f_base64)
    img = Image.open(io.BytesIO(imgdata))
    f = img
    filename = str(uuid.uuid4()) + '.jpg'
    save_path.mkdir(exist_ok=True, parents=True)
    f.save(save_path / filename)
    print((save_path / filename).absolute())
    u = request.form['user_id']
    # print(request.form)

    basepath = os.path.dirname(__file__)  # 当前文件所在路径

    configuration = spoonacular.Configuration()
    # Configure API key authorization: apiKeyScheme
    configuration.api_key['apiKey'] = 'cf2b2f60e4f64dcfaf2ea8c7a1b9f2e1'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['apiKey'] = 'Bearer'

    # create an instance of the API class
    api_instance = spoonacular.DefaultApi(spoonacular.ApiClient(configuration))
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    # str | The URL of the image to be analyzed.
    image_url = 'http://'+ip+':5000'+'/download/'+filename
    #image_url = 'https://spoonacular.com/recipeImages/635350-240x150.jpg' # str | The URL of the image to be analyzed.

    try:
        # Image Analysis by URL
        api_response = api_instance.image_analysis_by_url(image_url)
        response = api_response
        bs = str(base64.b64encode(str(response).encode("utf-8")), "utf-8")
        sql = "INSERT INTO main (user_id, date, result) VALUES (" + u +', CURDATE(), "' + bs + '");'
        print(sql)
        db.execute_db(sql)

    except ApiException as e:
        response = "Exception when calling DefaultApi->image_analysis_by_url: %s\n" % e

    print(request.headers)
    # print(request.stream.read())
    # print(upload_path)
    print(image_url)
    return response

@app.route("/history", methods=['POST'])
def history():
    sql = "SELECT h_id FROM main WHERE user_id = " + request.form['user_id'] + " AND date = '" + request.form['date'] + "';"
    print(sql)
    res = json.dumps(db.select_db(sql))
    return res

@app.route("/search", methods=['POST'])
def search():
    sql = "SELECT result FROM main WHERE h_id = " + request.form['h_id']+ ";"
    print(sql)
    res = json.dumps(db.select_db(sql))
    return res

@app.route("/g/<path>")
def index(path):
    image = open(path, "rb").read()
    resp = Response(image, mimetype="image/jpeg")
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
