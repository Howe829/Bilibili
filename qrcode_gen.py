import qrcode
from qrcode.constants import ERROR_CORRECT_H
import string
import random

base = string.ascii_letters + string.digits


def generate(data):
    qr = qrcode.QRCode(version=2.0, error_correction=ERROR_CORRECT_H, box_size=3, border=2)

    qr.add_data(data=data)
    qr.make()
    img = qr.make_image()
    name = "".join([random.choice(base) for i in range(5)]) + '.jpg'
    img.save('qrcode_jpg/'+name)
    return name
