import os
from flask import Flask,flash,redirect,url_for,render_template,request
from werkzeug.utils import secure_filename
import secrets
from ml_model import get_prediction

UPLOAD_FOLDER = '.'
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
            tmp_path = app.config['UPLOAD_FOLDER']+ 'tmp.'+ file.filename.rsplit('.', 1)[1]
            file.save(tmp_path)
            label, result = get_prediction(tmp_path)
            flash('Your results: ' + label + '\nConfidence: '+ str(result))
        else:
            flash('Unsupported file type!\nPlease upload file in .jpg, .jpeg, or .png formats only.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)