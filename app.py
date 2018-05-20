import os
import dlib
from skimage import io
from skimage.draw import polygon_perimeter
import io as python_io
import base64
from flask import jsonify
from flask import Flask
from flask import request
from flask_cors import CORS
from PIL import Image
import requests

app = Flask(__name__)

def box_with_skimage(image, xmin, ymin, xmax, ymax):
    try:
        yy, xx = polygon_perimeter([xmin, xmin, xmax, xmax, xmin], [ymin, ymax, ymax, ymin, ymin])
        image[xx, yy] = (255, 0, 0)

        xmin, ymin, xmax, ymax = xmin - 1, ymin - 1, xmax - 1, ymax - 1
        yy, xx = polygon_perimeter([xmin, xmin, xmax, xmax, xmin], [ymin, ymax, ymax, ymin, ymin])
        image[xx, yy] = (255, 0, 0)

        xmin, ymin, xmax, ymax = xmin + 2, ymin + 2, xmax + 2, ymax + 2
        yy, xx = polygon_perimeter([xmin, xmin, xmax, xmax, xmin], [ymin, ymax, ymax, ymin, ymin])
        image[xx, yy] = (255, 0, 0)

    except IndexError as e:
        return image

    return image


def rectangle_perimeter(r0, c0, r1, c1, shape=None, clip=False):
    rr, cc = [r0, r1, r1, r0], [c0, c0, c1, c1]
    return polygon_perimeter(rr, cc, shape=shape, clip=clip)


def encode_image(image):
    image_buffer = python_io.BytesIO()
    image.save(image_buffer, format='PNG')
    b_str = base64.b64encode(image_buffer.getvalue())
    imgstr = 'data:image/png;base64,{:s}'.format(b_str.decode())
    return imgstr


detector = dlib.get_frontal_face_detector()


@app.route('/face-detection', methods=['POST'])
def post():
    print("in request")
    if request.content_type.startswith('multipart/form-data'):
        request_data = request.form.to_dict()

        errors = []
        if 'file' not in request.files:
            errors.append({'file': 'please provide file'})

        file_to_predict = request.files['file']

    elif request.content_type.startswith('application/json'):
        request_data = request.json

        image_url = request_data.get('image_url')

        errors = []
        if not image_url:
            errors.append({'image_url': 'please provide image_url request'})
        if image_url and not image_url.startswith('http'):
            errors.append({'image_url': 'please provide valid image_url request'})

        if errors:
            return jsonify({'errors': errors}), 400

        res = requests.get(image_url, timeout=10)

        file_to_predict = python_io.BytesIO(res.content)

    else:
        return jsonify({'errors': [{'content_type': 'invalid request content_type'}]}), 400

    return_predicted_image = request_data.get('return_predicted_image', False)
    result = {"predictions": []}
    img = io.imread(file_to_predict)
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    dets = detector(img, 1)

    print("Number of faces detected: {}".format(len(dets)))

    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))

        result['predictions'].append(
            {'box': {"xmin": d.left(), "ymin": d.top(), "xmax": d.right(), "ymax": d.bottom()}})

        if return_predicted_image:
            img = box_with_skimage(img, d.left(), d.top(), d.right(), d.bottom())

    if return_predicted_image:
        img = Image.fromarray(img)
#        img.thumbnail((100,100), Image.ANTIALIAS)
        result['predicted'] = encode_image(img)

    return jsonify(result)


CORS(app, supports_credentials=True, allow_headers=['Content-Type', 'X-ACCESS_TOKEN', 'Authorization'])
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8882, debug=False)
