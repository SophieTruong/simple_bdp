from flask import Flask, flash, request
from werkzeug.utils import secure_filename
import os

from input_data_process import input_data_split

UPLOAD_FOLDER = './data_temp/'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'gz', 'geojson'} # .txt file for testing'

if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER)
    except Exception as e:
        print(e)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route("/")
def hello_world(): 
    return "<p>Hello, World!</p>"

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # TODO: move input data processing out of API
            input_data_split(filename)
            # Once data is processed, the raw data is deleted
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return filename + " is successfully uploaded"
        return "Only .txt, .csv, .gz, and .geojson files are allowed"
    
    return "Only POST method is allowed for this end point"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
