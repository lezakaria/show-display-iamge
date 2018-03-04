from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from base64 import b64encode
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.LargeBinary)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def uplaod():
    f = request.files['inputFile']

    newFile = FileContents(data=f.read())
    db.session.add(newFile)
    db.session.commit()
    return 'Saved' 

@app.route('/show/')
def download():
      file_data = FileContents.query.filter_by(id=3).first()
      tr =  send_file(BytesIO(file_data.data), attachment_filename='logo.png', mimetype='image/png')
#     #return render_template('display.html', file_data=file_data)
#      return ('tr')
      return render_template("display.html", image=tr)
  #    return (send_file(BytesIO(file_data.data), attachment_filename='logo.png', mimetype='image/png'))

# @app.route('/show/')
# def show():
#     file_data = FileContents.query.filter_by(id=3).first()
#     image = b64encode(file_data.data)                            # defined in the tag
#     return render_template('display.html', file_data=file_data, image=image)
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
