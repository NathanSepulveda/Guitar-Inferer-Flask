import fastai
from fastai.imports import *
from fastai.learner import load_learner
# from fastai.vision.widgets import *
from fastai.vision.core import PILImage
path = Path()
print(path.ls(file_exts='.pkl'))
learn_inf = load_learner(path/'export.pkl')
predict = learn_inf.predict('test2.jpeg')[0]
from flask import Flask, request, render_template
import os
import glob
from flask import send_file
app = Flask(__name__)

#Defining the home page for the web service
# @app.route('/')
# def home():
#     return f"<h1>{predict}</h1>"


# UPLOAD_FOLDER = './upload'
UPLOAD_FOLDER = os.path.join('static', 'upload')

app = Flask(__name__, static_folder=os.path.abspath('static'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def clear_contents():
    files = glob.glob(UPLOAD_FOLDER)
    for f in files: os.remove(f)

def get_image(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, mimetype='image/gif')

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        pred,pred_idx,probs = learn_inf.predict(path)
        predPercent = f'{probs[pred_idx]*100:.02f}'
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        print(full_filename)
        return render_template('index.html', guitar_type = pred, prob = predPercent, user_image = full_filename)

        return 'ok'
    return render_template('start.html')


if __name__ == "__main__":
    app.run(debug=True)