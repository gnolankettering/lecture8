from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)
from typing import List

def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages)
    return (response.choices[0].message.content)


def assist_journalist(facts: List[str], tone: str, length_words: int, style: str):
    facts = ", ".join(facts)
    msgs=[{"role": "system", "content": "You are an assistant for journalists. \
        Your task is to write articles, based on the FACTS that are given to you. \
        You should respect the instructions: the TONE, the LENGTH, and the STYLE"},
        {"role": "user", "content": f'FACTS: {facts} TONE: {tone} LENGTH: {length_words} words STYLE: {style}'}
    ]
    return ask_chatgpt(msgs)

print(assist_journalist(['The sky is blue', 'The grass is green'], 'informal', 100, 'blogpost'))