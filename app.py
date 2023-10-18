import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb+srv://test:test@cluster0.twt800w.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_string)
db = client.dbsparta
app = Flask(__name__)

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')  # Ganti 'Content_receive' menjadi 'content_receive'

    today = datetime.now()
    mytime = today.strftime('%Y-%M-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'

    profile = request.files['profile_give']
    profile_extension = profile.filename.split('.')[-1]
    profile_filename = f'static/profile-{mytime}.{profile_extension}'
    profile.save(profile_filename)

    save_to = 'static/myimage.jpg'
    file.save(save_to)

    doc = {
        'file': filename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)