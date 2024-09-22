import os
from anthropic import Anthropic
import streamlit as st

from models.text_config import ADDITIONAL_GUARDRAILS, EXAMPLES

MODEL_NAME = "claude-3-5-sonnet-20240620"

IDENTITY = """You are a health chatbot, a friendly and knowledgeable AI assistant for a virtual care clinic in Rural Ghana. 
You will be presented with patients who have various acute and chronic medical issues. You will use all the information you
have on the patient and factual medical knowledge to answer their questions, provide advice on ways to treat their
conditions, and ways to prevent further complications. This includes taking into account: occupation, age, gender,
previous health history, family history, current diagnosis and treatment (if given) and the context provided to you in conversation to share information
about how their conditions will specifically affect them, and how they can improve their day-day life. As the first message to 
the patient, you will introduce yourself and mention what you know about the patient based on the patient context to start
the conversation."""

sample_patient = {
    "Name": "Jane Doe",
    "Occupation": "Carrot Farmer",
    "DOB": "09/21/2006",
    "Gender": "Female",
    "Diagnosis": "Malaria, malnutrition",
    "Symptoms": ["fever", "chills", "headache", "nausea", "fatigue"],
    "Exercise": "Farming 8h of the day, every day, dance",
    "Diet": "Cassava, root vegetables",
    "Family History": "hypertension, diabetes",
    "Treatment": "Malaria pills"
}
def get_patient_context(patient: dict):
    patient_context = f"""
        Information about the patient: 
            The patient's name is {patient["Name"]}, and their occupation is {patient["Occupation"]}.
            Their date of birth is {patient["DOB"]}, so calculate their age based on the year given as MM/DD/YYYY
            and the current year. Their diagnosis given is {patient["Diagnosis"]}, and the treatment is {patient["Treatment"]}. 
            If these are none, they have not been given a diagnosis. Their current symptoms are a list of 
            {patient["Symptoms"]}. Their exercise consists of {patient["Exercise"]}, and their diet is {patient["Diet"]}. 
    """
    return patient_context

TASK_SPECIFIC_INSTRUCTIONS = ' '.join([
   EXAMPLES,
   ADDITIONAL_GUARDRAILS,
   get_patient_context(sample_patient)
])

class MedicalChatbot:
    
    def __init__(self, session_state):
        self.anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.session_state = session_state

    def generate_message(self, messages,max_tokens):
        try:
            response = self.anthropic.messages.create(
                model = MODEL_NAME,
                system = IDENTITY,
                max_tokens=max_tokens,
                messages = messages,
            )
            return response
        except Exception as e:
            return {"error": str(e)}
        
    def process_user_input(self, user_input):
        self.session_state.messages.append({"role": "user", "content": user_input})
        response_message = self.generate_message(
           messages=self.session_state.messages,
           max_tokens=2048,
        )
        if "error" in response_message:
           return f"An error occurred: {response_message['error']}"
        
        elif response_message.content[0].type == "text":
           response_text = response_message.content[0].text
           self.session_state.messages.append(
               {"role": "assistant", "content": response_text}
           )
           return response_text
        else:
           raise Exception("An error occurred: Unexpected response type")


        





