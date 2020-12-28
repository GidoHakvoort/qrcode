"""
Simple REST API server for generating QR Codes
"""

import base64

from io import BytesIO
from flask import Flask, send_file, request
from flask_restful import Resource, Api, abort
from marshmallow import Schema, fields, ValidationError, validate
from PIL import Image

import requests
import qrcode

# Class te generate QR Codes
class QRCodeGenerator:
    """
    Class to generage QR Codes
    """

    correction_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self, data, version=None, error_correction='M', box_size=10, border=4, logo=None, logo_size=7, fit=True, mode='raw'):
        self.data = data
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border
        self.logo = logo
        self.logo_size = logo_size
        self.fit = fit
        self.mode = mode

    def generate(self):
        """
        Generate a QR Code. In case a logo if provided paste it in the center
        """

        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.correction_levels[self.error_correction],
            box_size=self.box_size,
            border=self.border,
        )

        qr.add_data(self.data)
        qr.make(fit=self.fit)

        # prepare output
        out = BytesIO()
        qr_img = qr.make_image(back_color='white', fill_color='black')
        qr_img = qr_img.convert("RGBA")

        # insert logo if provided
        if self.logo:
            # download image and create logo
            response = requests.get(self.logo)
            response.raise_for_status()

            logo = Image.open(BytesIO(response.content))

            # scale logo to number of box_size
            logo = logo.resize((self.logo_size * self.box_size, self.logo_size *self.box_size))

            # past logo in center of QR code
            position = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
            qr_img.paste(logo, position)

        qr_img.save(out, "PNG")
        out.seek(0)

        if self.mode == "base64":
            return u"data:image/png;base64," + base64.b64encode(out.getvalue()).decode("ascii")

        return out

# Schema for request data
class QRCodeSchema(Schema):
    """
    The QR Code RESTful parameter schema
    """

    data = fields.Str(required=True)
    version = fields.Int(missing=None, validate=validate.Range(min=1, max=40))
    error = fields.Str(missing='M', validate=validate.OneOf(QRCodeGenerator.correction_levels.keys()))
    box_size = fields.Int(missing=10, validate=validate.Range(min=1))
    border = fields.Int(missing=4)
    logo = fields.Url(missing=None)
    logo_size = fields.Int(missing=7, validate=validate.Range(min=3, max=11))


# QRCode resource
class QRCodeAPI(Resource):
    """
    The QR Code RESTful resource
    """

    def get(self):
        """
        Endpoint for QR Code API.
        """
        try:
            result = QRCodeSchema().load(request.args)

            # create QR generator
            qr_generator = QRCodeGenerator(
                data=result['data'],
                version=result['version'],
                error_correction=result['error'],
                box_size=result['box_size'],
                border=result['border'],
                logo=result['logo'],
                logo_size=result['logo_size'])

            # get the QR image
            image = qr_generator.generate()

            return send_file(image, mimetype="image/png")

        except ValidationError as err:
            return abort(str(err.messages))

        except requests.RequestException as err:
            return abort("{{'logo':['{}']}}".format(str(err)))

# create Flask application and api
errors = {
        'InternalServerError': {
        'status': 500,
        'message': 'Internal Server Error'
    },
}

app = Flask(__name__)
api = Api(app, errors=errors)

# add resource for QR Code generation
api.add_resource(QRCodeAPI, '/qrcode', endpoint='qrcode')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
