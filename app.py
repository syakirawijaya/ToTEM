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
        return render_template('user_page.html', user_data=user_data)
    return 'User not found', 404

if __name__ == '__main__':
    app.run(debug=True)