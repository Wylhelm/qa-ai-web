from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class TestScenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    criteria = db.Column(db.Text, nullable=False)
    scenario_text = db.Column(db.Text, nullable=False)
    processed_files = db.Column(db.Text, nullable=False)
    ui_elements = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'criteria': self.criteria,
            'scenario_text': self.scenario_text,
            'processed_files': json.loads(self.processed_files),
            'ui_elements': json.loads(self.ui_elements),
            'timestamp': self.timestamp.isoformat()
        }

class Database:
    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scenarios.db'
        db.init_app(app)
        with app.app_context():
            db.create_all()

    def save_scenario(self, test_scenario):
        new_scenario = TestScenario(
            name=test_scenario.name,
            criteria=test_scenario.criteria,
            scenario_text=test_scenario.scenario_text,
            processed_files=json.dumps(test_scenario.processed_files),
            ui_elements=json.dumps(test_scenario.ui_elements)
        )
        db.session.add(new_scenario)
        db.session.commit()

    def get_scenarios(self):
        return TestScenario.query.order_by(TestScenario.timestamp.desc()).all()

    def clear_history(self):
        TestScenario.query.delete()
        db.session.commit()

    def get_scenario_by_id(self, scenario_id):
        return TestScenario.query.get(scenario_id)
