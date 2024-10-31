from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

import config
import json

client = OpenAI(api_key=config.OPENAI_API_KEY)

# Download the transcript from the YouTube video
transcript_list = YouTubeTranscriptApi.list_transcripts('dYXstMaO3_8')
transcript = transcript_list.find_generated_transcript(['en']).fetch()

# Extract and concatenate all text elements
concatenated_text = " ".join(item['text'] for item in transcript)

#  Call the openai ChatCompletion endpoint, with the ChatGPT model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the following text."},
        {"role": "assistant", "content": "Yes."},
        {"role": "user", "content": concatenated_text}])

print(response.choices[0].message.content)

