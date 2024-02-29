from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template ('index.html')

    firstName = request.form.get('name')
    lastName = request.form.get('lastname')

    print(firstName, lastName)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()