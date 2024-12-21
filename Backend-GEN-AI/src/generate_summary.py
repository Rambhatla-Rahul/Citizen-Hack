
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langgraph.graph import START, StateGraph, END
from typing import Literal, List
from typing_extensions import TypedDict
from dotenv import load_dotenv
from PIL import Image
# from IPython.display import Image
import google.generativeai as genai
import easyocr
import os
import warnings
import re
import spacy
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(api_key = GOOGLE_API_KEY, model = "gemini-1.5-flash",temperature = 0.1)

class GraphState(TypedDict):
    report : str
    generation : str    
    summary : str
    anamoly : str
    root_cause : str
    path : str
    translation : str
    
def ocr(state):
    path = state["path"]
    warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
    reader = easyocr.Reader(['en'])
    warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
    result = reader.readtext(path)
    response = [detection[1] for detection in result]
    response_text = '\n'.join(response)
    return {"report" : response_text}


def redact_sensitive_info(report, doc):
    redacted_text = report  # Initialize redacted_text with the original report
    for ent in doc.ents:
        if ent.label_ == "PERSON":  
            redacted_text = redacted_text.replace(ent.text, "[REDACTED]")
    
    # Redact phone numbers and sensitive information
    redacted_text = re.sub(r'\b\d{10}(?:/\d{10})?\b', '[REDACTED]', redacted_text)
    redacted_text = re.sub(
        r'(?i)(?:deliver to|patient address|sample collected at)[:\s].(?:\n|$)',
        '[REDACTED]\n',
        redacted_text
    )

    return redacted_text

def remove_details(state):
    report = state["generation"]
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(report)
    redacted_text = redact_sensitive_info(report, doc)

    print(redacted_text)
    return {"generation" : redacted_text}


def report(state):
    report = state["report"]
    # generation = state["generation"]

    response = llm.invoke(f"You are being provided a medical report correct this grammatically{report} Note: Do not add anything extra. Just return the report as it is.").content
    return {"generation" : response}


def generate_summary(state):
    generation = state["generation"]
    # summary = state["summary"]

    response = llm.invoke(f"""You are an Expert in Evaluating medical Reports.You are given the report, 
                          Based on the report Devise a comprehensive in layman terms of the report in not more than 100 words.
                          report {generation}""").content
    print(response)
    
    return {"summary" : response}

def Translate_Summary(state):
    lang = "telugu"
    summary = state["summary"]
    response = llm.invoke(f"""
    You are a professional translator. Your task is to translate the following English summary into {lang}. 
    Ensure that any numbers, dates, and proper nouns remain in English. 
    Here is the summary to translate:"{summary}".""").content
    print(response)
    return {"translation" : response}


def anamoly_detection(state):#this is an edge
    summary = state["summary"]

    class Route_Anamoly(BaseModel):
        Binary_Score: str = Field(..., description="Does this report contain abnormal values? Yes or No")

    structured_llm = llm.with_structured_output(Route_Anamoly)

    system = """
    You are provided with a summary of a medical report containing various measurements and observations. 
    Your task is to identify any abnormal values or measurements. A value is considered abnormal if it is described as "elevated," "low," "absent," or if it falls outside the reference range.
    If any abnormal values are found, respond with 'Yes'. If no abnormal values are found, or if the summary lacks numerical data, respond with 'No'.
    """

    binary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "report:{report}")
        ]
    )

    grader_chain = binary_prompt | structured_llm

    llm_response = grader_chain.invoke({"report": summary})
    if llm_response.Binary_Score == "Yes":
        return "Anamoly"
    else:
        return "Normal"


def value_extractor(state):
    summary = state["summary"]

    system = """
    You are given a medical report summary that includes various measurements and observations. 
    Your task is to identify and extract all values or measurements that are described as abnormal. 
    A value is considered abnormal if it is described as "elevated," "low," "absent," or if it is outside the reference range.
    Return the abnormal values along with the associated measurement.
    If no abnormal values are found, respond with 'None'.
    """
    extraction_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", f"summary: {summary}")
        ]
    )

    chain = extraction_prompt | llm
    extracted_values = chain.invoke({summary : summary})  # Invoke with an empty dict or any necessary input
    extracted_values = extracted_values.content
    print(extracted_values)
    return {"anamoly": extracted_values}


def root_cause(state):#THIS IS A NODE
    anamoly = state["anamoly"]
    # root_cause = state["root_cause"]

    response = llm.invoke(f"From the given extracted values find out the root causes.NOTE: Only find out root cause and nothing else. Values{anamoly}")
    response = response.content

    print(response)
    return {"root_cause" : response}


def root_cause_1(state):
    anamoly = state["anamoly"]

    response_1 = llm.invoke(f"From the given extracted values find out the root causes.NOTE: Only find out root cause and nothing else. Values{anamoly}")
    response_1 = response_1.content

    print(response_1)
    return {"root_cause" : response_1}