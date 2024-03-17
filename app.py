from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from datetime import datetime
import os

app = Flask(__name__)
qrcode = QRcode(app)
db = TinyDB('db.json')

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
        file = request.files['image']
        description = request.form['description']
        title = request.form['title']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            user_route = f"{session.get('firstname').lower()}_{session.get('lastname').lower()}_{timestamp}"
            db.insert({
                'firstname': session.get('firstname'),
                'lastname': session.get('lastname'),
                'title': title,
                'description': description,
                'filename': filename,
                'route': user_route
            })
            return redirect(url_for('user_page', user_route=user_route))
    return render_template('uploadForm.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<user_route>')
def user_page(user_route):
    User = Query()
    user_data = db.search(User.route == user_route)
    if user_data:
        user_data = user_data[0]

        print(f"Generated URL for QR code: {request.url}")

        return render_template('user_page.html', user_data=user_data)
    return 'User not found', 404

#TEST
@app.route('/test_qr')
def test_qr():
    # This route is just for testing QR code generation
    test_url = 'https://blog.teclado.com/file-uploads-with-flask/'
    qr_img_src = qrcode(test_url, mode='raw')
    return f'<img src="{qr_img_src}" alt="QR Code">'

#TEST2
@app.route('/test_qr_image')
def test_qr_image():
    # Generate a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data("https://blog.teclado.com/file-uploads-with-flask/")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)