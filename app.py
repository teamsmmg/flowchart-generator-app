from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}  # Allow only CSV
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read CSV file instead of Excel
                df = pd.read_csv(file)

                # Validate required columns
                required_columns = ['key', 'from', 'to']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    flash(f'Missing required columns: {", ".join(missing_columns)}')
                    return redirect(request.url)

                nodes = []
                links = []
                node_set = set()

                # First pass: create nodes
                for _, row in df.iterrows():
                    try:
                        key = str(row['key']).strip()
                        from_level = int(row['from'])

                        if key not in node_set:
                            nodes.append({"id": key, "level": from_level})
                            node_set.add(key)
                    except (ValueError, KeyError):
                        continue

                # Second pass: create links based on direct row mapping
                for _, row in df.iterrows():
                    try:
                        source_key = str(row['key']).strip()
                        from_level = int(row['from'])
                        to_level = int(row['to'])

                        target_rows = df[(df['from'] == to_level)]

                        for _, target_row in target_rows.iterrows():
                            target_key = str(target_row['key']).strip()

                            if source_key != target_key:
                                if target_key not in node_set:
                                    nodes.append({"id": target_key, "level": to_level})
                                    node_set.add(target_key)

                                link = {"source": source_key, "target": target_key}
                                if link not in links:
                                    links.append(link)

                    except (ValueError, KeyError):
                        continue

                # Sort nodes by level
                nodes.sort(key=lambda x: x['level'])

                print("Final Nodes:", json.dumps(nodes, indent=2))
                print("Final Links:", json.dumps(links, indent=2))

                if not nodes:
                    flash('No valid data found in the CSV file')
                    return redirect(request.url)

                return render_template("flowchart.html", nodes=nodes, links=links)

            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file (.csv)')
            return redirect(request.url)

    return render_template('index.html')

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
