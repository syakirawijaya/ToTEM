from flask import Flask, render_template, request, send_file, redirect, url_for, session, send_from_directory
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from datetime import datetime
import os

app = Flask(__name__)
qrcode = QRcode(app)  # Initialize QRcode extension
db = TinyDB('db.json')

# Configurations
app.secret_key = 'testTOTEM2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['QR_FOLDER'] = 'qrcodes'  # Folder to save QR code images

# Ensure the upload and QR code folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
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

@app.route('/user/<user_route>')
def user_page(user_route):
    User = Query()
    user_data = db.search(User.route == user_route)
    if user_data:
        user_data = user_data[0]
        
        # Generate URL for QR code
        qr_url = 'http://10.16.20.202:5000/user/' + user_route
        
        print(f"Generated URL for QR code: {qr_url}")

        # Generate QR code image
        qr_image = qrcode(qr_url, mode="raw")

        # Save QR code image to a file
        qr_filename = f"{user_route}.png"
        qr_filepath = os.path.join(app.config['QR_FOLDER'], qr_filename)
        with open(qr_filepath, 'wb') as f:
            f.write(qr_image.getvalue())

        # Return the URL of the saved QR code image
        qr_image_url = url_for('qr_image', filename=qr_filename)

        return render_template('user_page.html', user_data=user_data, qr_image_url=qr_image_url)

    return 'User not found', 404

@app.route('/qrcodes/<filename>')
def qr_image(filename):
    return send_from_directory(app.config['QR_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
