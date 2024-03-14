from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        firstName = request.form.get('firstname')  # corrected from 'name' to 'firstname'
        lastName = request.form.get('lastname')

        print(firstName, lastName)

        return redirect(url_for('upload'))
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('uploadForm.html')

if __name__ == '__main__':
    app.run()