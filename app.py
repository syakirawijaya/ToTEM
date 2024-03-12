from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')  # This will create db.json if it doesn't exist

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        print(f"Received data: firstName={firstName}, lastName={lastName}")  # Debug print
        return redirect(url_for('upload'))
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        print(f"Received data: firstName={firstName}, lastName={lastName}")  # Debug print
        db.insert({'firstName': firstName, 'lastName': lastName})
        return render_template('uploadForm.html')  # Assuming you want to stay on the same page or redirect appropriately

    # Logic for GET request or initial page load
    return render_template('uploadForm.html')

if __name__ == '__main__':
    app.run(debug=True)  # Added debug=True for easier debugging
