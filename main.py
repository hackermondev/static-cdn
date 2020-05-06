from flask import *
import flask
from werkzeug.utils import secure_filename
import os
import random
import string

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/static/uploads/"

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route("/",methods=['POST','GET'])
def home_upload():
  if request.method == 'GET':
    return render_template('upload.html')
  else:
    print()
    if 'file' not in request.files:
      return render_template('error.html',error="Please select a file")
    file = request.files['file']
    if file.filename == '':
      return render_template('error.html',error="Please select a file")
    filename = randomString(10)
    absolute_path = os.path.dirname(os.path.realpath(__file__)) + app.config['UPLOAD_FOLDER']
    if request.files['file'].mimetype.split('/')[0] == 'image':
      filename = filename + f".{request.files['file'].mimetype.split('/')[1]}"
    try:
      file.save(absolute_path + filename)
      return redirect(f'/static/uploads/{filename}')
    except FileNotFoundError as e:
      print(e)
      return render_template('error.html',error="Internal Server Error")


try:
  app.run(host="0.0.0.0",port=3000)
except:
  print("Could not start server")