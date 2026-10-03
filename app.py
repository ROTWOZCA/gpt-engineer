import os
import subprocess
import shutil
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>GPT-Engineer Web</title></head>
<body>
    <h1>GPT-Engineer Web Interface</h1>
    <form action="/generate" method="post">
        <textarea name="prompt" rows="5" cols="50" placeholder="What do you want to build?"></textarea><br><br>
        <input type="submit" value="Generate Code">
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    project_path = "/tmp/my_project"
    os.makedirs(project_path, exist_ok=True)
    
    try:
        result = subprocess.run(
            ["gpte", project_path, "--prompt", prompt], 
            capture_output=True, text=True, timeout=300
        )
        
        shutil.make_archive("/tmp/output", 'zip', project_path)
        
        return f"<h2>Success!</h2><p>Output: {result.stdout}</p><p>Your project is ready.</p>"
    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
