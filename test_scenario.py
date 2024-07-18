from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TestScenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    criteria = db.Column(db.Text, nullable=False)
    scenario_text = db.Column(db.Text, nullable=False)
    processed_files = db.Column(db.JSON, nullable=False)
    ui_elements = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, criteria, scenario_text, processed_files):
        self.name = name
        self.criteria = criteria
        self.scenario_text = scenario_text
        self.processed_files = processed_files
        self.ui_elements = []

        for file in processed_files:
            if 'ui_elements' in file:
                self.ui_elements.extend(file['ui_elements'])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'criteria': self.criteria,
            'scenario_text': self.scenario_text,
            'processed_files': [{k: v for k, v in file.items() if k != 'image_data'} for file in self.processed_files],
            'ui_elements': self.ui_elements,
            'timestamp': self.timestamp.isoformat()
        }
