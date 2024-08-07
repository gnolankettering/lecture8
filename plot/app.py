from IPython.display import display, Image
from openai import OpenAI
import os
import pandas as pd
import json
import io
from PIL import Image
import requests
import config
import time

client = OpenAI(api_key=config.OPENAI_API_KEY)

#Lets import some helper functions for assistants from https://cookbook.openai.com/examples/assistants_api_overview_python
def show_json(obj):
    display(json.loads(obj.model_dump_json()))

def submit_message(assistant_id, thread, user_message,file_ids=None):
    params = {
        'thread_id': thread.id,
        'role': 'user',
        'content': user_message,
    }
    if file_ids:
        params['file_ids']=file_ids

    client.beta.threads.messages.create(
        **params
)
    return client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)

# Quick helper function to convert our output file to a png
def convert_file_to_png(file_id, write_path):
    data = client.files.content(file_id)
    data_bytes = data.read()
    with open(write_path, "wb") as file:
        file.write(data_bytes)


financial_data_path = 'data/NotRealCorp_financial_data.json'
financial_data = pd.read_json(financial_data_path)

file = client.files.create(
  file=open('data/NotRealCorp_financial_data.json',"rb"),
  purpose='assistants',
)

assistant = client.beta.assistants.create(
  instructions="You are a data scientist assistant. When given data and a query, write the proper code and create the proper visualization",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Calculate profit (revenue minus cost) by quarter and year, and visualize as a line plot across the distribution channels, where the colors of the lines are green, light red, and light blue",
      "file_ids": [file.id]
    }
  ]
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

while True:
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    try:
        #See if image has been created
        messages.data[0].content[0].image_file
        #Sleep to make sure run has completed
        time.sleep(5)
        print('Plot created!')
        break
    except:
        time.sleep(10)
        print('Assistant still working...')

plot_file_id = messages.data[0].content[0].image_file.file_id
image_path = "images/NotRealCorp_chart.png"
convert_file_to_png(plot_file_id,image_path)

#Upload
plot_file = client.files.create(
  file=open(image_path, "rb"),
  purpose='assistants'
)

submit_message(assistant.id,thread,"Give me two medium length sentences (~20-30 words per sentence) of the \
      most important insights from the plot you just created.\
             These will be used for a slide deck, and they should be about the\
                     'so what' behind the data."
)


# Hard coded wait for a response, as the assistant may iterate on the bullets.
time.sleep(10)
response = get_response(thread)
bullet_points = response.data[0].content[0].text.value
print(bullet_points)

submit_message(assistant.id,thread,"Given the plot and bullet points you created,\
        come up with a very brief title for a slide. It should reflect just the main insights you came up with."
)

#Wait as assistant may take a few steps
time.sleep(10)
response = get_response(thread)
title = response.data[0].content[0].text.value
print(title)

company_summary = "NotReal Corp is a prominent hardware company that manufactures and sells processors, graphics cards and other essential computer hardware."

response = client.images.generate(
  model='dall-e-3',
  prompt=f"given this company summary {company_summary}, create an inspirational \
    photo showing the growth and path forward. This will be used at a quarterly\
       financial planning meeting",
       size="1024x1024",
       quality="hd",
       n=1
)
image_url = response.data[0].url




