# Docker RESTful QR Code Generator

<!-- Shields -->
![Top language](https://img.shields.io/github/languages/top/GidoHakvoort/qrcode?style=for-the-badge)
![Code size](https://img.shields.io/github/languages/code-size/GidoHakvoort/qrcode?style=for-the-badge)
[![Last commit](https://img.shields.io/github/last-commit/GidoHakvoort/qrcode?style=for-the-badge)](https://github.com/GidoHakvoort/qrcode/commits/master)
[![License](https://img.shields.io/github/license/GidoHakvoort/qrcode?style=for-the-badge)](https://github.com/GidoHakvoort/qrcode/blob/master/LICENSE)

<!-- Project description -->
A simple RESTful API for QR Code generation in Docker using [qrcode](https://github.com/lincolnloop/python-qrcode), [Flask](https://flask.palletsprojects.com/en/1.1.x/), [Flask-RESTful](https://github.com/flask-restful/flask-restful/) and [marshmallow](https://github.com/marshmallow-code/marshmallow).

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

## License
This project uses an [MIT License](https://github.com/GidoHakvoort/qrcode/blob/master/LICENSE).