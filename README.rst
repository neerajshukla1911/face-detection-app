Face Detection App
******************
Create your own face detection rest api in python.

Installation
------------
Face detection app has been tested in **Ubuntu 16.04** with **python 3.5**. Although it might work in other environments with/without few changes. Hit below commands in terminal to install app.

.. code:: shell

    git clone https://github.com/neerajshukla1911/face-detection-app.git
    cd face-detection-app
    pip install -r requirements.txt
    git clone https://github.com/davisking/dlib.git
    python setup.py install --yes USE_AVX_INSTRUCTIONS

Run Server
----------
Below command will start face-detection server on port 8882. Port can be modified in app.py file.

.. code:: shell
    python app.py


REST API Details
----------------
Below are face-detection REST api details.

.. code:: shell
    - Request Type: form-data
        - Request method: post
        - API:          http://localhost:8882/face-detection
        - Request Parameter:
            - file: file object (Required)
            - return_predicted_image: Return base64 string of image with detected faces bounding boxes. Value of parameter can true/false (optional)
        - Response: Returns list of coordinates of detected faces.

            {
                "predictions": [
                    {
                        "box": {
                            "xmax": 394,
                            "xmin": 305,
                            "ymax": 166,
                            "ymin": 76
                        }
                    }
                ]
            }

    - Request Type: application/json
        - Request method: post
        - API:          http://localhost:8882/face-detection
        - Request Parameter:
            - image_url: "image url of image" (Required)
            - return_predicted_image: Return base64 string of image with detected faces bounding boxes. Value of parameter can true/false (optional)
        - Response: Returns list of coordinates of detected faces.

            {
                "predictions": [
                    {
                        "box": {
                            "xmax": 394,
                            "xmin": 305,
                            "ymax": 166,
                            "ymin": 76
                        }
                    }
                ]
            }

Usage
-----
You can use any http client (eg. postman) to hit post request on  http://localhost:8882/face-detection
Below is sample curl requests. Change file path to your image file path.

.. code:: shell

    curl \
      -F "file=@/home/neeraj/2.jpg" \
      localhost:8882/face-detection

    curl \
      -F "file=@/home/neeraj/2.jpg" \
      -F "return_predicted_image=true" \
      localhost:8882/face-detection

    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"image_url":"https://d2zv4gzhlr4ud6.cloudfront.net/media/pictures/tagged_items/540x0/119_CFM04BL976/1.jpg"}' \
      localhost:8882/face-detection

    curl --header "Content-Type: application/json" \
      --request POST \
      --data '{"image_url":"https://d2zv4gzhlr4ud6.cloudfront.net/media/pictures/tagged_items/540x0/119_CFM04BL976/1.jpg", "return_predicted_image": true}' \
      localhost:8882/face-detection
