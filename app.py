import os
import pandas as pd
import analyzer
from flask import session
from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
from flask import redirect, url_for
from werkzeug.utils import secure_filename
from demoparser2 import DemoParser


app = Flask(__name__)

app.secret_key = 'secure'
UPLOAD_FOLDER = 'matches'
ALLOWED_EXTENSIONS = {'dem'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():

    match_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        match_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.dem')]

    stats = session.get('stats', {})

    # 3. ALLE Variablen übergeben (WICHTIG!)
    return render_template('index.html',
                           matches=match_files,
                           personal=stats.get('personal', {}),
                           teams=stats.get('teams', {}),       
                           kills=stats.get('kills', []),       
                           dateiname=stats.get('filename', 'Kein Match geladen')
                           )
#Dynamic pages, for every match in fileStorage
@app.route('/<match_id>')
def dynamic_page(match_id):

    match_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        match_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.dem')]

    stats = session.get('stats', {})

    # 3. ALLE Variablen übergeben (WICHTIG!)
    return render_template('dynamic_page.html',
                           matches=match_files,
                           personal=stats.get('personal', {}),
                           teams=stats.get('teams', {}),       
                           kills=stats.get('kills', []),       
                           space=stats.get('tot_kills', []),       
                           dateiname=stats.get('filename', 'Kein Match geladen'),
                           )












@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('matches', filename, as_attachment=True)

@app.route('/analyze/<filename>')
def analyze_existing(filename):
    file_path = os.path.join('matches', filename)
    
    if os.path.exists(file_path):

        session['stats'] = analyzer.run_analysis(file_path)
        return redirect(url_for('index'))
    else:
        return "Datei nicht gefunden", 404

@app.route('/matches')
def matches():

    match_files = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        match_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.dem')]

    stats = session.get('stats', {})

    return render_template('matches.html',
                           matches=match_files,
                           personal=stats.get('personal', {}),
                           teams=stats.get('teams', {}),       
                           kills=stats.get('kills', []),       
                           dateiname=stats.get('filename', 'Kein Match geladen'),
                           analyzed=stats.get('analyzed'))

@app.route('/upload', methods=['POST'])

def upload_file():

    if 'datei' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['datei']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        file_path = "/home/nicolai/csweb/matches/" + filename
        print(file_path)
        return redirect(url_for('index'))

    
    return "Fehler beim Upload", 400
    return jsonify({"error": "Invalid file type. Only .dem allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)