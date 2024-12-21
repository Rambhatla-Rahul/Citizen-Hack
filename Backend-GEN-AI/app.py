import streamlit as st
from src.bot import GraphState, ocr, report, generate_summary, anamoly_detection, value_extractor, root_cause, root_cause_1
from src.bot import graph_workflow
import tempfile
import os

st.title("Medical Report Analyzer")

uploaded_file = st.file_uploader("Upload an image of the medical report", type=["jpg", "jpeg", "png", "pdf"])

sums = {}
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    inputs = {"path": temp_file_path}

    app = graph_workflow()

    for output in app.stream(inputs):
        for key, value in output.items():
            # st.write(f"Node '{key}': {value}")
            if key == "generate_summary_node":
                temp = value['summary']
                st.write(value['summary'])
            if key == "value_extractor_node":
                st.write(value['anamoly'])
            if key == "root_cause_node":
                st.write(value['root_cause'])
            if key == "root_cause_1_node":
                st.write(value['root_cause_1'])
            if key == "Translation_node":
                st.write(value['translation'])
            
    os.remove(temp_file_path)
else:
    st.write("Please upload an image file to start the analysis.")