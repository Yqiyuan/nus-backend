from flask import Flask, request, send_file
from spoonacular.rest import ApiException
from db import db
import spoonacular
import requests
import base64
from PIL import Image
import io
from pathlib import Path
import datetime

from configurations import SERVER_PORT, IMAGE_SAVE_PATH, API_TOKEN

app = Flask(__name__)
# Image save path
image_save_path = Path(IMAGE_SAVE_PATH)
image_save_path.mkdir(exist_ok=True, parents=True)
# API configuration
configuration = spoonacular.Configuration()
configuration.api_key['apiKey'] = API_TOKEN
# create an instance of the API class
api_instance = spoonacular.DefaultApi(spoonacular.ApiClient(configuration))
ip = requests.get('https://checkip.amazonaws.com').text.strip()


@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    path = image_save_path / filename
    return send_file(path)


@app.route('/confirm', methods=['POST'])
def confirm_query():
    query_id = request.form['query_id']
    new_name = request.form.get('new_name')
    weight = request.form['weight']
    meal_time = request.form['meal_time']
    sql = "UPDATE meals " \
          "SET name='%s', weight='%s', meal_time='%s', valid='%s' WHERE id='%s'" % \
          (new_name, weight, meal_time, '1', query_id)
    db.execute_db(sql)

    response = {
        'status': 'success'
    }
    return response


@app.route('/upload', methods=['POST'])
def image_analysis():
    image_base64 = request.form['file']
    user_id = request.form['user_id']

    img = Image.open(io.BytesIO(base64.b64decode(image_base64)))
    img = img.rotate(-90)
    img_filename = user_id + '_' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + '.jpg'
    img.save(image_save_path / img_filename)
    print((image_save_path / img_filename).absolute())

    # The URL of the image to be analyzed.
    image_url = 'http://' + ip + ':' + str(SERVER_PORT) + '/images/' + img_filename
    response = {
        'id': '',
        'name': '',
        'nutrition': {
            'calories': '',
            'fat': '',
            'protein': '',
            'carbs': ''
        }
    }
    try:
        # Image Analysis by URL
        api_response = api_instance.image_analysis_by_url(image_url)
        print(api_response)
        response['name'] = api_response['category']['name']
        response['nutrition']['calories'] = api_response['nutrition']['calories']['value']
        response['nutrition']['fat'] = api_response['nutrition']['fat']['value']
        response['nutrition']['protein'] = api_response['nutrition']['protein']['value']
        response['nutrition']['carbs'] = api_response['nutrition']['carbs']['value']
        sql = "INSERT INTO meals (user_id, image_path, name, calories, fat, protein, carbs, valid) " \
              "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  user_id, (image_save_path / img_filename).as_posix(), api_response['category']['name'],
                  api_response['nutrition']['calories']['value']
                  , api_response['nutrition']['fat']['value'], api_response['nutrition']['protein']['value'],
                  api_response['nutrition']['carbs']['value']
                  , 0)
        print(sql)
        db.execute_db(sql)
        print(db.cur.lastrowid)
        response['id'] = db.cur.lastrowid

    except ApiException as e:
        return "Exception when calling DefaultApi->image_analysis_by_url: %s\n" % e, 500

    # print(request.headers)
    # print(image_url)
    return response


@app.route("/get_daily_images", methods=['POST'])
def get_daily_images():
    date = request.form['date']
    user_id = request.form['user_id']
    max_num = request.form.get('max_num')
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_next = date + datetime.timedelta(days=1)
    sql = "SELECT image_path FROM meals WHERE user_id='%s' AND create_time BETWEEN '%s' AND '%s'" % (
    user_id, date.strftime("%Y-%m-%d"), date_next.strftime("%Y-%m-%d"))
    print(sql)
    image_paths = db.select_db(sql)
    response = {'image_amount': 0,
                'images': []}
    for image_path in image_paths:
        with open(image_path['image_path'], "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            response['images'].append(img_base64)
            response['image_amount'] += 1
            if response['image_amount'] == max_num:
                break
    return response


@app.route("/get_daily_nutrition", methods=['POST'])
def get_daily_nutrition():
    date = request.form['date']
    user_id = request.form['user_id']
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_next = date + datetime.timedelta(days=1)
    sql = "SELECT COALESCE(SUM(calories),0) as calories, COALESCE(SUM(fat),0) as fat, COALESCE(SUM(protein),0) as protein, COALESCE(SUM(carbs),0)as carbs FROM meals " \
          "WHERE user_id='%s' AND valid='1' AND create_time BETWEEN '%s' AND '%s'" % (user_id,
                                                                                      date.strftime("%Y-%m-%d"),
                                                                                      date_next.strftime("%Y-%m-%d"))
    print(sql)
    result = db.select_db(sql)
    return result[0]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
