from flask import Flask, send_file
import os

app = Flask(__name__)


@app.route('/loginqr/<name>')
def qrcodea(name):
    if not '.jpg' in name:
        return 'Illegal Parameter!'
    return send_file(os.getcwd() + '/qrcode_jpg/{}'.format(name))




if __name__ == '__main__':
    app.run()
