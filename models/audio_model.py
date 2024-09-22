
from pathlib import Path
from openai import OpenAI

from text_config import ADDITIONAL_GUARDRAILS, EXAMPLES
from text_model import sample_patient, get_patient_context

AUDIO_IDENTITY = """You are a health expert, a friendly and knowledgeable AI assistant for a virtual care clinic in Rural Ghana. 
Talk about preventative care and how the conditions of the described patient will specifically affect them, and how they can improve
their day-day life. Do not include anything a narrator would not say aloud. If the patient is seven or younger than seven years old,
write an engaging story, like Aesop's fables. If the patient is older than seven, write an engaging podcast episode. Again, do not 
include directions or titles. """

AUDIO_TASK_SPECIFIC_INSTRUCTIONS = ' '.join([
   AUDIO_IDENTITY,
   ADDITIONAL_GUARDRAILS,
   get_patient_context(sample_patient)
])

class MedicalAudio: 
    
    def __init__(self): 
        self.client = OpenAI()
        #self.session_state = session_state
        self.speech_file_path = Path(__file__).parent / "speech.mp3"

    def make_script(self):
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
          {"role": "system", "content": "You are a skilled storyteller, and an efficient and engaging communicator."},
          {"role": "user", "content": AUDIO_TASK_SPECIFIC_INSTRUCTIONS}
          ]
        )
        return response.choices[0].message.content

    def make_audio(self, lyrics): 
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input= lyrics 
            ) as  response:
                response.stream_to_file(self.speech_file_path) 

a = MedicalAudio() 
a.make_audio((a.make_script()))
