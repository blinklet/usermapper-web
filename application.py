from flask import Flask, render_template, send_from_directory, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os, tempfile
import yaml
from usermapper.usermapper import xmlwriter
from usermapper.mapperdata import get_users
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv

app = Flask(__name__)
bootstrap = Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['FLASK_APP'] = os.environ.get('FLASK_APP')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

class MyForm(FlaskForm):
    filename = FileField('Select configuration file: ', 
        validators=[FileRequired(), FileAllowed(['yaml'], 
        message='Only YAML files accepted')], 
        description="Only YAML files accepted")
    submit = SubmitField('Upload')
    
@app.route("/", methods=('GET','POST'))
def index():
    form = MyForm()
    filename = None
    if form.validate_on_submit():

        f = form.filename.data
        basedir = os.path.join(
            os.path.relpath(os.path.dirname(__file__)), 
            'downloads')
        tempdir = tempfile.mkdtemp(dir=basedir)

        filename = os.path.join(tempdir,'user-mapping.xml')

        configuration = yaml.safe_load(f.read())
        structure = get_users(configuration)
        xmlwriter(structure,filename)

        temp_folder = os.path.split(tempdir)[1]
        return redirect (url_for('download_page', temp_folder=temp_folder))

    return render_template('index.html', form=form)

@app.route('/download_page/<temp_folder>', methods=('GET','POST'))
def download_page(temp_folder):
    filename = os.path.join(
        os.path.relpath(os.path.dirname(__file__)), 
        'downloads',temp_folder,'user-mapping.xml')

    with open(filename) as preview:
       data = preview.readlines()
    
    download_url = url_for('download', tempfolder=temp_folder, filename='user-mapping.xml')

    return render_template('download.html', 
        data=data, download_url=download_url)

@app.route("/download/<tempfolder>/<filename>", methods=('GET','POST'))
def download(tempfolder,filename):
    basedir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        'downloads')
    temp_dir = os.path.join(basedir,tempfolder)
    return send_from_directory(
        temp_dir, filename, as_attachment=True)