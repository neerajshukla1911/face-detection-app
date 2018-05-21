Face Detection App
******************
Create your own face detection rest api in python.

Installation
------------
Face detection app has been tested in **Ubuntu 16.04** with **python 3.5**. Although it might work in other environmentes with/without few changes.

.. code:: shell

    git clone https://github.com/neerajshukla1911/face-detection-app.git
    cd face-detection-app
    pip install -r requirements.txt
    git clone https://github.com/davisking/dlib.git
    python setup.py install --yes USE_AVX_INSTRUCTIONS
    python app.py

Run Server
----------
Below command will start face-detection server on port 8882. Port can be modified in app.py file.

.. code:: shell
    python app.py


REST API Details
----------------
**API**:          http://localhost:8882/face-detection
**Request method**: post
**Request Type**: form-data
**Request Parameter**:
    - file: file object
**Response**:

Usage
-----
You can use any http client (eg. postman) to hit post request on  http://localhost:8882/face-detection
Below is sample curl request. Change file path to your image file path.
.. code:: shell

    curl \
      -F "file=@/home/neeraj/2.jpg" \
      localhost:8882/face-detection



