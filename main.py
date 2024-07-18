from flask import Flask, render_template, request, jsonify
from ai_processor import AIProcessor
from database import Database
from image_processor import ImageProcessor
from test_scenario import TestScenario
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scenarios.db'

ai_processor = AIProcessor()
database = Database(app)
image_processor = ImageProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        processed_data = ai_processor.process_file(filename)
        return jsonify(processed_data)

@app.route('/generate', methods=['POST'])
def generate_scenario():
    data = request.json
    scenario_name = data['name']
    criteria = data['criteria']
    processed_files = data['processed_files']
    scenario = ai_processor.generate_scenario(criteria, processed_files)
    test_scenario = TestScenario(scenario_name, criteria, scenario, processed_files)
    database.save_scenario(test_scenario)
    return jsonify({'scenario': scenario})

@app.route('/history')
def get_history():
    scenarios = database.get_scenarios()
    return jsonify([scenario.to_dict() for scenario in scenarios])

@app.route('/clear_history', methods=['POST'])
def clear_history():
    database.clear_history()
    return jsonify({'message': 'History cleared'})

@app.route('/update_prompt', methods=['POST'])
def update_prompt():
    data = request.json
    prompt_type = data['type']
    new_prompt = data['prompt']
    if prompt_type == 'system':
        ai_processor.set_system_prompt(new_prompt)
    elif prompt_type == 'scenario':
        ai_processor.set_scenario_prompt(new_prompt)
    return jsonify({'message': f'{prompt_type.capitalize()} prompt updated'})

@app.route('/update_context_window', methods=['POST'])
def update_context_window():
    data = request.json
    new_size = int(data['size'])
    ai_processor.set_context_window_size(new_size)
    return jsonify({'message': f'Context window size updated to {new_size}'})

if __name__ == '__main__':
    app.run(debug=True)
