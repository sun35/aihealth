from typing import Dict, List
from openai import OpenAI
from datetime import datetime
import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# sex: "man" | "woman"
# dob: YYYY-MM-DD
# location: string
# issue: Issue[]
# pastHistory: Issue[]
# family: Family[]

class Issue():
  type: str;
  since: str;
  until: str | None;
  thingsDone: str;

class Family():
  relationship: str;
  issue: str;

def show_image_from_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="Generated Stretches", use_column_width=True)
    except requests.RequestException as e:
        st.error(f"Error loading image from URL: {e}")

def getAge(birthdate):
  # Convert the birthdate string to a datetime object
  birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
  
  # Get the current date
  today = datetime.today()
  
  # Calculate the age
  age = today.year - birthdate.year
  
  # If the birthday hasn't occurred yet this year, subtract 1 from the age
  if (today.month, today.day) < (birthdate.month, birthdate.day):
      age -= 1
      
  return age

def makeImage(sex: str, dob: str, occupation: str, location: str, issues: List[Dict[str, str]], pastHistories: List[Dict[str, str]], familyHistories: List[Dict[str, str]]):
  client = OpenAI(api_key = os.environ["openai_key"])

  age = getAge(dob)

  prompt = f"This guide is designed to empower a patient who is physically {age} years old {sex} living in {location} who work as a {occupation}, with simple yet effective strategies to maintain your health and prevent common issues right at home. By integrating these habits into your daily routine, you can improve your overall well-being. Today, the target audience for this guide are experiencing "

  if issues:
    for issue in issues:
      type = issue["type"]
      since = issue["since"]
      prompt += f"{type} since {since}. "

      if issue["thingsDone"]:
        things = " ".join(issue["thingsDone"])
        prompt += f"The person has tried {things}. "

  if pastHistories:
    for history in pastHistories:
      thingsDone = " ".join(history["thingsDone"])
      type = history["type"]
      since = history["since"]
      if "until" in history:
        until = history["until"]
        prompt += f"The person had {type} in the past since {since} until {until}. I did {thingsDone}. "
      else:
        prompt += f"The person had {type} in the past since {since}. I did {thingsDone}. "


  if familyHistories:
    for history in familyHistories:
      relationship = history["relationship"]
      issue = history["issue"]
      prompt += f"My {relationship} had {issue}. "
  
  prompt += "Please provide a series of at-home stretches. Please make sure there are no words in the image. If possible, make the image a grid of multiple stretches. Make sure to have all the images in the frame so that it's not cut. The focus of the guide should be the stretches and not the person."

  response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url

  print(image_url)
