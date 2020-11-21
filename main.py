from flask import Flask, send_file, request
from flask_restful import Resource, Api, abort
from marshmallow import Schema, fields, ValidationError, validate

import base64
import qrcode
from io import BytesIO

# Class te generate QR Codes
class QRCodeGenerator:

    correction_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self, data, version=None, error_correction='M', box_size=10, border=0, fit=True, mode='raw'): 
        self.data = data
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border
        self.fit = fit
        self.mode = mode

    def generate(self):
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
        qr_img.save(out, "PNG")
        out.seek(0)

        if self.mode == "base64":
            return u"data:image/png;base64," + base64.b64encode(out.getvalue()).decode("ascii")
        elif self.mode == "raw":
            return out

# Schema for request data
class QRCodeSchema(Schema):
    data = fields.Str(required=True)
    version = fields.Int(missing=None, validate=validate.Range(min=1, max=40))
    error = fields.Str(missing='M', validate=validate.OneOf(QRCodeGenerator.correction_levels.keys()))
    box_size = fields.Int(missing=10, validate=validate.Range(min=1))
    border = fields.Int(missing=4)


# QRCode resource
class QRCodeAPI(Resource):
    def get(self):
        try:
            result = QRCodeSchema().load(request.args)

            qr_generator = QRCodeGenerator(
                data=result['data'], 
                version=result['version'],
                error_correction=result['error'],
                box_size=result['box_size'],
                border=result['border'])

            image = qr_generator.generate()

            return send_file(image, mimetype="image/png")

        except ValidationError as err:
            abort(str(err.messages))
            

# create Flask application and api
app = Flask(__name__)
api = Api(app)

# add resource for qr code generation
api.add_resource(QRCodeAPI, '/qrcode', endpoint='qrcode')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)