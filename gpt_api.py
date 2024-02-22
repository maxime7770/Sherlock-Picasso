import base64
import requests
#from api_keys import OPENAI_API_KEY
from openai import OpenAI
import streamlit as st

# OpenAI API Key
api_key = st.secrets["OPENAI_API_KEY"]

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def image_to_text(base64_image, prompt):

    # Getting the base64 string
    #base64_image = encode_image(image_path) #use this if image_path is given

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print("RESPONSE:  ", response)
    print(" ")
    return response.json()['choices'][0]['message']['content']


def text_to_text(text_input, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
       model="gpt-3.5-turbo-0125",
       messages=[
          {"role": "system", "content": prompt},
          {"role": "user", "content": text_input}
        ]
    )

    return response.choices[0].message.content


def text_to_text_v2(user_prompt, json_format=False):
    client = OpenAI(api_key=api_key)

   
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        model = "gpt-4-1106-preview",
        messages=[
            {"role": "user", "content": user_prompt},
        ]
    )
    
    return response.choices[0].message.content



if __name__ == "__main__":
    image_path = "posts_cristiano/2024-02-15_16-29-45_UTC.jpg"
    # prompt = "What objects are in the image?"
    # image_to_text(image_path, prompt)