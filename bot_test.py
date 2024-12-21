import os
import tempfile
from src.bot import graph_workflow

def analyze_image(file_path):
    """Analyzes the uploaded image and returns a dictionary with the results."""
    sums = {}

    inputs = {"path": file_path}
    app = graph_workflow()

    for output in app.stream(inputs):
        for key, value in output.items():
            if key == "generate_summary_node":
                sums['summary'] = value['summary']
            if key == "value_extractor_node":
                sums['anamoly'] = value['anamoly']
            if key == "root_cause_node":
                sums['root_cause'] = value['root_cause']
            if key == "root_cause_1_node":
                sums['root_cause_1'] = value['root_cause_1']
            if key == "Translation_node":
                sums['translation'] = value['translation']

    return sums
