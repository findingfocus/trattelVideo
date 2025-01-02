from flask import Flask, request, jsonify, send_file, render_template
from main import perform_task
import os
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')  # Serve the HTML form

@app.route('/run_task', methods=['POST'])
def run_task():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    year = data.get('year', '2024')
    videographer = data.get('videographer', 'Unknown')
    month_str = data.get('month')  # Month as a string
    day = data.get('day')
    start_time = data.get('start_time', '9:00AM')
    deponent = data.get('deponent', 'Unknown')
    case_name = data.get('case_name', 'Unknown vs. Unknown')
    plaintiff_attorney = data.get('plaintiff_attorney', 'Unknown')
    defense_attorney = data.get('defense_attorney', 'Unknown')

    if not all([month_str, day]):
        return jsonify({"error": "Month and day are required."}), 400

    zip_path, _ = perform_task(year, videographer, month_str, day, start_time, deponent, case_name, plaintiff_attorney, defense_attorney)

    if isinstance(zip_path, str) and zip_path.startswith("Error"):
        return jsonify({"error": zip_path}), 400

    return jsonify({
        "zip_file_url": request.host_url + "download?filepath=" + quote(zip_path)
    })

@app.route('/download')
def download_file():
    filepath = request.args.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found."}), 404
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
