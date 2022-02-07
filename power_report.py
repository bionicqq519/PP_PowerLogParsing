# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 15:37:27 2022

@author: Nick
"""
import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}

@app.route("/")
def hello():
    return "Flask on port 8888."

@app.route("/power")
def power():
    return render_template("./power_upload.html")

def allowed_file(filename):
    # 判斷後綴
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def parseCSV(file):
    df = pd.read_csv(file)
    # msg = '<table>'
    # msg += '<tr>'
    # msg += '    <th>Power-IA Core Power(Watts) mean.</th>'
    # msg += '    <th>Power-Integrated Graphics Power(Watts) mean.</th>'
    # msg += '<tr>'
    # msg += '<tr>'
    # msg += ('    <td>'+ str(df['Power-IA Core Power(Watts)'].mean()) +'</td>')
    # msg += ('    <td>'+ str(df['Power-Integrated Graphics Power(Watts)'].mean()) +'</td>')
    # msg += '<tr>'
    # msg += '</table>'
    # print(msg)
    
    return df['Power-IA Core Power(Watts)'].mean(), df['Power-Integrated Graphics Power(Watts)'].mean()

@app.route("/upload_show", methods=['GET', 'POST'])
def upload_show():
    msg = "file uploaded failed"
    
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        # read by pandas
        # mean_msg = parseCSV(file)
        
        
        filename = secure_filename(file.filename)
        if filename == '' or not allowed_file(filename):
            return "file is empty or not .csv"
        
        cpu_mean, gpu_mean = parseCSV(file)
        
        filepath = os.path.join('./upload', filename)
        #file.save(filepath)
        
        # msg = "file uploaded successfully. path = " + filepath + "<br>"
        # msg += mean_msg
        # msg += ('<a href="/download/' + filename + '">Download file</a><br>')
        return render_template('csv_result.html', filepath = filepath, cpu_mean = cpu_mean, gpu_mean = gpu_mean)
    else:
        msg = "file uploaded failed"
        
    return msg

@app.route("/download2/<path:filename>")
def downloader(filename):
	dirpath = os.path.join(app.root_path, 'upload')
	return send_from_directory(dirpath, filename, as_attachment=True)

@app.route('/download/<path:filename>')
def download_file(filename):
    file_path =  os.path.join(app.root_path, 'upload')
    file_path = os.path.join(file_path, filename)
    file_handle = open(file_path, 'r')
    
    print(filename)

    # This *replaces* the `remove_file` + @after_this_request code above
    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(file_path)

    return app.response_class(
        stream_and_remove_file(),
        headers={'Content-Disposition': 'attachment', 'filename': filename}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
