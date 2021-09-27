import os
from flask import Flask,flash,redirect,url_for,render_template,request
from werkzeug.utils import secure_filename
import secrets

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

secret = secrets.token_urlsafe(32)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secret

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['inputfile']
        if file and allowed_file(file.filename):
            file.save(app.config['UPLOAD_FOLDER']+ secure_filename(file.filename))
            flash('Your results: ')
        else:
            flash('Unsupported file type!\nPlease upload file in .jpg, .jpeg, or .png formats only.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)