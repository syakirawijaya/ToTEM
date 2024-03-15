from flask import Flask, render_template, request, redirect, url_for, session
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
qrcode = QRcode(app)

# Configurations
app.secret_key = 'testTOTEM2024'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']

        print(session['firstname'], session['lastname'])

        return redirect(url_for('upload'))
    return render_template('index.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        firstname = session.get('firstname')
        lastname = session.get('lastname')

        return redirect(url_for('qrcode'))
        
    return render_template('uploadForm.html', firstname=session.get('firstname'), lastname=session.get('lastname'))

@app.route('/QR_code', methods=['GET', 'POST'])
def qrcode():
    return render_template('QRcodeGenerator.html')

if __name__ == '__main__':
    app.run()