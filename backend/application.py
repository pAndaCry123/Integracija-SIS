from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
UPLOAD_FOLDER = 'upload_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from views import *

if __name__ == '__main__':
    app.run(port=5000,debug=True)