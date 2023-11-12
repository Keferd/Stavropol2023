import os

from flaskapp import app
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
import json
from ml.predict import predict
from image_processing.esrgan import image_proccessing

import base64


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# @app.route('/api/text', methods=['POST'])
# def post_text():
#     if not request.json or 'text' not in request.json:
#         return bad_request()
#     else:
#         text = request.json['text']
#         model_c = request.json['model']
#         response = {}
#         predicted_class, weights_dict = solution(text, model=model_c)
#         response["class"] = predicted_class
#         response["categories"] = get_categories(predicted_class)

#         response["weights"] = dict(sorted(weights_dict.items(), key=lambda item: item[1], reverse=True))


#         return json_response(response)


@app.route('/api/file', methods=['POST'])
def post_file():
    """
    Обработка полученного сервером изображения
    :return:
    """
    try:
        file = request.files["file"]
        camera = request.form.get('camera')
        model = request.form.get('model')
        check = False
        check = request.form.get('check')

        camera = camera.replace('"', '')
        model = model.replace('"', '')
        
        
        if file and camera and model and file.filename.endswith('.jpg'):
            save_path = os.path.join(os.path.dirname(__file__), file.filename)
            file.save(save_path)

            #тут внес изменения Kashanaft для улучшения изображения
            if check == "true":
                image_proccessing(save_path)

            output_image_path, result = predict(camera, save_path, model)

            os.remove(save_path)
            
            with open(output_image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            response_data = {
                'image_url': encoded_image, 
                'json_object': result
            }

            os.remove(output_image_path)

            return jsonify(response_data)

        else:
            return "Файл должен быть формата .jpg", 400

    except Exception as e:
        print(e)
        return str(e), 500

# @app.route('/api/file', methods=['POST'])
# def post_file():
#     file = request.files["file"]
#     camera = request.form.get('camera')

#     if file and file.filename.endswith('.jpg'):
#         try:
#             save_path = os.path.join(os.path.dirname(__file__), file.filename)
#             file.save(save_path)

#             if camera:
#                 json_object = json.loads(camera)
#             else:
#                 json_object = {}

#             print(save_path)
#             print(file.filename)
#             print(json_object)

#             return send_file(save_path, download_name=file.filename)
#         except Exception as e:
#             print(e)
#             return str(e), 500
#     else:
#         return "Файл должен быть формата .jpg", 400


def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)