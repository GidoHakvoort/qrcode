# Docker RESTful QR Code Generator

<!-- Shields -->
![Top language](https://img.shields.io/github/languages/top/GidoHakvoort/qrcode?style=for-the-badge)
![Code size](https://img.shields.io/github/languages/code-size/GidoHakvoort/qrcode?style=for-the-badge)
[![Last commit](https://img.shields.io/github/last-commit/GidoHakvoort/qrcode?style=for-the-badge)](https://github.com/GidoHakvoort/qrcode/commits/master)
[![License](https://img.shields.io/github/license/GidoHakvoort/qrcode?style=for-the-badge)](https://github.com/GidoHakvoort/qrcode/blob/master/LICENSE)

<!-- Project description -->
A simple RESTful API for QR Code generation in Docker using [python-qrcode](https://github.com/lincolnloop/python-qrcode), [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Flask-RESTful](https://github.com/flask-restful/flask-restful/) and [marshmallow](https://github.com/marshmallow-code/marshmallow).

## Prerequisities
Before you begin, ensure you meet the following requirements:

**For Python usage:**
- You have a machine with [Python 3.7+](https://www.python.org/)
- You have installed [pip](https://pip.pypa.io/en/stable/installing/) and [venv](https://docs.python.org/3/tutorial/venv.html)

**For Docker usage:**
- You have a machine with the latest version of [Docker](https://www.docker.com/) installed.

## Run with Python

Clone the project repository:
```
git clone https://github.com/GidoHakvoort/qrcode.git
cd qrcode
```

Create and activate a virtual environment:

```
python -m venv .
source bin/activate
```

Install the requirements using pip:
```
pip install -r requirements.txt
```

Finally, run the app:
```
python main.py
```
You should be able to access the API at http://localhost:3000/qrcode.

## Run with Docker

Clone the project repository:
```
git clone https://github.com/GidoHakvoort/qrcode.git
cd qrcode
```

To build the Docker image, simply run:
```
docker build -t qrcode .
```

To run the Docker image, run the following:
```
docker run -d --name qrcode -p 3000:3000 qrcode
```
You should be able to access the API at http://localhost:3000/qrcode.

To stop the Docker container, simply run:

```
docker stop qrcode
```

## Generating QR Codes

Once you have the RESTful API running using either Python or Docker you can create a QR code with a URL GET request.

### Syntax

Root URL: [http://localhost:3000/qrcode?](http://localhost:3000/qrcode?)

The request support the following URL query parameters:

**Required**
| Parameter | Type |  Description |
| --------- | ---- |  ----------- |
| data | String | The data to be encode. |

**Optional**

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| version | Integer |  | Version refers to the overall dimension of the QR Code in black/white squares. Possible values ranges from 1 to 40 where the total number of squares in each direction (width / height) equals 4 x version number + 17 (read more [here](https://www.qrcode.com/en/about/version.html)). Leave empty to let this be determine automatically.|
| error | String | M | The error correction to be used for the QR Code. This can be one of four values: L, M, Q or H with error correction capability of approximately 7%, 15%, 25% or 30% respectively (read more [here](https://www.qrcode.com/en/about/error_correction.html)). |
| box_size | Integer | 10 | The size of the individual squares in pixels. |
| border | Integer | 4 | The size of the border in squares. |
| logo | URL |  | If provided, the REST API will attempt to download the image and paste it at the center of the QR Code. Note that this is not according to the JIS or ISO standard and that scanning the QR Code might become slow or even impossible. Selecting a higher error correction might help but is not guaranteed to work. |
| logo_size | Integer | 7 | The size of the logo in squares. Possible values range from 3 to 11.|

**Example**
```
curl http://localhost:3000/qrcode?data=Hello%20World > qrcode.png
```


## License
This project uses an [MIT License](https://github.com/GidoHakvoort/qrcode/blob/master/LICENSE).