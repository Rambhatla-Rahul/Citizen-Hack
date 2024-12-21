
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain import hub
from langchain.schema import Document
from langgraph.graph import START, StateGraph, END
from typing import Literal, List
from typing_extensions import TypedDict
from dotenv import load_dotenv
from PIL import Image
import easyocr
import os
import pprint
import warnings
from src.generate_summary import GraphState, ocr, report, generate_summary, anamoly_detection, value_extractor, root_cause, root_cause_1,Translate_Summary, remove_details
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def graph_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("ocr_node", ocr)
    workflow.add_node("report_node", report)
    workflow.add_node("generate_summary_node", generate_summary)
    workflow.add_node("Translation_node",Translate_Summary)
    workflow.add_node("value_extractor_node", value_extractor)
    workflow.add_node("root_cause_node", root_cause)
    workflow.add_node("root_cause_1_node", root_cause_1)
    workflow.add_node("remove_details", remove_details)

    workflow.add_edge(START, "ocr_node")
    workflow.add_edge("ocr_node", "report_node")
    workflow.add_edge("report_node","remove_details")
    workflow.add_edge("remove_details", "generate_summary_node")
    workflow.add_edge("generate_summary_node","Translation_node")
    workflow.add_edge("Translation_node",END)

    workflow.add_conditional_edges("Translation_node", anamoly_detection,{
        "Anamoly" : "value_extractor_node",
        "Normal": "root_cause_1_node"
    })

    workflow.add_edge("root_cause_1_node", END)

    workflow.add_edge("value_extractor_node", "root_cause_node")
    workflow.add_edge("root_cause_node", END)

    app = workflow.compile()
    return app

if __name__ == "__main__":
    app = graph_workflow()
    inputs = {"path": r"C:\Users\aashutosh kumar\OneDrive\Pictures\WhatsApp Image 2024-08-29 at 18.24.47_a7a30409.jpg"}
    for output in app.stream(inputs):
        for key, value in output.items():
            
            pass
  