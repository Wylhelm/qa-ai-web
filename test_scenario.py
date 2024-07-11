class TestScenario:
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
            'name': self.name,
            'criteria': self.criteria,
            'scenario_text': self.scenario_text,
            'processed_files': [{k: v for k, v in file.items() if k != 'image_data'} for file in self.processed_files],
            'ui_elements': self.ui_elements
        }

    @classmethod
    def from_dict(cls, data):
        scenario = cls(data['name'], data['criteria'], data['scenario_text'], data.get('processed_files', []))
        scenario.ui_elements = data.get('ui_elements', [])
        return scenario
